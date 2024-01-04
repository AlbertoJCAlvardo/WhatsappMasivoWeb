import os
from dotenv import load_dotenv
from django.conf import settings
env_path = os.path.join(settings.BASE_DIR, ".env")
load_dotenv(env_path)

class Settings():
    ORACLE_USER = os.getenv("ORACLE_USER")
    ORACLE_USER_S = os.getenv('ORACLE_USER_S')
    ORACLE_PASSWORD_S = os.getenv('ORACLE_PASSWORD_S')
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
    ORACLE_SERVER = os.getenv("ORACLE_SERVER", "localhost")
    ORACLE_SERVER_S = os.getenv('ORACLE_SERVER_S','localhost')
    ORACLE_PORT = os.getenv("ORACLE_PORT", 1521)
    ORACLE_DB = os.getenv("ORACLE_DB", "test")
    DIALECT = 'oracle'
    SQL_DRIVER = 'cx_oracle'
    DATABASE_URL = "{dialect}+{driver}://{user}:{psw}@{host}:{port}/?service_name={service}".format(  # noqa
        dialect=DIALECT,
        driver=SQL_DRIVER,
        user=ORACLE_USER,
        psw=ORACLE_PASSWORD,
        host=ORACLE_SERVER,
        port=ORACLE_PORT,
        service=ORACLE_DB
    )
    DATABASE_URL_S = "{dialect}+{driver}://{user}:{psw}@{host}:{port}/?service_name={service}".format(  # noqa
        dialect=DIALECT,
        driver=SQL_DRIVER,
        user=ORACLE_USER_S,
        psw=ORACLE_PASSWORD_S,
        host=ORACLE_SERVER_S,
        port=ORACLE_PORT,
        service=ORACLE_DB
    )


    def ps(self):
        print( os.path.join(settings.BASE_DIR, ".env"))
settings = Settings()