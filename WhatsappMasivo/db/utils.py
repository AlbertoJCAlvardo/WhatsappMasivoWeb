from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from core.format import set_format,set_upper_format
from core.config import settings

class DataObtention:
    

    def __init__(self,user=None):    
        
        
        if user=='sistemas':
          self.DATABASE_URL = settings.DATABASE_URL_S
        else:
            self.DATABASE_URL = settings.DATABASE_URL
    
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

    def get_total_para_deposito(self,empresa,fecha_inicio,fecha_fin,tipo_de_anticipo):
        try:
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()
            
            ls1 = fecha_inicio.split(' ')
            ls2 = fecha_fin.split(' ')

            fecha_inicio = f'{ls1[0]} {ls1[1]}'
            fecha_fin = f'{ls2[0]} {ls2[1]}'

            query = f"""SELECT (SELECT NOMBRE FROM CL.CM_BANCO WHERE BANCO_ID = BANCO) BANCO,  
                                 NVL (SUM (MONTO), 0) MONTO_DEPOSITO
                         FROM CL.CS_ANTICIPO
                         WHERE FECHA_LIQUIDACION BETWEEN TO_DATE('{fecha_inicio}','DD/MM/YYYY HH:MI:SS') AND TO_DATE('{fecha_fin}','DD/MM/YYYY HH:MI:SS')
                         AND EMPRESA = '{empresa}'
                         AND FORMA_PAGO = 'D'
                         AND ORIGEN = NVL ('{tipo_de_anticipo}', ORIGEN)
                         GROUP BY BANCO
                    """
            
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


    def get_total_para_cheques(self,empresa,fecha_inicio,fecha_fin,tipo_de_anticipo):

        try:
            
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()

            ls1 = fecha_inicio.split(' ')
            ls2 = fecha_fin.split(' ')

            fecha_inicio = f'{ls1[0]} {ls1[1]}'
            fecha_fin = f'{ls2[0]} {ls2[1]}'



            query = f"""SELECT NVL (SUM (MONTO), 0)
                        FROM CL.CS_ANTICIPO
                        WHERE FECHA_LIQUIDACION BETWEEN 
                        TO_DATE('{fecha_inicio}','DD/MM/YYYY HH:MI:SS') AND 
                        TO_DATE('{fecha_fin}','DD/MM/YYYY HH:MI:SS')
                        AND EMPRESA = '{empresa}'

                        AND ORIGEN = NVL ('{tipo_de_anticipo}', ORIGEN)
                        AND FORMA_PAGO = 'C'
                    """
            
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

    def get_empresas(self):

        try:
            
            database = create_engine(self.DATABASE_URL)
            connection = database.connect(database.url)

            if connection.closed:
                connection.connect()

            query = """
                      SELECT DISTINCT CLAVE, NOMBRE
                      FROM   CL.AL_EMPRESAS
                      WHERE  CLAVE IS NOT NULL
                      ORDER BY NOMBRE
                    """
        
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
        
