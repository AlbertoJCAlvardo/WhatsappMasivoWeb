from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
import json
from core.utils import validate_session, validate_user
from core.formatter import Formatter
from django.views.decorators.csrf import csrf_exempt
from core.utils import send_message
from core.config import settings
from heyoo import WhatsApp
import pandas as pd
import asyncio
import random
# Create your views here.


@csrf_exempt
def initial_page(request):
    try:
        
        if request.method == 'GET':
            sesion_id = request.GET.get('sesion_id', None)
            user = request.GET.get('user', None)
            #if validate_session(sesion_id) and validate_user(user):
            if True:
                context = {'user':user, 
                           'sesion_id':sesion_id,
                           'headers':None,
                           'content':None
                           }
                return HttpResponse(render_to_string('data_upload_index.html',
                                                     context=context))
        elif request.method == 'POST':
            sesion_id = request.POST.get('sesion_id', None)
            user = request.POST.get('user', None)
            #if validate_user(user) amd validate_session(session_id):
            
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

                content = df.values

                filename = str(ar)

                
                
               


                if len(content) > 10:
                    footer = f"Ejemplo demostrativo, 10 celdas de {len(content)}"
                    content = df.iloc[0:10].values
                    
                if True:
                        print(df.to_json())
                        context = {'user':user,
                                    'sesion_id':sesion_id, 
                                    'filename':filename,
                                    'footer':footer,
                                    'headers':df.columns.to_list(),
                                    'content':content,
                                    'df':df.to_json()
                                }
                        return HttpResponse(render_to_string('data_upload_index.html',
                                                            context=context))
        context = {'user':user,
                                    'sesion_id':sesion_id, 
                                    'filename':filename,
                                    'footer':footer,
                                    'headers':None,
                                    'content':None,
                                    'df':None
                                }
        return HttpResponse(render_to_string('data_upload_index.html',
                                                            context=context))    
            
       
    except Exception as e:
        return HttpResponseBadRequest(f'{repr(e)}')
    
@csrf_exempt
def message_sending(request):
     
    try:
        if request.method == 'POST':
            filename = request.POST.get('filename', None)
            df = request.POST.get('df', None)
            if df is not None:
                
                df = pd.read_json(df)
                
                df.head()
                index = random.randint(0, df.iloc[:,[0]].size-1)
            context = {'user':None,
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
            print(df.iloc[0])
            formatter = Formatter()
            formatted_message = formatter.format_string(message, df.iloc[0])
            print(formatted_message)
            return JsonResponse(data={'message':formatted_message},
                                status=200)


    except Exception as e:
        print(repr(e))
        return JsonResponse(data={message:"error"},
                                status=400)

@csrf_exempt
def send_messages(request):
    try:

        if request.method == "POST":
        
            body = json.loads(request.body.decode('utf-8'))
            message = body['message']
            df = body['df']
            df = pd.read_json(df)
            
            df['NUMERO_TELEFONO'] = df['NUMERO_TELEFONO'].astype(str)
            formatter = Formatter()
            whatsapp = WhatsApp(settings.ACCESS_TOKEN, settings.PHONE_NUMBER)
            numeros_validos, numeros = formatter.format_phone_numbers(df['NUMERO_TELEFONO'])

            
            for index, row in df.iterrows():
                if row['NUMERO_TELEFONO'] in numeros_validos:
                    
                    formatted_message = formatter.format_string(message, row)
                    
                    
                    response = asyncio.run(send_message(formatted_message, 
                                                        numeros[row['NUMERO_TELEFONO']].replace('+', '')))
                    print(response)

            return HttpResponse("Mensajes enviados")
                                                 
    except Exception as e:
        raise(e)