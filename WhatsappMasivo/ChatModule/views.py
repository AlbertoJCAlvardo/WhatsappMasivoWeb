from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
import json

from django.template.loader import render_to_string
from core.utils import validate_session, validate_user, get_user_name, validate_login, repr_dic, print_dic, convert_query_dict
from core.formatter import format_string, format_phone_numbers, set_wa_format
from django.views.decorators.csrf import csrf_exempt
from core.utils import (send_message, register_template, get_components, 
                        check_template_status, remove_rejected_template, get_image_url, get_image_from_url)
from django.views.decorators.csrf import csrf_exempt
from db.utils import DatabaseManager
from core.config import settings
from heyoo import WhatsApp
import pandas as pd
import asyncio
import random
from time import sleep, time
from datetime import datetime
import pytz
# Create your views here.



@csrf_exempt
def chat_module(request):

    try:
        if request.method == 'GET':
            user = request.GET.get('user', None)
            session_id = request.GET.get('session_id', None)
            
            print(f'user: {user}, session_id:{session_id}')

            if validate_user(user):

                context = {'user':user,
                           'session_id':session_id}
                return HttpResponse(render_to_string('ChatModule/chatmodule.html', context=context))
            
    
        
        return HttpResponseRedirect('/data_upload')
    except Exception as e:
        print(repr(e))
        return HttpResponseRedirect('/data_upload')

@csrf_exempt
def whatsapp_webhook(request):
    
    if request.method == 'GET':
        print('\n\n\nwebhook recieved!')
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        

        if mode == 'subscribe' and token == settings.WEBHOOKS_TOKEN:
            print('webhook validated')
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)

 
    if request.method == 'POST':
        data = json.loads(request.body)
       
        print(f'\n\n\n\n')
        
        print(repr_dic(data))
        if 'object' in data.keys() and 'entry' in data.keys():
         
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry  in data['entry']:

                        conversation_id = entry['id']
                        changes = entry['changes'][0]
                       
                        if 'contacts' in changes['value'].keys() and 'messages' in changes['value'].keys():
                            value =  changes['value']

                            profile_name = value['contacts'][0]['profile']['name']
                          
                            from_id =  value['messages'][0]['from']
                            wamid = value['messages'][0]['id']
                            timestamp = value['messages'][0]['timestamp']
                            datetimes = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                            destiny = value['metadata']['display_phone_number']
                            message_type = value['messages'][0]['type']
                            content =  json.dumps(value['messages'][0][message_type])
                            

                            dm = DatabaseManager()
                            query = f"""
                                        SELECT DISTINCT(USUARIO) USUARIO, FECHA
                                        FROM CL.WHATSAPP_COMUNICATE V
                                        WHERE DESTINO = '52' || {from_id[3:]}
                                        AND ORIGEN = '{destiny[3:]}'
                                        ORDER BY V.FECHA DESC

                                    """
                            headers, dta = dm.execute_query(query=query)
                           
                            user = None



                            if len(dta) > 0:
                                user = dta[0][0]
                            
                            dm.insert_message_response(message_data={
                                    'date': datetimes,
                                    'origin': from_id,
                                    'wamid': wamid,
                                    'destiny': destiny,
                                    'conversation_id': conversation_id,
                                    'message_type': message_type,
                                    'content': content,
                                    'name':profile_name,
                                    'user': user
                                })
                        
                            

                        if 'statuses' in changes['value'].keys():
                            wamid = changes['value']['statuses'][0]['id']
                            status = changes['value']['statuses'][0]['status']

                            dm = DatabaseManager()
                            dm.update_message_status(message_data={
                                 'wamid': wamid,
                                 'status': status,
                                 'conversation_id': conversation_id   
                                })


                except Exception as e:
                    print(repr(e))

        return HttpResponse('success', status=200 )

@csrf_exempt
def chat_list(request):
    if request.method == 'GET':
        user = request.GET['user']
        page = request.GET['page']
        print(user, page)
        try:
            dm = DatabaseManager()

            query = f"""
                    SELECT   CASE
                        WHEN FLOW = 'ENVIADO' THEN '521' || SUBSTR(V.ORIGEN,3,13)
                        ELSE V.ORIGEN
                        END ORIGEN,
                        CASE
                            WHEN FLOW = 'ENVIADO'  THEN V.ORIGEN
                            ELSE V.DESTINO
                        END
                        TEL_EMPRESA, 
                        CASE
                            WHEN FLOW = 'ENVIADO' THEN V.DESTINO
                            ELSE  V.ORIGEN
                        END TEL_USUARIO,
                    
                        FECHA, TIEMPO, USUARIO, UNREAD_MESSAGES, STATUS_CONVERSACION, PROFILE_NAME, CONTENIDO,   TIPO, FLOW, START_DATE, START_TIME
                    FROM (SELECT
                                        V.ORIGEN,
                                        V.DESTINO,
                                        TO_CHAR(V.FECHA, 'MM/DD/RRRR')                  FECHA,
                                        TO_CHAR(FECHA, 'HH24:MM:SS')                       TIEMPO,
                                        V.USUARIO,
                                        (SELECT COUNT(*)
                                        FROM WHATSAPP_MASIVO_RESPUESTA
                                        WHERE ORIGEN = V.ORIGEN AND STATUS = 'unread') UNREAD_MESSAGES,
                                        CASE
                                            WHEN SYSDATE - V.FECHA >= 1 THEN 'INACTIVA'
                                            ELSE 'ACTIVA'
                                            END                                         STATUS_CONVERSACION,
                                        PROFILE_NAME,
                                        CONTENIDO,
                                        TIPO, 'RECIBIDO' FLOW

                                FROM CL.WHATSAPP_MASIVO_RESPUESTA V
                                UNION
                                SELECT
                                        B.DESTINO ORIGEN,
                                        B.ORIGEN DESTINO,
                                        TO_CHAR(B.FECHA, 'MM/DD/RRRR')                  FECHA,
                                        TO_CHAR(FECHA, 'HH24:MM:SS')                       TIEMPO,
                                        B.USUARIO,
                                        0 UNREAD_MESSAGES,
                                        CASE
                                            WHEN SYSDATE - B.FECHA >= 1 THEN 'INACTIVA'
                                            ELSE 'ACTIVA'
                                            END                                         STATUS_CONVERSACION,
                                        CASE WHEN '521' || SUBSTR(B.DESTINO,3,13) IN (SELECT DISTINCT(ORIGEN) FROM CL.WHATSAPP_MASIVO_RESPUESTA) THEN
                                        (SELECT DISTINCT(PROFILE_NAME) FROM CL.WHATSAPP_MASIVO_RESPUESTA WHERE ORIGEN = '521' || SUBSTR(B.DESTINO,3,13))

                                        ELSE
                                            B.DESTINO
                                        END PROFILE_NAME,
                                        CONTENIDO,
                                        TIPO, 'ENVIADO' FLOW

                                FROM CL.WHATSAPP_COMUNICATE B) V


                                JOIN(
                                    SELECT DISTINCT(ORIGEN), TO_CHAR(MAX(START_DATE), 'MM/DD/RRRR') START_DATE, TO_CHAR(MAX(START_DATE), 'HH24:MM:SS') START_TIME
                                    FROM(

                                        SELECT DISTINCT(ORIGEN) ORIGEN, MAX(FECHA) START_DATE
                                        FROM CL.WHATSAPP_MASIVO_RESPUESTA
                                        WHERE USUARIO = '{user} '
                                        GROUP BY ORIGEN
                                        UNION
                                        SELECT DISTINCT(DESTINO) ORIGEN, MAX(FECHA) START_DATE
                                        FROM CL.WHATSAPP_COMUNICATE
                                        WHERE USUARIO = '{user}'
                                        GROUP BY DESTINO
                                    )
                                    GROUP BY ORIGEN

                                ) B
                                ON V.ORIGEN = B.ORIGEN AND V.FECHA = START_DATE AND V.TIEMPO = START_TIME
                                WHERE V.USUARIO = '{user}' AND V.CONTENIDO IS NOT null
                                ORDER BY FECHA DESC
                                OFFSET ({page}- 1)  * 10 ROWS
                                FETCH NEXT 10 ROWS ONLY

                                            """
            
          
            headers, conversations = dm.execute_query(query)
            conv_list = convert_query_dict(headers=headers, data=conversations)
            return HttpResponse(json.dumps(conv_list), status=200)
        except Exception as e:
            print(repr(e))
            return HttpResponse('error', status=403)

@csrf_exempt
def chat_window(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        page = request.GET.get('page')
        user = request.GET.get('user')
        print(f'ph: {phone_number}\n\n\n, {type(phone_number)}')
        print(f'pg: {page}\n\n\n')
        if len(phone_number) > 9:
            if len(phone_number) == 12:
                phone_number = phone_number[2:12]
            if len(phone_number) == 13:
                phone_number = phone_number[3:13]
        print(phone_number)
        try:
            dm = DatabaseManager()
            query=f"""
                               SELECT FECHA AS datetime, TO_CHAR(FECHA, 'MM-DD-RR') FECHA, TO_CHAR(FECHA, 'HH24:MI') TIEMPO, ORIGEN, DESTINO, WAMID, CONVERSATION_ID, TIPO,
                                    CONTENIDO, STATUS, USUARIO, 'RECIBIDO' FLOW
                                FROM CL.WHATSAPP_MASIVO_RESPUESTA
                                WHERE ORIGEN = '521' || '{phone_number}'
                                UNION
                                (SELECT FECHA AS DATETIME, TO_CHAR(FECHA, 'MM-DD-RR') FECHA,
                                        TO_CHAR(FECHA, 'HH24:MI') TIEMPO,
                                        ORIGEN,
                                        DESTINO,
                                        WAMID,
                                        CONVERSATION_ID,
                                        TIPO_mensaje,
                                        MENSAJE  CONTENIDO,
                                        STATUS_MENSAJE STATUS,
                                        USUARIO ,
                                        'ENVIADO' FLOW
                                FROM CL.WHATSAPP_COMUNICATE
                                WHERE SUBSTR(DESTINO, 3,11) = '{phone_number}' AND STATUS_MENSAJE != 'failed'
                                
                                )

                                ORDER BY DATETIME DESC
                                OFFSET ({page} - 1)  * 30 ROWS
                                FETCH NEXT 30 ROWS ONLY
                             """
            headers, data = dm.execute_query(query)
            for i in data:
                if isinstance(i, list):
                    
                    for j in range(len(i)):

                        if isinstance(i[j], str):
                            
                            if '\"' in i[j]:
                                
                                i[j] = json.loads(i[j])
           
                                
            
            query_list = convert_query_dict(headers, data)
            print(len(query_list))

           

            return HttpResponse(json.dumps(query_list), status=200)

        except Exception as e:
            print(repr(e))
            error_dic=  {'error':repr(e)}
            return HttpResponse(json.dumps(error_dic), status=403)

@csrf_exempt
def api_image(request):
    
    if request.method == 'GET':
        try:

            image_id = request.GET['id']
            response =  asyncio.run(get_image_url(image_id))
            if response != 404:
                response['token']  = settings.ACCESS_TOKEN
                
                img = asyncio.run(get_image_from_url(response['url']))
            
                response['base64'] = img

                return HttpResponse(json.dumps(response), 200)
            
            return HttpResponse(json.dumps({'error':'API Error'}), status=403)
        except Exception as e:
            print(repr(e))
            return HttpResponse(repr(e), 403)
        

@csrf_exempt
def get_pages(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        
        try:
            dm = DatabaseManager()
            headers, data = dm.execute_query(f"""
                            SELECT COUNT(*) PAGINAS
                            FROM(
                               SELECT FECHA AS DATETIME, TO_CHAR(FECHA, 'MM-DD-RR') FECHA, TO_CHAR(FECHA, 'HH24:MI') TIEMPO, ORIGEN, DESTINO, WAMID, CONVERSATION_ID, TIPO,
                                    CONTENIDO, STATUS, USUARIO, 'RECIBIDO' FLOW
                                FROM CL.WHATSAPP_MASIVO_RESPUESTA
                                WHERE ORIGEN = '{phone_number}'
                                UNION
                                (SELECT FECHA AS DATETIME, TO_CHAR(FECHA, 'MM-DD-RR') FECHA,
                                        TO_CHAR(FECHA, 'HH24:MI') TIEMPO,
                                        ORIGEN,
                                        DESTINO,
                                        WAMID,
                                        CONVERSATION_ID,
                                        TIPO_mensaje,
                                        MENSAJE  CONTENIDO,
                                        STATUS_MENSAJE STATUS,
                                        USUARIO ,
                                        'ENVIADO' FLOW
                                FROM CL.WHATSAPP_COMUNICATE
                                WHERE DESTINO = '{phone_number}'
                                )
                                )   
                             """)
     

            paginas = int(data[0][0]) // 30
            return HttpResponse(json.dumps({'paginas': paginas}), status=200)

        except Exception as e:
            print(repr(e))
            error_dic=  {'error':repr(e)}
            return HttpResponse(json.dumps(error_dic), status=403)
        
@csrf_exempt
def update_seen(request):
    if request.method == 'GET':
        try:
            phone_number = request.GET.get('phone_number')
            dm = DatabaseManager()
            dm.update_seen_status(phone_number=phone_number)
            print(f'chat {phone_number} visto.')
            return HttpResponse(json.dumps({'status':'ok'}), 200)
        except Exception as e:
            error = repr(e)
            print('Hubo pedos', error)
            return HttpResponse(json.dumps({'error':error}))