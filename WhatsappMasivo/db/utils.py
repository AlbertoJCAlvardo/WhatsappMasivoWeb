from sqlalchemy import (create_engine,insert, update, MetaData, inspect,
                        Column, Integer, Date, String,PrimaryKeyConstraint, text, DateTime)
from sqlalchemy.orm import  Session
from sqlalchemy.ext.declarative import declarative_base

import copy
from datetime import datetime
import time
from core.format import set_format,set_upper_format
from core.config import settings

class DatabaseManager:
    
    Base  = declarative_base()

    def __init__(self,user=None):    
        
        
       

        if user=='sistemas':
            self.DATABASE_URL = settings.DATABASE_URL_S
        else:
            self.DATABASE_URL = settings.DATABASE_URL
     
        self.engine = create_engine(self.DATABASE_URL, echo=True)
        self.metadata = MetaData(bind=self.engine)
        declarative_base().metadata.create_all(self.engine)
    
       
        
    
    
    def print_tables(self):
        tables = self.metadata.tables
        with self.engine.connect(self.engine.url) as conn:
            
            nmetadata = MetaData(bind=self.engine)
            print(nmetadata.reflect(bind=self.engine))
            nmetadata.reflect(self.engine)
            print(nmetadata)
            tables = nmetadata.tables
            for i in tables.keys():
                
                print(i, tables[i])
            conn.close()

        inspector = inspect(self.engine)
        schemas = inspector.get_table_names()
        print(schemas)

    def lazy_insert(self):
        
        stmt = (insert(self.WhatsappComunicate).
                values(fecha = datetime.now(),
                        usuario = 'NULL',
                        destino = 'yyy',
                        mensaje =  'NULL',
                        status_envio =  'NULL',
                        tipo_mensaje = 'NULL',
                        nombre_mensaje =  'NULL',
                        origen = 'NULL',
                        wamid =  'NULL',
                        conversation_id = 'NULL',
                        status_mensaje = 'NULL',
                        contenido =  'NULL',
                        elements =  'NULL',
                        tipo =  'NULL',
                        facilidad_cobranza_rfc = 'NULL',
                        fallo_meta  = 'NULL',
                        codigo_fallo_meta  =  'NULL',
                        respuesta_automatica =  'NULL',
                        body_texto  = 'NULL'))
        print(stmt)
        with self.engine.connect() as connection:
            try:
                connection.execute(stmt)
                print('En teoria se logró xd')
            except Exception as e:
                print(repr(e))
            finally:
                print('Cerrando conexion')
                connection.close()
        
    def update_rfc(self,rfc,phone_number):
        try: 
            with self.engine.connect() as connection:
                try:
                    
                    stmt = (update(self.WhatsappComunicate).
                            where(self.WhatsappComunicate.destino == phone_number).
                            values({'facilidad_cobranza_rfc':rfc}))
                    
                    connection.execute(stmt)

                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()
          
            
                        
                 

        except Exception as e:
            
            print(repr(e))
      
    def insert_message_response(self, message_data):
        try:
            

            with self.engine.connect() as connection:
                try:
                    with Session(self.engine) as session:
                        rfc = None

                        if message_data['destiny'] in (settings.PHONE_NUMBER, settings.CORREO_MAESTRO_PHONE_NUMBER):
                            
                            
                            
                            rfc = (session.query(self.WhatsappComunicate.facilidad_cobranza_rfc,
                                                 ).
                                     filter(self.WhatsappComunicate.destino.ilike(f'%{message_data["origin"]}%')).
                                     first())[0]
                            
                            session.flush()
                       
                        stmt = (insert(self.WhatsappMasivoRespuesta).
                                values( fecha = message_data['date'],
                                        usuario = message_data['user'],
                                        destino = message_data['destiny'],
                                        profile_name = message_data['name'],
                                        origen = message_data['origin'],
                                        wamid = message_data['wamid'],
                                        conversation_id = message_data['conversation_id'],
                                        status= 'unread',
                                        contenido = message_data['content'],
                                        tipo = message_data['message_type'],
                                        facilidad_cobranza_rfc = rfc
                                                                         ))
                      
                        connection.execute(stmt)

                        session.flush()
                        session.commit()
                         
                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()
            
        except Exception as e:
                connection.close()
                print(repr(e))

    
    
    def insert_message_registry(self, message_data):
        try:
            with self.engine.connect() as connection:
                try:
                    with Session(self.engine) as session:
                        

                       

                        stmt = (insert(self.WhatsappComunicate).
                                values( fecha = message_data['date'],
                                        usuario = message_data['user'],
                                        destino = message_data['destiny'],
                                        mensaje = message_data['message'],
                                        status_envio = message_data['status_envio'],
                                        tipo_mensaje = message_data['type'],
                                        nombre_mensaje = message_data['message_name'],
                                        origen = message_data['origin'],
                                        wamid = message_data['wamid'],
                                        contenido = message_data['content'],
                                        tipo = message_data['tipo'],
                                        facilidad_cobranza_rfc = message_data['rfc'],
                                        respuesta_automatica = message_data['automatic_response'],
                                        body_texto = message_data['body_text']
                                      ))
                        
                        connection.execute(stmt)

                        session.flush()
                        session.commit
                         
                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()
        except Exception as e:
            
            raise(e)
    def update_message(self, message_data):
        try:
            
           
            with self.engine.connect() as connection:
                try:
                    
                    stmt = (update(self.WhatsappComunicate).
                            where(self.WhatsappComunicate.destino == '52' + message_data['phone_number']).
                            values({'mensaje':message_data['mensaje']}))
                    
                    connection.execute(stmt)

                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()
        except Exception as e:
            print(repr(e))
            
    def update_message_status(self, message_data):
       
        
        try:

           
            with self.engine.connect() as connection:
                try:
                    
                    stmt = (update(self.WhatsappComunicate).
                            where(self.WhatsappComunicate.wamid == message_data['wamid']).
                            values({'status_mensaje':message_data['status'],
                                    'conversation_id':message_data['conversation_id']}))
                    
                    connection.execute(stmt)

                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()

        except Exception as e:
            connection.close()
            print(repr(e))

    def update_message_error(self, message_data):
        
        try:

           
            with self.engine.connect() as connection:
                try:
                    
                    stmt = (update(self.WhatsappComunicate).
                            where(self.WhatsappComunicate.wamid == message_data['wamid']).
                            values({'fallo_meta':message_data['error_info'],
                                    'codigo_fallo_meta':message_data['error_code']}))
                    
                    connection.execute(stmt)

                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()
        except Exception as e:
            connection.close()
            print(repr(e))

    def check_db_connected(self):
        try:
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()

            print('Database connected succesfully')

        except Exception as e:
            connection.close()
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
                        cn.close()
                        print('traceback ', index, ': >',e)
                        pass

                    index += 1
                

                return headers, data

        except Exception as e:
           
            print('Error')
            raise e
        finally: connection.close()
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
                        cn.close()
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
            connection.close()
            print('Error')
            raise e

    def update_seen_status(self, phone_number, user, from_number):
        
        if len(phone_number) == 12:
            phone_number = phone_number[0:2] + '1' + phone_number[2:12]

        try:

            query = f"""UPDATE CL.WHATSAPP_MASIVO_RESPUESTA
                        SET STATUS = 'seen'
                           
                        WHERE STATUS = 'unread'
                        AND  ORIGEN LIKE '%{phone_number}%' AND USUARIO = '{user}' AND DESTINO = '{from_number}'
                    """
            with self.engine.connect() as connection:
                try:
                    
                    stmt = (update(self.WhatsappMasivoRespuesta).
                            where(self.WhatsappMasivoRespuesta.origen.ilike(phone_number) and 
                                  self.WhatsappMasivoRespuesta.usuario == user and
                                  self.WhatsappMasivoRespuesta.status == 'unread').
                            values({'status': 'seen'}))
                    
                    connection.execute(stmt)

                except Exception as e:
                    print(repr(e))
                finally:
                    connection.close()
        except Exception as e:
            print(repr(e))


    def sanitize_input(user_input):
        output = copy.deepcopy(user_input)
    
        replacements = {
            "'": "''",  # Escapar comillas simples
            ";": "",    # Eliminar punto y coma
            "--": "",   # Eliminar comentarios SQL
            "/*": "",   # Eliminar inicio de comentario de bloque
            "*/": "",   # Eliminar fin de comentario de bloque
            "=": "",    # Eliminar el signo igual
            "\\": "\\\\", # Escapar barra invertida
        }
        for i in replacements.keys():
            output = output.replace(i,replacements[i])

        return output
        
    class WhatsappComunicate(Base):
        __table_args__ = {'schema':'cl',
                          'quote':False}
        __tablename__ = 'WHATSAPP_COMUNICATE'
        
        whatsapp_id = Column(Integer(), primary_key=False)
        fecha = Column(DateTime())
        usuario = Column(String(30))
        destino = Column(String(13))
        mensaje = Column(String(2024))
        status_envio = Column(String(10))
        tipo_mensaje = Column(String(10))
        nombre_mensaje = Column(String(30))
        origen = Column(String(13))
        wamid = Column(String(100))
        conversation_id = Column(String(100))
        status_mensaje = Column(String(10))
        contenido = Column(String(2024))
        elements = Column(String(2024))
        tipo = Column(String(10))
        facilidad_cobranza_rfc = Column(String(30))
        fallo_meta  = Column(String(2024))
        codigo_fallo_meta  = Column(String(10))
        respuesta_automatica = Column(String(254))
        body_texto  = Column(String(2024))

    class WhatsappMasivoRespuesta(Base):
        __table_args__ = {'schema':'cl',
                          'quote':False}
        __tablename__ = 'WHATSAPP_MASIVO_RESPUESTA'
        id_respuesta = Column(Integer(), primary_key=True)
        fecha = Column(DateTime())
        usuario = Column(String(30))
        destino = Column(String(13))
        profile_name = Column(String(30))
        origen = Column(String(13))
        wamid = Column(String(100))
        conversation_id = Column(String(100))
        status= Column(String(10))
        contenido = Column(String(2024))
        tipo = Column(String(10))
        facilidad_cobranza_rfc = Column(String(30))
       