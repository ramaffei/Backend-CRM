db = "patrimonial"
usuario = "patrimonial"
nombre_bd = "patrimonial"
contrasenia = "*4Svu672j"
bd_type = "mysql+pymysql"
host = "190.60.174.157"

SQLALCHEMY_DATABASE_URI = f'{bd_type}://{usuario}:{contrasenia}@{host}/{nombre_bd}'

print(SQLALCHEMY_DATABASE_URI)
