from marshmallow import fields, EXCLUDE
from app.ext import BaseSchema
from app.modules.clientes.v1_0.schemas import ClienteSchema
from app.modules.empleados.v1_0.schemas import EmpleadoSchema
from app.modules.turnos.v1_0.schemas import TurnoSchema

class VentaSchema(BaseSchema):
   cliente = fields.Nested(ClienteSchema)
   #usuario = fields.Nested(UsuarioSchema)
   empleado = fields.Nested(EmpleadoSchema, exclude=('horarios',))
   turnos = fields.Nested(TurnoSchema, many=True, exclude= ('presupuesto_id','venta_id','cliente_id','usuario_id','empleados','cliente'))
   items = fields.Nested("ItemPresSchema", many=True)
   class Meta:
      fields = ("id","fecha","turnos","cliente","usuario","empleado","items", "total_importe", "cliente_id","empleado_id", "presupuesto_id", "usuario_id")
      load_only = ("cliente_id", "empleado_id", "usuario_id")
      dump_only = ("id", "cliente", "empleado", "turnos", "usuario", "items")
      unknown = EXCLUDE
      ordered = True
      allow_none = ('total_importe','cliente_id','empleado_id','presupuesto_id','usuario_id')

class PresupuestoSchema(BaseSchema):
   cliente = fields.Nested(ClienteSchema)
   #usuario = fields.Nested(UsuarioSchema)
   empleado = fields.Nested(EmpleadoSchema, exclude=('horarios',))
   turnos = fields.Nested(TurnoSchema, many=True, exclude= ('presupuesto_id','venta_id','cliente_id','usuario_id','empleados','cliente'))
   #venta = fields.Nested(VentaSchema, exclude=('presupuesto',"turno"))
   items = fields.Nested("ItemPresSchema", many=True)
   class Meta:
      fields = ("id","fecha","turnos","cliente","usuario","empleado","items", "total_importe", "cliente_id","empleado_id", "venta_id", "usuario_id")
      load_only = ("cliente_id", "empleado_id", "usuario_id")
      dump_only = ("id", "cliente", "empleado", "turnos", "usuario", "items")
      unknown = EXCLUDE
      ordered = True
      allow_none = ('total_importe','cliente_id','empleado_id','presupuesto_id','usuario_id')

class ItemSchema(BaseSchema):
   item_id = fields.Int(attribute = 'id')
   class Meta:
      fields = ("item_id","descripcion","precio_costo","precio_venta","ganancia","impuesto", "cantidad", "bon_gan", "precio")
      unknown = EXCLUDE
      ordered = True
      dump_only = ("item_id",)
      allow_none = ("impuesto","bon_gan","precio","precio_costo","precio_venta","ganancia")

class ItemPresSchema(BaseSchema):
   class Meta:
      fields = ("id","item_id","descripcion", "cantidad", "bon_gan", "precio")
      #dump_only = ("id", "item_id")
      unknown = EXCLUDE
      ordered = True
      dump_only = ("id",)
      allow_none = ('item_id', 'bon_gan')