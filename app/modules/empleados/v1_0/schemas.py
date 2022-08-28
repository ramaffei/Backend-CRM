from inspect import Attribute
from marshmallow import fields, EXCLUDE
from app.ext import ma

class EmpleadoSchema(ma.Schema):
   horarios = fields.Nested('HorarioSchema', many = True)
   class Meta:
      fields = ('id','nombre','apellido','mail','turnos','horarios')
      unknown = EXCLUDE
      ordered = True

class HorarioSchema(ma.Schema):
   empleado = fields.Nested('EmpleadoSchema', exclude=('horarios','turnos'))
   #horario_id = fields.Int(attribute = 'id')
   class Meta:
      fields = ('horario_id','dia','hora_entrada','hora_salida', 'empleado')
      unknown = EXCLUDE
      #ordered = True