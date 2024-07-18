from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, FileResponse
import json
from core.utils import validate_session, validate_user, get_user_name, validate_login, format_number, repr_dic
from core.formatter import format_string, format_phone_numbers, set_wa_format
from django.views.decorators.csrf import csrf_exempt
from core.utils import (send_message, register_template, get_components, 
                        check_template_status, remove_rejected_template, upload_file_api,
                        get_upload_permission, upload_file_api_2, get_user_projects, format_project_names,
                        get_phone_number, send_text_mesage_api, querydic_to_df, deformat_project_name)
from db.utils import DatabaseManager
from core.config import settings
import io
import pandas as pd
import asyncio
import random
from time import sleep, time
from datetime import datetime
import pytz
from datetime import timedelta
import copy
# Create your views here.

@csrf_exempt
def index(request):
    
    context = {}
    return HttpResponse(render_to_string('main.html', context=context))

@csrf_exempt
def login(request):
    if request.method == 'GET':
        try:
            context = {}
            return HttpResponse(render_to_string('login.html', context=context))
        except Exception as e:
            raise(e)
        
    elif request.method == 'POST':
        
        try:
            request = json.loads(request.body)
            user = request['user']
            password = request['password']
            print(user, password)
            db = DatabaseManager()
            start = time()
            validation = validate_login(user=user,
                                           password=password)
            print(validation)
            exec_time = time() - start
            print(f'Query exec time: {exec_time}')

            if validation == 'correct':
                header, sesion_id = db.execute_query("SELECT  pkg_general.f_sesion FROM dual")
                print(sesion_id)
                return HttpResponse(json.dumps({'message':'ok',
                                                'session_id':sesion_id[0][0]}))
            else:
                message = ""
                if validation == 'user_not_exist':
                    message = "El usuario no existe"
                if validation == 'wrong_password':
                    message = 'Contraseña Incorrecta'
                if validation == 'unauthorized':
                    message = 'Usuario no autorizado'
                    
                print(message)
                return HttpResponse(json.dumps({'message':message}))
                
                

        except Exception as e:
            print(repr(e))
            return HttpResponse(json.dumps({'message':'Error en el servidor'}))


@csrf_exempt
def format_table(request):
    
    if request.method == 'POST' and request.FILES['file'] is not None:
        print('request')
        try:
            file_data = request.FILES['file']
            extension = str(file_data).split('.')[1]
            footer = ""
            df = None

            if extension == 'xlsx':
                df = pd.read_excel(file_data)
            if extension == 'csv':
                df = pd.read_csv(file_data)

            content = df.iloc[:, :].values.tolist()

            if len(list(df.iloc[:, [0]].values)) > 10:
                print('logintud mayoer a 10')
                footer = f"Ejemplo demostrativo, 10 celdas de {len(content)}"
                content = df.iloc[0:10, :].values.tolist()
            print(len(list(df.iloc[:,[0]].values)))
           
            
            response = {
                        'footer':footer,
                        'headers':df.columns.to_list(),
                        'content':content,
                        'df':df.to_json()  
                }
            response = json.dumps(response)
            return HttpResponse(response, status=200)

           
            
        except Exception as e:
            print(repr(e))
            response = json.dumps({
                'error': repr(e),
                'status': 400
            })
            return HttpResponse(response, status=400)
        

@csrf_exempt
def data_upload(request):
    try:
        print(request.method)
        if request.method == 'GET':
            print('hola -.-')
            sesion_id = request.GET.get('session_id', None)
            user = request.GET.get('user', None)
            if True:
            #if validate_session(sesion_id) and validate_user(user):
                
                context = {'user':user, 
                           'session_id':sesion_id,
                           'user_name':get_user_name(user),
                           'headers':None,
                           'content':None
                          
                           }
                return HttpResponse(render_to_string('data_upload_index.html',
                                                        context=context))
            else:
                return HttpResponseRedirect('/login')


        elif request.method == 'POST':
            sesion_id = request.POST.get('session_id', None)
            user = request.POST.get('user', None)
            print(sesion_id, user)
            if validate_user(user):
                
                filename = "Archivo no seleccionado"
                footer = ""
                ar = request.FILES.get('docfile', None)
                if request.FILES.get('docfile') != None:
                    
                    ar = request.FILES['docfile']

                    extension = str(ar).split('.')[1]
                    
                    df = None

                    if extension == 'xlsx':
                        df = pd.read_excel(ar)
                    if extension == 'csv':
                        df = pd.read_csv(ar)

                    content = df.iloc[:, :].values

                    filename = str(ar)

                    if len(list(df.iloc[:, [0]])) > 10:
                        footer = f"Ejemplo demostrativo, 10 celdas de {len(content)}"
                        content = df.iloc[:, 0:10].values
                        
                    if True:
                            print(content)
                            print(df.to_json())
                            context = {'user':user,
                                        'session_id':sesion_id, 
                                        'user_name':get_user_name(user),
                                        'filename':filename,
                                        'footer':footer,
                                        'headers':df.columns.to_list(),
                                        'content':df.to_json(),
                                        'df':df.to_json(),        
                                }
                            return HttpResponse(render_to_string('data_upload_index.html',
                                                                context=context))
            
            return HttpResponseRedirect('/login')    
            
       
    except Exception as e:
        print('\n\n\n\n Algo salio terrible')
        print(repr(e))
        return HttpResponseRedirect('/login')
    
@csrf_exempt
def message_sending(request):
     
    try:
        if request.method == 'POST':
            filename = request.POST.get('filename', None)
            df = request.POST.get('df', None)
           
            user = request.POST.get('user', None)
            
            print(user,filename)
            if df is not None:
                
                df = pd.read_json(df)
                
                df.head()
                index = random.randint(0, df.iloc[:,[0]].size-1)

            print( format_project_names(get_user_projects(user)))
            context = {'user':user,
                       'user_name': get_user_name(user),
                       'filename':filename,
                       'df':df.to_json,
                       'headers':list(df.columns), 
                       'test':df.iloc[index:index+1].to_json,
                       'empresas': format_project_names(get_user_projects(user))}   

            return HttpResponse(render_to_string('message_sender_index.html',
                                                 context=context))
        else:
            return HttpResponseRedirect('/data_upload/')
    except Exception as e:
        print(repr(e))
        return HttpResponseBadRequest(f'{repr(e)}')
    
@csrf_exempt
def check_message(request):
    try:
        if request.method == 'POST':
            body = json.loads(request.body.decode('utf-8'))
            message = body['message']
            df = body['test']
            df = pd.read_json(df)
            
            
            formatted_message = format_string(text=message, data=df.iloc[0])
            print(formatted_message)
            return JsonResponse(data={'message':formatted_message},
                                status=200)


    except Exception as e:
        print(repr(e))
        return JsonResponse(data={message:"error"},
                                status=400)

@csrf_exempt
def template_registry(request):
    try:
         if request.method ==  'POST':
            body = json.loads(request.body.decode('utf-8'))
            print('-*-*-*-*-\n\n\n', repr_dic(body))


            message = body['message']
            df = body['df']
            from_number = body['from_number']
            print(type(df),df)
            auxdic = json.loads(df)
            if message is not None and  df is not None and from_number is not None:
                print(type(auxdic),auxdic)
                repr_dic(auxdic)
                print('auxiliardic sesupone ya impreso')
                df = pd.read_json(df)

                pre_component_dic = {}
                pre_components = message['components']
                header_type = message['type']
                file_data =  body['file_data']

                for i in pre_components:
                    print(i)
                    if i != None:
                        print(i, type(i))
                        if type(i) == 'str':
                            i = json.loads(i)
                        print(i['type'])
                        pre_component_dic[i['type']] = i

                tokens_header = {}
                if header_type != 'text':
                    
                    permisions = file_data['permisions']

                    pre_component_dic['HEADER']['example'] = {
                        'header_handle': permisions['resource_id']
                    }
                    
                else:
                    
                    header_text= pre_component_dic['HEADER']['text']
                    formatted_header, tokens_header = set_wa_format(message=header_text, data=df.iloc[0])
                    
                    pre_component_dic['HEADER']['text'] = formatted_header
                    if len(list(tokens_header.keys())) > 0:
                        pre_component_dic['HEADER']['example'] = {
                            'header_text':get_components(df[list(tokens_header.keys())])
                        }
                
                body_message = pre_component_dic['BODY']['text']
                formatted_body, tokens_body = set_wa_format(message=body_message, data=df.iloc[0])

                print('fbody: ',formatted_body)
                pre_component_dic['BODY']['text'] = formatted_body

                if len(list(tokens_body.keys())) > 0:
                    pre_component_dic['BODY']['example'] = {
                                        'body_text': [get_components(df[list(tokens_body.keys())])]
                                    }
                

                components = []
                for i in pre_component_dic.keys():
                    print(i)
                    components.append(pre_component_dic[i])
                print(f'Intentando registrar {components}')
                template_name, response =  asyncio.run(register_template(components, from_number=from_number))
                i
                print(template_name)
                if 'error' not in response.keys():
                    status = response['status']
                
                    for _ in range(50):
                        sleep(2)
                        print('Esperando...')
                        if status != 'PENDING':
                            break
                        
                        status = asyncio.run(check_template_status(response['id']))
                    response['status'] = 400
                    response['template_name'] = template_name
                                    
                    if status == 'APPROVED':
                        response['status'] = 200
                        response['tokens'] = {'tokens_header': tokens_header, 
                                            'tokens_body': tokens_body}
                        
                    if status == 'REJECTED':
                        removed = asyncio.run(remove_rejected_template(template_name=template_name))
                        print('REJECTED')
                    return HttpResponse(json.dumps(response))
                
                error = response['error']
                
                if error['code'] == 190:
                    
                    response = {'status':'ERROR',
                                'error': 'Fallo en Token de Acceso de Meta'}
                    return HttpResponse(json.dumps(response))
                    
                if error['code'] == 80008:
                    
                    response = {'status':'ERROR',
                                'error': 'Muchos Intentos, API saturada'}
                    return HttpResponse(json.dumps(response))
                
            response = {'status':'ERROR', 'error':'Faltan parametros'}
            return HttpResponse(json.dumps(response))

    except Exception as e:
        print('error: ', repr(e))
        response = {'status':'ERROR', 'error':F'{repr(e)}'}
        return HttpResponse(json.dumps(response))


@csrf_exempt
def get_file_authorization(request):

    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))


@csrf_exempt
def send_messages(request):
    try:
            
         if request.method == "POST":
        
            body = json.loads(request.body.decode('utf-8'))
            repr_dic(body)
            message = body['message']

            df = body['df']
            df = pd.read_json(df)
            template_name = body['template_name']
            pre_component_dic = {}
            component_dic = {}
            from_number = body['from_number']
            pre_components = message['components'].copy()
            header_type = message['type']
            file_data = body['file_data']
            for i in pre_components:
                if i:
                    pre_component_dic[i['type']] = i
                    component_dic[i['type']] = {
                        'type': i['type']
                    }
            
            if header_type != 'text':
                ar = ""
                if header_type == 'file':
                  
                    permisions = file_data['permisions']
                    component_dic['HEADER']['parameters'] = [{
                        'type': 'DOCUMENT',
                        'document': {'id':permisions['display_id']}
                    }]
                    pre_component_dic['HEADER']['display_id'] = permisions['display_id']
                   

                if header_type == 'image':
                    permisions = file_data['permisions']
                    component_dic['HEADER']['parameters'] = [{
                        'type': 'IMAGE',
                        'image': {'id':permisions['display_id']}
                    }]

                    pre_component_dic['HEADER']['display_id'] = permisions['display_id']
           
            body_message = pre_component_dic['BODY']['text']
            
            formatted_body, tokens_body = set_wa_format(message=body_message, data=df.iloc[0])
            

            db = DatabaseManager('sistemas')
            
            df['NUMERO_TELEFONO'] = df['NUMERO_TELEFONO'].apply(format_number)
            

            numeros_validos, numeros = format_phone_numbers(df['NUMERO_TELEFONO'])
            
            counter = 0
            print('\n\n\n\nEnviando mensajes...')
          
            for index, row in df.iterrows():
                print('\n\n\n-----------',index)
                if True:  
                    if header_type == 'text':
                        header_parameters = []
                        pcc_d =pre_component_dic.copy()
                        header_message = pcc_d['HEADER']['text']
                        formatted_header, tokens_header = set_wa_format(message=header_message, data=df.iloc[[index], :])
                        
                        
                        pcc_d['HEADER']['content'] = formatted_header
                        for parameter in row.loc[tokens_header.keys()]:
                            header_parameters.append({
                                'type': 'text',
                                'text': str(parameter)
                            })
                            print(header_parameters)
                        component_dic['HEADER']['parameters'] = header_parameters

                      
                    formatted_body, tokens_body = set_wa_format(message=body_message, data=df.iloc[[index],:])
                    body_parameters = []

                    for parameter in row.loc[tokens_body.keys()]:
                        body_parameters.append({
                            'type': 'text',
                            'text': str(parameter)
                        })
                    
                    component_dic['BODY']['parameters'] = body_parameters

                    
                    components  = [component_dic['HEADER'], component_dic['BODY']]
                    
                   
                    
                    response = asyncio.run(send_message( 
                                                        numeros[row['NUMERO_TELEFONO']].replace('+', ''),
                                                        template_name=template_name, 
                                                        components=components,
                                                        from_number=from_number))
                    
                    
                    m_status = 'error'
                    wamid = ''
                    
                    if 'messages' in response.keys():
                        messages = response['messages'][0]

                        if messages['message_status'] == 'accepted':
                            m_status = 'ok'
                            counter += 1
                        wamid = messages['id']
                        
                  
                    n_dic = message.copy()
                    
                    li = n_dic['components']
                    
                    for ixx, i in enumerate(pre_components):
                        if i is not None:
                            aux = i.copy()
                            
                            if 'text' in i.keys():
                                
                                formatiado = format_string(aux['text'], data=df.iloc[[index]])
                                print(formatiado)
                                aux['text'] = formatiado
                                
                                li[ixx] = aux
                                

                       
                    
                    
                    n_dic['components'] = li
                    print(f'En teoria el mensaje ya fue formateado')      
                    print('message: ', n_dic)
                    
                    r_body = json.dumps(n_dic)
                    print('insertando en la base de datos...')
                    if 'RFC' in df.columns.values:
                        db.insert_message_registry(message_data={
                            'date':datetime.now(pytz.timezone("Mexico/General")).strftime("%Y-%m-%d %H:%M:%S"),
                            'user':body['user'],
                            'destiny':numeros[row['NUMERO_TELEFONO']].replace('+', ''),
                            'message': r_body,
                            'status_envio':m_status,
                            'type':'template',
                            'message_name':template_name,
                            'origin': get_phone_number(from_number),
                            'wamid':wamid,
                            'content': json.dumps(pre_component_dic),
                            'tipo': header_type,
                            'rfc': row['RFC']
                        })
                        
                    else:
                       
                        if from_number != 'Edilar':
                            db.insert_message_registry(message_data={
                                'date':datetime.now(pytz.timezone("Mexico/General")).strftime("%Y-%m-%d %H:%M:%S"),
                                'user':body['user'],
                                'destiny':numeros[row['NUMERO_TELEFONO']].replace('+', ''),
                                'message': json.dumps(r_body),
                                'status_envio':m_status,
                                'type':'template',
                                'message_name':template_name,
                                'origin': get_phone_number(from_number),
                                'wamid':wamid,
                                'content': json.dumps(pre_component_dic),
                                'tipo': header_type,
                                'rfc': None
                            })
                    
                    
            response = {
                'status':200,
                'error':'',
                'message_count':counter
            }
            return HttpResponse(json.dumps(response))
                                                 
    except Exception as e:
        print(repr(e))
        return HttpResponse(json.dumps({'status':400,
                        'error':repr(e)}))
    

    

@csrf_exempt
def home(request):
    return HttpResponseRedirect('/login/')


@csrf_exempt 
def upload_file(request):
    if request.method == 'POST':
        try:
           
            
           
            
            if request.FILES.get('file') != None:
                print(request)
                from_number = request.POST.get('from_number') 
                ar = request.FILES['file']
                data = request.FILES['file'].read()

                extension = str(ar).split('.')[1]
                
                for filename, file in request.FILES.items():
                    nme = request.FILES[filename].name
                    
                    name = filename
                
                mime = ""
                extension = extension.lower()
                if extension == 'jpg':
                    extension = 'jpeg'
                if extension in ("jpeg", 'jpg', 'png'):
                    
                    mime = f'image/{extension}'
                elif extension in ("mp4"):
                    mime = f'video/{extension}'
                else:   
                    mime = f'application/{extension}'
               
                
                file_data = {'mime':mime,
                             'length': len(data),
                             'data': data,
                             'name': nme}
                
                
                print('\n\n\npn---', from_number)
                
                
                permision = asyncio.run(get_upload_permission(file_data))
               
                resource_id = asyncio.run(upload_file_api(permision['id'], file_data))
                
                display_id = asyncio.run(upload_file_api_2(file_data, from_number))
                display_id = json.loads(display_id)
                response = {
                                        'resource_id': resource_id,
                                        'permision':  permision
                             }
                
                print(display_id)
                if 'id' in display_id.keys():
                    response['display_id'] = display_id['id']

                    return HttpResponse(json.dumps({'status':'ok', 'permisions':response}))
                else:
                    response['display_id'] = None
                    

                    return HttpResponse(json.dumps({'status':'error', 'error':"Error de registro"}))
        except Exception as e:
            print('error de registro')
            print(repr(e))
            return HttpResponse(json.dumps({'status': 'error', 'error':repr(e)}))



@csrf_exempt
def send_text_message(request):

    if request.method == 'POST':

        
        try:

            body = json.loads(request.body)
            print(body)
            to = body['phone_number']
            from_number = body['from_number']
            message  =  body['message']
            user = body['user']
            
            

            response = asyncio.run(send_text_mesage_api(message,from_number, to))

            m_body = {"components": 
                      [{"type": "HEADER", "format": "TEXT", "text": "", 
                        "content": "Apreciable {{1}} "}, 
                        {"type": "BODY", "text": f"{message}"},
                        {"type": "FOOTER", "text": ""}, 
                        'null'
                      ],
                        "type": "text", "buttons": 0}
            m_b =  { 
                       "BODY": {"type": "BODY", "text": f"{message}"},
                     
                        "type": "text"}
            
            m_m = json.dumps(m_body)
            if 'messaging_product' in response.keys():
                db = DatabaseManager('sistemas')
                db.insert_message_registry(message_data={
                            'date':datetime.now(pytz.timezone("Mexico/General")).strftime("%Y-%m-%d %H:%M:%S") ,
                            'user':user,
                            'destiny': to,
                            'message': m_m,
                            'status_envio':'ok',
                            'type':'template',
                            'message_name':None,
                            'origin': from_number,
                            'wamid':response['messages'][0]['id'],
                            'content': json.dumps(m_b),
                            'tipo': 'text'
                        })
                        
                response = {'status':'ok'}
            else:

             response = {'status':'error'}            
                
            
            return HttpResponse(json.dumps(response), status=200)
        
        except Exception as e:
            print(repr(e))
            response = json.dumps({
                'error': repr(e)
            })
            return HttpResponse(response, status=400)
        
@csrf_exempt
def get_phone(request):
    if request.method == 'GET':
        user = request.GET.get('user')
        
        data = get_user_projects(user)
        resp_dic = {'projects':data}
        status = 400
        if len(data) > 0:
            status = 200
        return HttpResponse(json.dumps(resp_dic), status=status)

@csrf_exempt
def history(request):
    if request.method == "GET":
        user = request.GET.get('user')
        if user is not None:
            projects = get_user_projects(user)

           
            context = {'user':user,
                       'user_name': get_user_name(user),
                       'empresas':format_project_names(get_user_projects(user))}
            return HttpResponse(render_to_string('message_story_view.html', context=context))

        HttpResponseRedirect('/login')

@csrf_exempt
def format_history(request):
     if request.method == 'POST':
        try:
            body = json.loads(request.body)
            project = body['project']
            user = body['user']
            project  = deformat_project_name(project)
            ph_query = f"""
                           
                            SELECT TELEFONO
                            FROM CL.CL_SYS_PROYECTO_WA
                            WHERE PROYECTO_ID = '{project}' 
                            
                        """
            dm1 = DatabaseManager('sistemas')
            headers, data = dm1.execute_query(ph_query)
            query = f"""
                        SELECT NOMBRE_MENSAJE ,     
                                CASE    
                                    WHEN TOTAL_EN_BASE > 0 THEN TO_CHAR(TOTAL_EN_BASE) ELSE '0'
                                END TOTAL_EN_BASE,
                                CASE    
                                    WHEN ENVIADOS_POR_APP > 0 THEN TO_CHAR(ENVIADOS_POR_APP) ELSE '0'
                                END ENVIADOS_POR_APP,
                                CASE    
                                    WHEN ENVIOS_EXITOSOS_META > 0 THEN TO_CHAR(ENVIOS_EXITOSOS_META) ELSE '0'
                                END ENVIOS_EXITOSOS_META,
                                CASE    
                                    WHEN ENVIOS_FALLIDOS_META > 0 THEN TO_CHAR(ENVIOS_FALLIDOS_META) ELSE '0'
                                END ENVIOS_FALLIDOS_META,
                                CASE    
                                    WHEN TELEFONOS_NO_VALIDOS > 0 THEN TO_CHAR(TELEFONOS_NO_VALIDOS) ELSE '0'
                                END ERROR_DE_DATOS_EN_BASE,
                                CASE    
                                    WHEN MONTO_POR_ENVIO > 0 THEN  '$\t' || TO_CHAR(MONTO_POR_ENVIO) ELSE '0'
                                END MONTO_POR_ENVIO,  FECHA, ORIGEN, USUARIO
                        FROM(
                        SELECT DISTINCT(V.NOMBRE_MENSAJE) NOMBRE_MENSAJE,
                        (SELECT COUNT(*) FROM CL.WHATSAPP_COMUNICATE WHERE  V.NOMBRE_MENSAJE = NOMBRE_MENSAJE)  TOTAL_EN_BASE,
                        (SELECT COUNT(*) FROM CL.WHATSAPP_COMUNICATE WHERE STATUS_ENVIO = 'ok' AND V.NOMBRE_MENSAJE = NOMBRE_MENSAJE) ENVIADOS_POR_APP,
                        (SELECT COUNT(*) FROM CL.WHATSAPP_COMUNICATE WHERE STATUS_MENSAJE <> 'failed' AND V.NOMBRE_MENSAJE = NOMBRE_MENSAJE) ENVIOS_EXITOSOS_META,
                        (SELECT COUNT(*) FROM CL.WHATSAPP_COMUNICATE WHERE (STATUS_MENSAJE = 'failed')AND V.NOMBRE_MENSAJE = NOMBRE_MENSAJE) ENVIOS_FALLIDOS_META,
                        (SELECT COUNT(*) FROM CL.WHATSAPP_COMUNICATE WHERE (STATUS_ENVIO <> 'ok')AND V.NOMBRE_MENSAJE = NOMBRE_MENSAJE) TELEFONOS_NO_VALIDOS,
                            TRUNC((SELECT COUNT(*) FROM CL.WHATSAPP_COMUNICATE WHERE STATUS_MENSAJE IN ('sent', 'delivered') AND V.NOMBRE_MENSAJE = NOMBRE_MENSAJE) * 0.7,2) MONTO_POR_ENVIO,
                        TO_CHAR(V.FECHA, 'RRRR-MM-DD') FECHA, ORIGEN, USUARIO
                        FROM CL.WHATSAPP_COMUNICATE V
                        WHERE ORIGEN = '{data[0][0]}'
                        GROUP BY NOMBRE_MENSAJE, FECHA, ORIGEN, USUARIO
                        ORDER BY FECHA DESC)
                        ORDER BY FECHA DESC

                    """


            dm = DatabaseManager('sistemas')
            data =  dm.execute_indexed_query(query)
            
            n_data= {}
            for i in data.keys():
                nkey = '\t'+i.replace('_', ' ').capitalize()+'\t'
                n_data[nkey] = data[i]

            df = querydic_to_df(n_data)
            
            content = df.iloc[:, :].values.tolist()
            
            print(len(list(df.iloc[:,[0]].values)))


           
            
            response = {
                        
                        'headers':df.columns.to_list(),
                        'content':content,
                        'df':df.to_json()  
                }
            response = json.dumps(response)
            return HttpResponse(response, status=200)

           
            
        except Exception as e:
            print(repr(e))
            response = json.dumps({
                'error': repr(e),
                'status': 400
            })
            return HttpResponse(response, status=400)

@csrf_exempt
def delete_template(request):
    if request.method == 'GET':
        template_name = request.GET.get('template_name')
        if template_name is not None:
            server_response = asyncio.run(remove_rejected_template(template_name=template_name))
            print(server_response)
            return HttpResponse(json.dumps({'status':'ok', 'data':server_response}),status=200)
        
    return HttpResponse(json.dumps({'status':'error','error':'Bad Request'}), status=401)

@csrf_exempt
def get_message_base(request,  template_name):

    if request.method == 'GET':
            message_name= template_name
            user = request.GET.get('user')
            if message_name is not None:
                
               
                query = f"""
                            SELECT NOMBRE_MENSAJE, FECHA, USUARIO, DESTINO, MENSAJE, FACILIDAD_COBRANZA_RFC RFC,
                            CASE
                                WHEN   STATUS_ENVIO <> 'ok' THEN 'ERROR_DE_DATOS_EN_BASE'
                                WHEN  STATUS_MENSAJE = 'failed' THEN 'FALLO_DE_META'
                            END RAZON_FALLA,
                            FALLO_META
                            FROM CL.WHATSAPP_COMUNICATE V
                            WHERE (STATUS_MENSAJE = 'failed' OR STATUS_ENVIO <> 'ok') AND V.NOMBRE_MENSAJE = '{message_name}'
                            
                            ORDER BY FECHA DESC
                        """


                dm = DatabaseManager('sistemas')
                data =  dm.execute_indexed_query(query)
               
                df = querydic_to_df(data)
                print(df)
                df.to_csv( 'base_fallas.csv', index=None)
                response = HttpResponse(content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=%s' % f'base_fallas_{message_name}.csv'
               
                response.write(open('base_fallas.csv').read())
                return response

            
    return HttpResponse(json.dumps({'error':'Falla'}),405)

@csrf_exempt
def file_test(request):
    context = {}
    

    return HttpResponse(render_to_string('file_test.html', context=context))

@csrf_exempt
def fix_cobranza(request):
    if request.method == 'POST' and request.FILES['file'] is not None:
        print('request')
        try:
            file_data = request.FILES['file']
            extension = str(file_data).split('.')[1]
            footer = ""
            df = None

            if extension == 'xlsx':
                df = pd.read_excel(file_data)
            if extension == 'csv':
                df = pd.read_csv(file_data)
            pre_component_dic ={"HEADER": 
                                {"type": "HEADER", 
                                "format": "TEXT",
                                "text": "\u00a1Felicidades {NOMBRE}!",
                                "content": "\u00a1Felicidades {{1}}!"}, 
                            "BODY":
                                {"type": "BODY", 
                                "text": " Elegiste formar parte del programa \u201cApoyo econ\u00f3mico adicional para fortalecer el desempe\u00f1o acad\u00e9mico y profesional de las figuras educativas del CONAFE\u201d.  \nAl elegir formar parte de este programa, CONAFE te entrega un apoyo econ\u00f3mico de $ 4,450.00 una vez que hayas completado el 50%, por $ 4,450.00, en \n*{OPCION_PAGO}* pagos de *$ {CUOTA}* , como previamente lo seleccionaste cuando realizaste tu registro.\n\n*Enviamos a tu correo {EMAIL} el contrato y el formato de pago*\n\n\u00a1Empieza hoy mismo!\nSi completas tu pago ahora mismo, ser\u00e1s de los primeros\nen recibir tu laptop. \n\nEs indispensable que al realizar tus pagos ingreses tu referencia personal \n*{REFERENCIA_PAGO}*.  Esto permite al sistema identificarlos de manera autom\u00e1tica."},
                            "FOOTER": {"type": "FOOTER", "text": "Gracias por tu atenci\u00f3n"}}
            pcc_di = copy.deepcopy(pre_component_dic)
            j = 1
            for  index, row in df.iterrows():
                print('\n\n\n-----------',index,row)
                
                header_parameters = []
                pcc_d = copy.deepcopy(pcc_di)
                header_message = pcc_d['HEADER']['text']
               
                
                
                h_formatiado = format_string(pcc_d['HEADER']['text'][:], data=df.iloc[[index]])            
                b_formatiado = format_string(pcc_d['BODY']['text'][:], data=df.iloc[[index]])   
                pcc_d['HEADER']['text'] = h_formatiado
                pcc_d['BODY']['text'] = b_formatiado
                r_d = {'components':[]}
                for x in pcc_d.keys():
                    
                    r_d['components'].append(pcc_d[x])

                print('\n\n',j,h_formatiado)
            
                dm = DatabaseManager('sistemas')


                dm.update_message(message_data={
                    'message': json.dumps(r_d),
                    'phone':str(row['NUMERO_TELEFONO'])
                    
                })
                
                j += 1
                    
                    
                  
                
            return HttpResponse(json.dumps({'status','ok'}),status=200)

        except Exception as e:
            
            print(repr(e))
            return HttpResponse(json.dumps({'status','error'}),status=500)
    return  HttpResponse(json.dumps({'status':'error'}),status=500)