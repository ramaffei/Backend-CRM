from inspect import Attribute
from marshmallow import fields, EXCLUDE, post_load
from app.ext import ma
from app.modules.models import Empleado
#from app.modules.turnos.v1_0.schemas import TurnoSchema

class EmpleadoSchema(ma.Schema):
   horarios = fields.Nested('HorarioSchema', many = True, exclude=('empleado', ))
   #turnos = fields.Nested('TurnoSchema', many=True)
   class Meta:
      fields = ('id','nombre','apellido','mail','horarios')
      unknown = EXCLUDE
      ordered = True
   
class HorarioSchema(ma.Schema):
   empleado = fields.Nested('EmpleadoSchema', exclude=('horarios',))
   horario_id = fields.Int(attribute = 'id')
   class Meta:
      fields = ('horario_id','dia','hora_entrada','hora_salida', 'empleado')
      unknown = EXCLUDE
      ordered = True
