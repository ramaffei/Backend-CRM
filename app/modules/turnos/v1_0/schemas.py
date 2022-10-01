from datetime import datetime, timedelta
from marshmallow import fields, EXCLUDE, validates, validates_schema, ValidationError
from app.ext import ma
from app.modules.empleados.v1_0.schemas import EmpleadoSchema

class TurnoSchema(ma.Schema):
   empleados = fields.Nested(EmpleadoSchema, many=True,  exclude=('horarios',))
   fecha_inicio = fields.DateTime()
   fecha_fin = fields.DateTime()
   class Meta:
      fields = ('id','fecha_inicio','fecha_fin','descripcion','presupuesto_id','venta_id','cliente_id','estado_turno','usuario_id','presupuesto','venta','empleados','cliente','usuario')
      unknown = EXCLUDE
      ordered = True

   @validates("fecha_inicio")
   def validar_fechaInicio(self, value):
      if value < datetime.now():
         raise ValidationError("La fecha no puede ser anterior a la fecha actual")
   
   @validates_schema
   def validate_numbers(self, data, **kwargs):
        if data["fecha_fin"] <= data["fecha_inicio"]:
            raise ValidationError("La fecha de fin de no puede ser igual o mayor a la fecha de inicio")

class TurnoEmpleadoSchema(ma.Schema):
   empleado = fields.Nested('EmpleadoSchema')
   class Meta:
      fields = ('id','id_empleado','empleado')
      unknown = EXCLUDE
      ordered = True