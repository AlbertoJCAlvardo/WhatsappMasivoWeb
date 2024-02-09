from db.utils import DataObtention
from .config import settings
import aiohttp
import json


def validate_session(session_id:str)->bool:
    do = DataObtention()
    

    query =f"""
                SELECT count(*) no_sesiones
                FROM v$session
                WHERE sid||audsid = '{session_id}' 
            """
    data = do.execute_indexed_query(query)
    

    if data['NO_SESIONES'][0] == '0' or data['NO_SESIONES'][0] == '':
        return False
    return True 

def validate_user(u:str)->bool:
    

    try:
        query = f"""
                    SELECT nombre,
                        usuario_id
                    FROM cl_sys_usuario
                    WHERE upper(usuario_id) = upper('{u}')
                
                """
        do = DataObtention()
        data = do.execute_indexed_query(query)

        if len(data['USUARIO_ID'])>0:
            return True
        return False
    except Exception as e:
        raise Exception
    
def get_user_name(u:str):
    try:
        query = f"""
                    SELECT nombre, usuario_id
                    FROM cl_sys_usuario
                    WHERE upper(usuario_id) = upper('{u}')
                
                """
        do = DataObtention('')
        data = do.execute_indexed_query(query)
        
        return data['NOMBRE'][0]
    except Exception as e:
        print(e)
        raise Exception

async def send_message(message, number):
    try:

        headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
        }
        
        body = {"messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": f"{number}",
                "type": "text",
                "text": {"preview_url": False,
                         "body": message }
                }
        """

        
        body = { "messaging_product": "whatsapp", 
                "to": f"{number}",
                "type": "template", 
                "template": { "name": "pruebaedilar", 
                             "language": { "code": "en_US" } } }
        
        """
       
        body = json.dumps(body)
        print(body)
        async with aiohttp.ClientSession() as session:
            url = 'https://graph.facebook.com' + f"/{settings.VERSION}/{settings.PHONE_NUMBER}/messages"
            try:
                async with session.post(url, data=body, headers=headers) as response:
                    if response.status == 200:
                        print("Status:", response.status)
                        print("Content-type:", response.headers['content-type'])

                        html = await response.text()
                        print("Body:", html)
                        return response
                    else:
                        print('\n\n\n\nError')
                        print(response)   
                        print('\n\n\n\n')           
                        return response
                         
            except aiohttp.ClientConnectorError as e:
                print('Connection Error', str(e))
        
    except Exception as e:
        print('pichula')
        return repr(e)