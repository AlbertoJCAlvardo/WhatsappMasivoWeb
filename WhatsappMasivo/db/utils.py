from sqlalchemy import create_engine
from sqlalchemy.orm import  Session
from datetime import datetime
from core.format import set_format,set_upper_format
from core.config import settings

class DatabaseManager:
    

    def __init__(self,user=None):    
        
        print
        if user=='sistemas':
          self.DATABASE_URL = settings.DATABASE_URL_S
        else:
            self.DATABASE_URL = settings.DATABASE_URL

    def insert_message_response(self, message_data):
        try:
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()
            

            
            rfc = 'NULL'
            if message_data['destiny'] == settings.PHONE_NUMBER:
                query = f"""
                            SELECT  FACILIDAD_COBRANZA_RFC
                            FROM CL.WHATSAPP_COMUNICATE
                            WHERE DESTINO LIKE '%{message_data['origin']}%'
                         """
                headers, data = self.execute_query(query)
                rfc = f"'{data[0][0]}'"
                print('rfc obtenido')
            query = f"""
                    INSERT INTO 
                    CL.WHATSAPP_MASIVO_RESPUESTA 
                    (FECHA, ORIGEN, DESTINO, WAMID, CONVERSATION_ID, TIPO, CONTENIDO, USUARIO, STATUS, PROFILE_NAME, FACILIDAD_COBRANZA_RFC)

                    VALUES (TO_DATE('{message_data['date']}', 'RRRR-MM-DD hh24:mi:ss'), '{message_data["origin"]}',
                        '{message_data['destiny']}', '{message_data['wamid']}', '{message_data['conversation_id']}', 
                        '{message_data['message_type']}', '{message_data['content']}', '{message_data['user']}', 'unread', '{message_data['name']}', {rfc})
                """
            print(query)
            result = database.execute(query)
            
        except Exception as e:
            print(repr(e))

    
    
    def insert_message_registry(self, message_data):
        try:
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()
           
            rfc = 'NULL'
            if rfc in message_data.keys():
                rfc = f"'{message_data['rfc']}'"    

            query = f"""
                        INSERT INTO 
                        CL.WHATSAPP_COMUNICATE
                        (FECHA, USUARIO, DESTINO, MENSAJE, STATUS_ENVIO, TIPO_MENSAJE, NOMBRE_MENSAJE, ORIGEN, WAMID, CONTENIDO, TIPO, FACILIDAD_COBRANZA_RFC)
                        
                        VALUES (TO_DATE('{message_data['date']}', 'RRRR-MM-DD hh24:mi:ss'), '{message_data["user"]}',
                          '{message_data['destiny']}', '{message_data['message']}', '{message_data['status_envio']}', 
                          '{message_data['type']}', '{message_data['message_name']}', '{message_data['origin']}', '{message_data['wamid']}',
                          '{message_data['content']}', '{message_data['tipo']}',  {rfc})
                    """
            
            result = database.execute(query)

            

        except Exception as e:
            raise(e)

    def update_message_status(self, message_data):
        database = create_engine(self.DATABASE_URL)
        connection = database.connect(database.url)

        if connection.closed:
            connection.connect()
        
        try:

            query = f""" 
                        UPDATE CL.WHATSAPP_COMUNICATE 
                        SET STATUS_MENSAJE = '{message_data['status']}',
                            CONVERSATION_ID = '{message_data['conversation_id']}'
                        WHERE WAMID = '{message_data['wamid']}'
                    """
            result = database.execute(query)

            with Session(database) as session:
                session.commit()

        except Exception as e:
            print(repr(e))

    def update_message_error(self, message_data):
        database = create_engine(self.DATABASE_URL)
        connection = database.connect(database.url)

        if connection.closed:
            connection.connect()
        
        try:

            query = f""" 
                        UPDATE CL.WHATSAPP_COMUNICATE 
                        SET FALLO_META = '{message_data['error_info']}',
                            CODIGO_FALLO_META = '{message_data['error_code']}'
                        WHERE WAMID = '{message_data['wamid']}'
                    """
            result = database.execute(query)
            

            with Session(database) as session:
                session.commit()

        except Exception as e:
            print(repr(e))

    def check_db_connected(self):
        try:
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()

            print('Database connected succesfully')

        except Exception as e:
            print('Error; traceback >')
            raise e
        
    def check_db_disconnected(self):
        try:
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if not connection.closed:
                try:
                    connection.close()
                except:
                    pass

            print('Database disconnected succesfully')
        except Exception as e:
            raise e

 

    
    
    def execute_query(self,query):
        try:
            
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()

        
            with connection.connect() as cn:
                start_tipe = datetime.now()
                results = cn.execute(query)
                headers = list(
                            map(lambda item: set_upper_format(item),results.keys())        
                        )
            
                data = []

                index = 1
                    
                for row in results:
                    
                    try:
                        row_item = list(
                                    map(lambda item: set_format(item), row._mapping.values())
                                )
                        data.append(row_item)
                    except Exception as e:
                        print('traceback ', index, ': >',e)
                        pass

                    index += 1
                cn.close()

                return headers, data

        except Exception as e:
            print('Error')
            raise e
    
    def execute_indexed_query(self,query:str)->dict:

        dic = {}
        try:
            
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()

            
        
            with connection.connect() as cn:
                start_tipe = datetime.now()
                results = cn.execute(query)
                headers = list(
                            map(lambda item: set_upper_format(item),results.keys())        
                        )
            
                data = []

                index = 1
                    
                for row in results:
                    try:
                        row_item = list(
                                    map(lambda item: set_format(item), row._mapping.values())
                                )
                        data.append(row_item)
                    except Exception as e:
                        print('traceback ', index, ': >',e)
                        pass

                    index += 1
                cn.close()
                

                for i in range(len(headers)):
                    ls = []                    
                    for j in range(len(data)):
                        ls.append(data[j][i])
                
                    dic[headers[i]] = ls 
                
                return dic

        except Exception as e:
            print('Error')
            raise e

    def update_seen_status(self, phone_number, user, from_number):
        database = create_engine(self.DATABASE_URL)
        connection = database.connect(database.url)

        if connection.closed:
            connection.connect()
        
        if len(phone_number) == 12:
            phone_number = phone_number[0:2] + '1' + phone_number[2:12]

        try:

            query = f"""UPDATE CL.WHATSAPP_MASIVO_RESPUESTA
                        SET STATUS = 'seen'
                           
                        WHERE STATUS = 'unread'
                        AND  ORIGEN LIKE '%{phone_number}%' AND USUARIO = '{user}' AND DESTINO = '{from_number}'
                    """
            result = database.execute(query)
            print('en teoria procesado')
            result = database.execute("COMMIT")
        except Exception as e:
            print(repr(e))


           
        
