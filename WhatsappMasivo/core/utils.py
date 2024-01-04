from db.utils import DataObtention

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