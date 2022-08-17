from .default import *
from .bd_prod import *

# Configuración del email
MAIL_SERVER = 'smtp.office365.com'
MAIL_PORT = 587
MAIL_USERNAME = 'sitdesarrollos@me.cba.gov.ar'
MAIL_PASSWORD = 'Sinasados.2022'
DONT_REPLY_FROM_EMAIL = 'sitdesarrollos@me.cba.gov.ar'
ADMINS = ('rodrigo.maffei@me.cba.gov.ar','gustavo.villarreal@me.cba.gov.ar' )
MAIL_USE_TLS = True
MAIL_DEBUG = False

APP_ENV = APP_ENV_PRODUCTION
