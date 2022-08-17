BD_TYPE = 'mysql+pymysql'
BD_USER = 'api'
BD_PASSWORD = 'API21Soft13'
BD_HOST = 'localhost'
BD_NAME = 'registros_patrimonial'
SQLALCHEMY_DATABASE_URI = f'{BD_TYPE}://{BD_USER}:{BD_PASSWORD}@{BD_HOST}/{BD_NAME}'
SQLALCHEMY_BINDS = {
   'old': f'{BD_TYPE}://{BD_USER}:{BD_PASSWORD}@{BD_HOST}/patrimonial'
}