from flask import Blueprint
from database.models import Caja

caja = Blueprint('caja', __name__)

@caja.route('/cajas')
def get_caja():
   Caja.query.all()
   return CajaSchema.dump(caja)