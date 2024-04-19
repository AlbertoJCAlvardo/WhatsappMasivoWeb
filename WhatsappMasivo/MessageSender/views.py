from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
import json
from core.utils import validate_session, validate_user, get_user_name, validate_login, format_number, repr_dic
from core.formatter import format_string, format_phone_numbers, set_wa_format
from django.views.decorators.csrf import csrf_exempt
from core.utils import (send_message, register_template, get_components, 
                        check_template_status, remove_rejected_template, upload_file_api,
                        get_upload_permission, upload_file_api_2)
from db.utils import DatabaseManager
from core.config import settings
import io
import pandas as pd
import asyncio
import random
from time import sleep, time
from datetime import datetime
import pytz
# Create your views here.

@csrf_exempt
def index(request, **kwargs):
    id = kwargs['id']
    print(id)
    context = {'id': id}
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
           
            db = DatabaseManager('sistemas')
            start = time()
            validation = validate_login(user=user,
                                           password=password)
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
                    
                print(message)
                return HttpResponse(json.dumps({'message':message}))
                
                

        except Exception as e:
            print(repr(e))
            return HttpResponse(json.dumps({'message':'Error en el servidor'}))

@csrf_exempt
def data_upload(request):
    try:
        print(request.method)
        if request.method == 'GET':
            print('hola -.-')
            sesion_id = request.GET.get('session_id', None)
            user = request.GET.get('user', None)
            print(user, sesion_id)
            if validate_session(sesion_id) and validate_user(user):
                print(user)
                context = {'user':user, 
                           'session_id':sesion_id,
                           'user_name':get_user_name(user),
                           'headers':None,
                           'content':None
                          
                           }
                return HttpResponse(render_to_string('data_upload_index.html',
                                                        context=context))
            else:
                print('aaaaaaaaaaaaa')
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
                                        'content':content,
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
            print(user)
            if df is not None:
                
                df = pd.read_json(df)
                
                df.head()
                index = random.randint(0, df.iloc[:,[0]].size-1)
            context = {'user':user,
                       'user_name': get_user_name(user),
                       'filename':filename,
                       'df':df.to_json,
                       'headers':list(df.columns), 
                       'test':df.iloc[index:index+1].to_json}

            return HttpResponse(render_to_string('message_sender_index.html',
                                                 context=context))
        else:
            return HttpResponseRedirect('/data_upload/')
    except Exception as e:
        
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
            message = body['message']
            df = body['df']
            df = pd.read_json(df)

            formatted_header, tokens_header = set_wa_format(message=message['header'], data=df.iloc[0])


            formatted_body, tokens_body = set_wa_format(message=message['body'], data=df.iloc[0])
            



                
            template_name, response =  asyncio.run(register_template({'header':formatted_header,
                                                                      'body':formatted_body,
                                                                      'footer':message['footer']}, 
                                                                      data={'header_data':df[list(tokens_header.keys())],
                                                                            'body_data':df[list(tokens_body.keys())]}))
            if 'error' not in response.keys():
                status = response['status']
               
                for _ in range(50):
                    sleep(2)
                    print('Esperando...')
                    if status != 'PENDING':
                        break
                    
                    status = asyncio.run(check_template_status(template_name=template_name))
                response = {
                    'status':400,
                    'template_name':template_name
                    }                         
                if status == 'APPROVED':
                    response['status'] = 200
                    response['tokens'] = {'tokens_header': tokens_header, 
                                          'tokens_body': tokens_body}
                if status == 'REJECTED':
                    removed = asyncio.run(remove_rejected_template(template_name=template_name))
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
            
            response = {'status':'ERROR', 'error':'Error Desconocido'}
            return HttpResponse(json.dumps(response))

    except Exception as e:
        raise e


@csrf_exempt
def send_messages(request):
    try:
            
        if request.method == "POST":
        
            body = json.loads(request.body.decode('utf-8'))
            print('\n\nenviando...',repr_dic(body))
           
            template_name = body['template_name']
            message_dic = body['message_dic']
            df = body['df']
            df = pd.read_json(df)
            
            message = body['message']
            
            formatted_header, tokens_header = set_wa_format(message=message_dic['header'], data=df.iloc[0])
            formatted_body, tokens_body = set_wa_format(message=message_dic['body'], data=df.iloc[0])

            db = DatabaseManager()
            
            df['NUMERO_TELEFONO'] = df['NUMERO_TELEFONO'].apply(format_number)

            numeros_validos, numeros = format_phone_numbers(df['NUMERO_TELEFONO'])

            counter = 0
            print('\n\n\n\nEnviando mensajes...')
            for index, row in df.iterrows():
                
                if row['NUMERO_TELEFONO'] in numeros_validos:
                    
                    
                    
                    response = asyncio.run(send_message( 
                                                        numeros[row['NUMERO_TELEFONO']].replace('+', ''),
                                                        template_name=template_name, 
                                                        data={'header': list(row.loc[tokens_header.keys()].values),
                                                              'body': list(row.loc[tokens_body.keys()].values)
                                                              }))
                    print('\n\nresponse: \n',repr_dic(response))
                    
                    m_status = 'error'
                    wamid = ''
                    
                    if 'messages' in response.keys():
                        messages = response['messages'][0]

                        if messages['message_status'] == 'accepted':
                            m_status = 'ok'
                            counter += 1
                        wamid = messages['id']
                        
                    r_body = {'body': format_string(message, row)}
                    
                    db.insert_message_registry(message_data={
                        'date':datetime.now(pytz.timezone("Mexico/General")).strftime("%Y-%m-%d %H:%M:%S"),
                        'user':get_user_name(body['user']),
                        'destiny':numeros[row['NUMERO_TELEFONO']].replace('+', ''),
                        'message': json.dumps(r_body),
                        'status_envio':m_status,
                        'type':'template',
                        'message_name':template_name,
                        'origin': settings.WHATSAPP_NUMBER,
                        'wamid':wamid
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
           
            
            ar = request.FILES.get('file', None)
            if request.FILES.get('file') != None:
                
                ar = request.FILES['file']
                data = request.FILES['file'].read()

                extension = str(ar).split('.')[1]
                
                for filename, file in request.FILES.items():
                    nme = request.FILES[filename].name
                    print(file.read())
                    name = filename
                
                mime = ""
                if extension in ("jpeg", 'jpg', 'png'):
                    mime = f'image/{extension}'
                elif extension in ("mp4"):
                    mime = f'video/{extension}'
                else:   
                    mime = f'document/{extension}'
               
                
                file_data = {'mime':mime,
                             'length': len(data),
                             'data': data,
                             'name': nme}
                


                
               #permision = asyncio.run(get_upload_permission(file_data))

                
                response = asyncio.run(upload_file_api_2(file_data ))

                print(response)

                return HttpResponse(json.dumps({'status':'ok', 'response':response}))

            return HttpResponse(json.dumps({'status':'error', 'error':permision.error}))
        except Exception as e:
            print(repr(e))
            return HttpResponse(json.dumps({'status': 'error', 'error':repr(e)}))

@csrf_exempt
def file_test(request):
    context = {}
    return HttpResponse(render_to_string('file_test.html', context=context))