db = "crm"
usuario = "ramaffei"
nombre_bd = "crm"
contrasenia = r"52866Jam"
bd_type = "mysql+pymysql"
host = "45.162.169.65"

SQLALCHEMY_DATABASE_URI = f'{bd_type}://{usuario}:{contrasenia}@{host}/{nombre_bd}'

print(SQLALCHEMY_DATABASE_URI)
