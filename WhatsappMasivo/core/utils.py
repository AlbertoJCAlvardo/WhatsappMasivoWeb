from db.utils import DatabaseManager
from .config import settings
from datetime import datetime
import aiohttp
import json
import pandas as pd
import pytz
import numpy as np
import base64
import chardet
from PIL import Image
import requests 
import io
from math import isnan

def format_number(number):
    print(f'{number}, {type(number)}')
    if not isnan(number):
        return f'{int(number)}'
    return ''



def validate_session(session_id)->bool:
    try:
        print('dbuser = sistemas')
        do = DatabaseManager('sistemas')
        
        print(session_id)
        query =f"""
                    SELECT count(*) no_sesiones
                    FROM  SYS.V_$session
                    WHERE sid||audsid = '{str(session_id)}' 
                """
        data = do.execute_indexed_query(query)
        print(data)
        if data["NO_SESIONES"][0] == "0" or data["NO_SESIONES"][0] == "":
            query =f"""
                    select pkg_general.f_sesion() from dual
                """
            data = do.execute_indexed_query(query)
            print(data)


            return False
        return True 
    except Exception as e:
        print(repr(e))
        return False

def validate_user(u:str)->bool:
    

    try:
        query = f"""
                    SELECT nombre,
                        usuario_id
                    FROM CL.cl_sys_usuario
                    WHERE upper(usuario_id) = upper('{u}')
                
                """
        do = DatabaseManager("sistemas")
        data = do.execute_indexed_query(query)

        if len(data["USUARIO_ID"])>0:
            return True
        return False
    except Exception as e:
        raise Exception
    
def get_user_name(u:str):
    try:
        query = f"""
                    SELECT nombre, usuario_id
                    FROM CL.cl_sys_usuario
                    WHERE upper(usuario_id) = upper('{u}')
                
                """
        do = DatabaseManager("sistemas")
        data = do.execute_indexed_query(query)
        
        return data["NOMBRE"][0]
    except Exception as e:
        print(e)
        raise Exception
    

def get_components(data:pd.DataFrame)-> list:
    return list(data.iloc[0].apply(str).values)

def validate_login(user, password):
    try:

        do =  DatabaseManager('sistemas')
        query = f"""
                    SELECT CONTRASENA
                    FROM CL.CL_SYS_USUARIO
                    WHERE USUARIO_ID = '{user}'
                """
        
        headers, result = do.execute_query(query)
        do = DatabaseManager('sistemas')

        query = f"""
                    SELECT DISTINCT(PROYECTO) AS PROYECTOS
                    FROM CL.CL_SYS_USUARIO_PROYECTO_WA
                    WHERE USUARIO = '{user}'
                """
        
        headers, result2 = do.execute_query(query)
        
        
        if (len(result) == 0 and len(result2) == 0):
            return 'user_not_exist'
        else:
            if len(result2) == 0:
                return 'unauthorized'
            if result[0][0] != password:
                return 'wrong_password'
            
            return 'correct'

    except Exception as e:
        print(e)
        return 'Error'




async def register_template(components, from_number):

    template_name = f'edilar_{datetime.now(pytz.timezone("Mexico/General")).strftime("%y%m%d_%H%M%S")}'

    headers = { "Content-Type":"application/json",
                "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
    
    baid = settings.BUSINESS_ACCOUNT_ID
    if from_number == 'Red Potencia':
        baid = settings.REDPOTENCIA_BUSINESS_ACCOUNT_ID
    

    url = f"https://graph.facebook.com/v18.0/{baid}/message_templates"
    print(url)
    body = {"name": template_name,
            "language": "es",
            "category": "MARKETING",
            "components": components
        }
    
        
    body = json.dumps(body)
    print("body", body)
    try:
        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    
                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])

                        html = await response.text()
                        response = json.loads(html)
                        
                        
                        print(response)
                        return template_name, response
                    
                        
                            
                        
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
                return template_name, {'status':'ERROR DE CONEXION'}
    except Exception as e:
        print(repr(e))
        return template_name, {'status':'ERROR DE CONEXION'}



def to_parameters(params:list):
    dic_list = []
    for i in params:
        aux =  {
            "type":"text",
            "text":i
        }
        dic_list.append(aux)
    return dic_list

async def send_message(number, template_name, components, from_number):
    try:

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
        print('from_number', from_number)
        
        body = {"messaging_product": "whatsapp", 
                "recipient_type": "individual",
                    "to": f"{number}",
                    "type": "template", 
                    "template": { "name": template_name, 
                                "language": { "code": "es" },
                                 "components": components
                    }
                }
       
        body = json.dumps(body)
        phone_number = settings.PHONE_NUMBER
        if from_number == 'Red Potencia':
            phone_number = settings.REDPOTENCIA_PHONE_NUMBER_ID
            print(phone_number)
        
        async with aiohttp.ClientSession() as session:
            url = f"https://graph.facebook.com/v18.0/{phone_number}/messages"
            print(url)
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    html = await response.text()
                    if response.status == 200:

                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])

                        
                        print("Body:", html)
                        
                        return json.loads(html)
                    
                    return json.loads(html)
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
                return {'error':repr(e)}
        
    except Exception as e:
        return {'error':repr(e)}
 
    
async def check_template_status(template_name):
    headers = { "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
    url = f"https://graph.facebook.com/v18.0/{settings.BUSINESS_ACCOUNT_ID}/message_templates?name={template_name}"
    
    try:
        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        

                        html = await response.text()

                        response = json.loads(html)
                        print(response)
                        if len(response['data']) > 0 :
                            data = response["data"][0]
                        else:
                            print(response['data'])
                            data = {'status':'PENDING'}
                            
                        return data["status"]
                    else:
                        print("\n\n\n\nError")
                        print(response)   
                        print("\n\n\n\n")           
                        return None
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
    except Exception as e:
        print(repr(e))
        return "Error"
    
async def remove_rejected_template(template_name):
    headers = { "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
    url = f"https://graph.facebook.com/v18.0/{settings.BUSINESS_ACCOUNT_ID}/message_templates?name={template_name}"

    try:
        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.delete(url, headers=headers) as response:
                    if response.status == 200:
                        

                        html = await response.text()

                        response = json.loads(html)
                        
                        return response
                    else:
                        print("\n\n\n\nError")
                        print(response)   
                        print("\n\n\n\n")           
                        return None
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
    except Exception as e:
        print(repr(e))
        return "Error" 

def print_dic(dic:dict, level=0):
    if level is None:
        level=0
    sa, so = "", ""
    for _ in range(level):
        sa += "   "
    so = sa
    if level != 0:
        sa+="   "
    print(sa+"{")
    
    for i in dic.keys():
        if isinstance(dic[i], dict):
            print(sa,f'"{i}": ')
            print_dic(dic[i], level + 1)
        elif isinstance(dic[i], list):
            print(sa+f'  "{i}": '+'[')
            for j in dic[i]:
                if isinstance(j, dict):
                    
                    print_dic(j, level + 3)
                else:
                    print(sa,f'   "{i}": "',j,'",')
            print(sa+' '+']')
        else:
            print(sa,f'"{i}": "',dic[i],'",')
            
    print(so+"}")

def repr_dic(dic:dict, level=0):
    dic_str = ""

    if level is None:
        level=0
    sa, so = "", ""
    for _ in range(level):
        sa += "  "
    so = sa
    if level != 0:
        sa+=" "
    dic_str += sa+"{"
    
    for i in dic.keys():
        if isinstance(dic[i], dict):
            dic_str += f'{sa}"{i}": '
            dic_str += '\n'+sa+repr_dic(dic[i], level + 1) + '\n'
        elif isinstance(dic[i], list):
            dic_str+= sa+f'  "{i}": [\n'
            for j in dic[i]:
                if isinstance(j, dict):
                    dic_str += '\n'+repr_dic(j, level + 3) + "\n"
                else:
                    dic_str += f'{sa} "{i}": "{j}",\n'
            dic_str + sa+']\n'
        else:
            dic_str += f'\n{sa}  "{i}": "{dic[i]}",\n'
            
    dic_str += so+"}"
    return dic_str

def convert_query_dict(headers, data)-> list:
    dic_list = []
    for row in data:
        dic  = {}
        
        for i, header in enumerate(headers):
            if header == 'CONTENIDO' and isinstance(row[i], str):
                if len(row[i]) > 0:
                    if row[i][0] == '{':
                        dic[header] = json.loads(row[i])
                    else:
                     dic[header] = row[i]

                else:
                    dic[header] = row[i]
            else:
                    dic[header] = row[i]
            
        dic_list.append(dic)
    
    return dic_list

async def get_image_url(id):
    headers = { "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
    url = f"https://graph.facebook.com/v18.0/{id}"

    try:
        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        

                        html = await response.text()
                    
                        response = json.loads(html)
                        
                        return response
                    else:
                        print("\n\n\n\nError")
                        print(response)   
                        print("\n\n\n\n")           
                        return None
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
    except Exception as e:
        print(repr(e))
        return "Error" 
    
async def get_image_from_url(url):
    headers = { "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
    

    try:
        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        

                        bytes = await response.read()
        
                        
                        image = io.BytesIO(bytes)
                        return base64.b64encode(image.read()).decode()
                    else:
                                
                        return 404
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
    except Exception as e:
        print(repr(e))
        return "Error" 
    

async def send_text_mesage_api(body, phone_number, destiny):
    try:
        phone_number_id = ""
        print(body)
        if '521'+phone_number == settings.PHONE_NUMBER:
            phone_number_id  = settings.EDILAR_PHONE_NUMBER_ID
        if '521' + phone_number == settings.REDPOTENCIA_PHONE_NUMBER:
            phone_number_id  = settings.REDPOTENCIA_PHONE_NUMBER_ID

      
        headers = {
            f'Authorization': f'Bearer {settings.ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        print(headers)
        body = {
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': f'{destiny}',
            'type': 'text',
            'preview_url': False,
            'text': {
                
                'body': body
            }
        }

        body = json.dumps(body)
        async with aiohttp.ClientSession() as session:
            url = f'https://graph.facebook.com/v19.0/{phone_number_id}/messages'
            print(url)
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    html = await response.text()
                    if response.status == 200:
                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])

                        
                        print("Body:", json.loads(html))
                        
                        return json.loads(html)
                    else:
                        print('\n\nerror: ',html)
                    return json.loads(html)
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
                return {'error':repr(e)}
        
    except Exception as e:
        print(repr(e))
        return 'error'


async def upload_media(media, phone_number):
    try:
        phone_number_id = ""
        if phone_number == 'edilar':
            phone_number_id  = settings.EDILAR_PHONE_NUMBER_ID
        if phone_number == 'redpotencia':
            phone_number_id  = settings.REDPOTENCIA_PHONE_NUMBER_ID

        url = f'https://graph.facebook.com/v18.0/{phone_number_id}/media'
        headers = {
            f'Authorization': 'Bearer {settings.ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }

        body = {
            'file': media['file'],
            'type': media['type'],
            'messaging_product': 'whatsapp'
        }

        async with aiohttp.ClientSession() as session:
            
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    html = await response.text()
                    if response.status == 200:
                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])

                        
                        print("Body:", html)
                        
                        return json.loads(html)
                    
                    return json.loads(html)
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
                return {'error':repr(e)}
        
    except Exception as e:
        pass

async def send_media_mesage(message, phone_number):
    try:
        phone_number_id = ""
        if phone_number == 'edilar':
            phone_number_id  = settings.PHONE_NUMBER
        if phone_number == 'redpotencia':
            phone_number_id  = settings.REDPOTENCIA_PHONE_NUMBER

        url = f'https://graph.facebook.com/v18.0/{phone_number_id}/messages'
        headers = {
            f'Authorization': 'Bearer {settings.ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        body = {
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': '{destiny}',
            'type': message['type'],
            'type': {
                'body': message['media_id']
            }
        }

        body = json.dumps(body)
        async with aiohttp.ClientSession() as session:
            url = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER}/messages"
            print(url)
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    html = await response.text()
                    if response.status == 200:
                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])

                        
                        print("Body:", html)
                        
                        return json.loads(html)
                    
                    return json.loads(html)
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
                return {'error':repr(e)}
        
    except Exception as e:
        print(repr(e))
        return 'error'




async def send_interactive_template(number, template_name, data):
    try:

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
        
        header_data = data['header']
        body_data = data['body']

        components = []
        if len(header_data) > 0:
            components.append({ "type": "header",
                                "parameters": to_parameters(header_data)
                                    })
        
        components.append({
                            "type": "body",
                            "parameters": to_parameters(body_data)
                    })
        body = {}
        body = {
                    "to": f"{number}",
                    "type": "template",
                    "template": {
                        "namespace": f"{template_name}",
                        "language": {
                            "policy": "deterministic",
                            "code": "your-language-and-locale-code"
                        },
                        "name": "your-template-name",
                        "components": [
                            {
                                "type" : "header",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": "replacement_text"
                                    }
                                ]
                           
                            },
                            {
                                "type" : "body",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": "replacement_text"
                                    },
                                    {
                                        "type": "currency",
                                        "currency" : {
                                            "fallback_value": "$100.99",
                                            "code": "USD",
                                            "amount_1000": 100990
                                        }
                                    },
                                    {
                                        "type": "date_time",
                                        "date_time" : {
                                            "fallback_value": "February 25, 1977",
                                            "day_of_week": 5,
                                            "day_of_month": 25,
                                            "year": 1977,
                                            "month": 2,
                                            "hour": 15,
                                            "minute": 33, #OR
                                            "timestamp": 1485470276
                                        }
                                    },
                                    {
                                        ...
                                        # Any additional template parameters
                                    }
                                ] 
                            # end body
                            },

                            # The following part of this code example includes several possible button types, 
                            # not all are required for an interactive message template API call.
                            {
                                "type": "button",
                                "sub_type" : "quick_reply",
                                "index": "0", 
                                "parameters": [
                                    {
                                        "type": "payload",
                                        # Business Developer-defined payload
                                        "payload":"aGlzIHRoaXMgaXMgY29vZHNhc2phZHdpcXdlMGZoIGFTIEZISUQgV1FEV0RT"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type" : "url",
                                "index": "1", 
                                "parameters": [
                                    {
                                        "type": "text",
                                        # Business Developer-defined dynamic URL suffix
                                        "text": "9rwnB8RbYmPF5t2Mn09x4h"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type" : "url",
                                "index": "2",
                                "parameters": [
                                    {                    
                                        "type": "text",
                                        # Business Developer-defined dynamic URL suffix
                                        "text": "ticket.pdf"
                                    }
                                ]
                            }
                        ]
                    }
                }
        
        
       
        body = json.dumps(body)
        print(body)
        async with aiohttp.ClientSession() as session:
            url = f"https://graph.facebook.com/v18.0/{settings.PHONE_NUMBER}/messages"
            print(url)
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    html = await response.text()
                    if response.status == 200:
                        print("Status:", response.status)
                        print("Content-type:", response.headers["content-type"])

                        
                        print("Body:", html)
                        
                        return json.loads(html)
                    
                    return json.loads(html)
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", str(e))
                return {'error':repr(e)}
        
    except Exception as e:
        return {'error':repr(e)}



async def get_upload_permission(file_data):
    try:
        url_upload = f"https://graph.facebook.com/v19.0/{settings.APP_ID}/uploads"
        url_upload += f'?file_length={file_data["length"]}&file_type={file_data["mime"]}&access_token={settings.ACCESS_TOKEN}'
        print(url_upload)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url_upload) as response:
                    html = await response.text()
                    print(html)
                    if response.status == 200:

                        body = json.loads(html)
                        upload_id = body['id']

                        return {'status':'ok',
                                'id':upload_id}

                
                        
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", repr(e))
                return {'status':'error', 'error':repr(e)}
        


        
    except Exception as e:
        print(repr(e))
        return {'error':repr(e)}

async def upload_file_api(upload_id, file_data):

    try:
        
        async with aiohttp.ClientSession() as session:
            try:
                
                url = f"https://graph.facebook.com/v18.0/{upload_id}"
                print(url)
                headers = {
                    "file_offset": "application/json",
                    "Authorization": f"OAuth {settings.ACCESS_TOKEN}"
                }
                
                async with session.post(url, headers=headers, data=file_data['data']) as response:
                    html = await response.text()
                    print('\n\n--Respuesta file api', html)
                    if response.status == 200:
                        r_data = json.loads(html)
                        print(repr_dic(r_data))
                        return r_data['h']
                        
                
                        
                         
            except aiohttp.ClientConnectorError as e:
                
                print("Connection Error", repr(e))
                return {'status':'error', 'error':repr(e)}
        


        
    except Exception as e:
        print(repr(e))
        return {'status':'error', 'error':repr(e)}

async def upload_file_api_2(file_data, from_number):

    try:
        
        async with aiohttp.ClientSession() as session:
            try:
                phone_number = settings.EDILAR_PHONE_NUMBER_ID
                if from_number == 'Red Potencia':
                    phone_number = settings.REDPOTENCIA_PHONE_NUMBER_ID

                url = f"https://graph.facebook.com/v18.0/{phone_number}/media"
                print(url)

                data = {
                    'file':str(file_data['data']),
                    'type':file_data['mime']
                }
               
                dt =file_data['data'] 
                headers = {
                    "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
                }
                files ={
                        'file': (file_data['name'], dt, file_data['mime'], {'Expires': '0'}),
                    }
                data = {
                     'messaging_product':(None, 'whatsapp'),
                        'type': (None, file_data['mime'])
                }
                
                response = requests.post(url, headers=headers, files=files, data=data)
                print('\n\n\n--',response.text)
                
                return response.text
                
                        
                         
            except aiohttp.ClientConnectorError as e:
                print("Connection Error", repr(e))
                return {'status':'error', 'error':repr(e)}
        


        
    except Exception as e:
        print(repr(e))
        return {'status':'error', 'error':repr(e)}    
    
def get_user_projects(user):
    dm = DatabaseManager('sistemas')

    query = f"""
                SELECT DISTINCT(PROYECTO) AS PROYECTOS
                FROM CL.CL_SYS_USUARIO_PROYECTO_WA
                WHERE USUARIO = '{user}'
                """
   
    headers, data = dm.execute_query(query)
    print(data)
    return data[0]


def format_project_names(projects:list):
    result = []
    for i in projects:
        if i == "EDILAR":
            result.append('Edilar')
            continue
        if i == "REDPOTENCIA":
            result.append('Red Potencia')
            continue
        if i == 'CORREO_DEL_MAESTRO':
            result.append('Correo Del Maestro')
            continue
        else:
            result.append(i)

    return result
def get_phone_number(project):
    
    if project == 'Edilar':
        return settings.PHONE_NUMBER
    if project == 'Red Potencia':
        return settings.REDPOTENCIA_PHONE_NUMBER