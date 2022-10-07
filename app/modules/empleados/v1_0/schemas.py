from inspect import Attribute
from marshmallow import fields, EXCLUDE, post_load
from app.ext import BaseSchema
from app.modules.models import Empleado
#from app.modules.turnos.v1_0.schemas import TurnoSchema

class EmpleadoSchema(BaseSchema):
   horarios = fields.Nested('HorarioSchema', many = True, exclude=('empleado', ))
   #turnos = fields.Nested('TurnoSchema', many=True)
   class Meta:
      fields = ('id','nombre','apellido','mail','horarios')
      dump_only = ('id',)
      unknown = EXCLUDE
      ordered = True
class HorarioSchema(BaseSchema):
   empleado = fields.Nested('EmpleadoSchema', exclude=('horarios',))
   horario_id = fields.Int(attribute = 'id')
   class Meta:
      fields = ('horario_id','dia','hora_entrada','hora_salida', 'empleado')
      dump_only = ('horario_id',)
      unknown = EXCLUDE
      ordered = True
