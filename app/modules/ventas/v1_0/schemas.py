from marshmallow import fields, EXCLUDE
from app.ext import ma
from app.modules.clientes.v1_0.schemas import ClienteSchema
from app.modules.empleados.v1_0.schemas import EmpleadoSchema
from app.modules.turnos.v1_0.schemas import TurnoSchema

class VentaSchema(ma.Schema):
   cliente = fields.Nested(ClienteSchema, exclude=('turnos',))
   #usuario = fields.Nested(UsuarioSchema)
   empleado = fields.Nested(EmpleadoSchema, exclude=('horarios',))
   turnos = fields.Nested(TurnoSchema, many=True, exclude= ('presupuesto_id','venta_id','cliente_id','usuario_id','presupuesto','venta','empleados','cliente','usuario'))
   items = fields.Nested("ItemPresSchema", many=True)
   class Meta:
      fields = ("id","fecha","turnos","cliente","usuario","empleado","items", "total_importe", "cliente_id","empleado_id", "presupuesto_id", "usuario_id")
      load_only = ("cliente_id", "empleado_id", "usuario_id")
      dump_only = ("cliente", "empleado", "turnos", "usuario", "items")
      unknown = EXCLUDE
      ordered = True

class PresupuestoSchema(ma.Schema):
   cliente = fields.Nested(ClienteSchema, exclude=('turnos',))
   #usuario = fields.Nested(UsuarioSchema)
   empleado = fields.Nested(EmpleadoSchema, exclude=('horarios',))
   turnos = fields.Nested(TurnoSchema, many=True, exclude= ('presupuesto_id','venta_id','cliente_id','usuario_id','presupuesto','venta','empleados','cliente','usuario'))
   #venta = fields.Nested(VentaSchema, exclude=('presupuesto',"turno"))
   items = fields.Nested("ItemPresSchema", many=True)
   class Meta:
      fields = ("id","fecha","turnos","cliente","usuario","empleado","items", "total_importe", "cliente_id","empleado_id", "venta_id", "usuario_id")
      load_only = ("cliente_id", "empleado_id", "usuario_id")
      dump_only = ("cliente", "empleado", "turnos", "usuario", "items")
      unknown = EXCLUDE
      ordered = True

class ItemSchema(ma.Schema):
   class Meta:
      fields = ("id","descripcion","precio_costo","precio_venta","ganancia","impuesto", "cantidad", "bon_gan", "precio")
      unknown = EXCLUDE
      ordered = True

class ItemPresSchema(ma.Schema):
   class Meta:
      fields = ("id","item_id","descripcion", "cantidad", "bon_gan", "precio")
      #dump_only = ("id", "item_id")
      unknown = EXCLUDE
      ordered = True