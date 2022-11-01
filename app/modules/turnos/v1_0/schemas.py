from datetime import datetime, timedelta
from marshmallow import fields, EXCLUDE, validates, validates_schema, ValidationError
from app.ext import BaseSchema
from app.modules.clientes.v1_0.schemas import ClienteSchema
from app.modules.empleados.v1_0.schemas import EmpleadoSchema

class TurnoSchema(BaseSchema):
   empleados = fields.Nested(EmpleadoSchema, many=True,  exclude=('horarios', 'turnos'))
   cliente = fields.Nested(ClienteSchema)
   cliente_id = fields.Int(allow_none = True)
   venta_id = fields.Int(allow_none = True)
   presupuesto_id = fields.Int(allow_none = True)
   usuario_id = fields.Int(allow_none = True)
   fecha_inicio = fields.DateTime()
   fecha_fin = fields.DateTime()
   class Meta:
      fields = ('id','fecha_inicio','fecha_fin','descripcion','presupuesto_id','venta_id','cliente_id','estado_turno','usuario_id','empleados','cliente')
      unknown = EXCLUDE
      ordered = True
      dump_only = ("id","empleados", "cliente")
      allow_none = ('cliente_id','venta_id','presupuesto_id','usuario_id')

   @validates("fecha_inicio")
   def validar_fechaInicio(self, value):
      if (value + timedelta(seconds=30)) < datetime.now():
         raise ValidationError("La fecha no puede ser anterior a la fecha actual")
   
   @validates_schema
   def validate_numbers(self, data, **kwargs):
      fecha_fin = data.get('fecha_fin')
      fecha_inicio = data.get('fecha_inicio')
      if (fecha_fin and fecha_inicio) and fecha_fin <= fecha_inicio:
         raise ValidationError("La fecha de fin de no puede ser igual o mayor a la fecha de inicio")

class TurnoEmpleadoSchema(BaseSchema):
   empleado = fields.Nested('EmpleadoSchema',exclude=('turnos',))
   turno = fields.Nested('TurnoSchema', exclude=('empleados',))
   class Meta:
      fields = ('id_empleado','empleado', 'id_turno', 'turno')
      unknown = EXCLUDE
      ordered = True