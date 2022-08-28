from marshmallow import fields, EXCLUDE
from app.ext import ma

class ClienteSchema(ma.Schema):
   class Meta:
      fields = ('id','nombre','apellido','mail','fecha_nac','telefono','facebook','instagram','twitter','turnos')
      unknown = EXCLUDE
      ordered = True