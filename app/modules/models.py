from app.db import db, BaseModelMixin
from sqlalchemy.ext.associationproxy import association_proxy

"""
MODULO TURNO.
"""   
class Turno(db.Model, BaseModelMixin):
   __tablename__ = 'turnos'
   id = db.Column(db.Integer, primary_key=True)
   fecha_inicio = db.Column(db.DateTime)
   fecha_fin = db.Column(db.DateTime)
   descripcion = db.Column(db.String(255))
   presupuesto_id = db.Column(db.Integer, db.ForeignKey("presupuestos.id"))
   venta_id = db.Column(db.Integer, db.ForeignKey("ventas.id"))
   cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
   estado_turno = db.Column(db.String(255))
   usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

   presupuesto = db.relationship("Presupuesto", lazy='joined',backref='turnos')
   venta = db.relationship("Venta", lazy='joined',backref='turnos')
   cliente = db.relationship("Cliente", lazy='joined', back_populates="turnos")
   usuario = db.relationship("Usuario", lazy='joined', back_populates="turnos")

   empleados = association_proxy("turno_empleado", "empleado")  

   def __repr__(self):
      return f'Turno({self.id})'

   def __str__(self):
      string = ''
      for k, v in self.__dict__.items():
         string += f'{k} = {v}\n'
      return string

"""
MODULO EMPLEADOS
"""
class Empleado(db.Model, BaseModelMixin):
   __tablename__ = 'empleados'
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(255)) 
   apellido = db.Column(db.String(255))
   mail = db.Column(db.String(255))

   turnos = association_proxy("turno_empleado", "turno")
   horarios = db.relationship("Horario", lazy='joined', back_populates="empleado")

class Horario(db.Model, BaseModelMixin):
   __tablename__ = 'horarios'
   id = db.Column(db.Integer, primary_key=True)
   dia = db.Column(db.String(10))
   hora_entrada = db.Column(db.String(5))
   hora_salida = db.Column(db.String(5))
   empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))

   empleado = db.relationship("Empleado", lazy='joined', back_populates="horarios")
   __table_args__ = (db.UniqueConstraint('dia', 'empleado_id', name='_dia_empleado'),)
   
""" class DiaTrabajado(db.Model, BaseModelMixin):
   __tablename__ = 'dias_trabajados'
   id = db.Column(db.Integer, primary_key=True)
   fecha_inicio = db.Column(db.DateTime)
   fecha_fin = db.Column(db.DateTime)
   empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
   
   empleado = db.relationship("Empleado", back_populates="horarios")  

   def __repr__(self):
      return f'Horario({self.id})'

   def __str__(self):
      return f'Inicio: {self.fecha_inicio} Fin:{self.fecha_fin}'
 """
"""
MODULO VENTAS
"""
class Presupuesto(db.Model, BaseModelMixin):
   __tablename__ = 'presupuestos'
   id = db.Column(db.Integer, primary_key=True)
   fecha = db.Column(db.DateTime)
   total_importe = db.Column(db.Float)
   cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
   usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
   empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))

   #turno = db.relationship("Turno", lazy='joined', back_populates="presupuesto")
   cliente = db.relationship("Cliente", lazy='joined')
   usuario = db.relationship("Usuario", lazy='joined')
   empleado = db.relationship("Empleado", lazy='joined')

   items = db.relationship("ItemPresupuesto", cascade="all, delete-orphan", lazy='joined', backref="presupuesto")

class Venta(db.Model, BaseModelMixin):
   __tablename__ = 'ventas'
   id = db.Column(db.Integer, primary_key=True)
   fecha = db.Column(db.DateTime)
   total_importe = db.Column(db.Float)
   cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
   usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
   empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
   presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'))

   cliente = db.relationship("Cliente", lazy='joined')
   usuario = db.relationship("Usuario", lazy='joined')
   empleado = db.relationship("Empleado", lazy='joined')
   presupuesto = db.relationship("Presupuesto", lazy='joined', backref="venta")

   #items

class Item(db.Model, BaseModelMixin):
   __tablename__ = 'items'
   id = db.Column(db.Integer, primary_key=True)
   descripcion = db.Column(db.String(255))
   precio_costo = db.Column(db.Float)
   precio_venta = db.Column(db.Float)
   ganancia = db.Column(db.Float)
   impuesto = db.Column(db.Float)
   
   #Categoria

"""
RELACION ITEM/PRESUPUESTO: MUCHOS A MUCHOS, UN PRESUPUESTO PUEDE TENER MUCHOS ITEMS Y UN ITEM PUEDE ESTAR EN VARIOS PRESUPUESTOS
"""

class ItemPresupuesto(db.Model, BaseModelMixin):
   __tablename__ = 'items_presupuestos'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'))
   item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
   descripcion = db.Column(db.String(255), nullable = False)
   cantidad = db.Column(db.Integer, nullable = False)
   bon_gan = db.Column(db.Float, nullable = False)
   precio = db.Column(db.Float, nullable = False)

   def __init__(self, item = {}, descripcion = None, cantidad = None, bon_gan = None, precio = None, **kwargs):
      self.descripcion = descripcion or item.descripcion
      self.precio = precio or item.precio_venta
      self.cantidad = cantidad or 1
      self.bon_gan = bon_gan or 0.00
      self.item = item or None
   
   item = db.relationship(Item, lazy="joined")

"""
RELACION ITEM/VENTA: MUCHOS A MUCHOS, UN PRESUPUESTO PUEDE TENER MUCHOS ITEMS Y UN ITEM PUEDE ESTAR EN VARIOS PRESUPUESTOS
"""

class ItemVenta(db.Model, BaseModelMixin):
   __tablename__ = 'item_ventas'
   id = db.Column(db.Integer, primary_key=True)
   venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'))
   item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
   descripcion = db.Column(db.String(255))
   cantidad = db.Column(db.Integer)
   bon_gan = db.Column(db.Float)
   precio = db.Column(db.Float)

   venta = db.relationship("Venta", lazy='joined', backref="items")

"""
RELACION: TURNOS/EMPLEADOS, MUCHOS A MUCHOS (UN EMPLEADO PUEDE TENER MUCHOS TURNOS ASIGNADOS Y UN TURNO PUEDE TENER MUCHOS EMPLEADOS)
"""
class TurnoEmpleado(db.Model, BaseModelMixin):
   __tablename__ = 'turnos_empleados'

   id = db.Column(db.Integer, primary_key = True)
   id_turno = db.Column(db.ForeignKey('turnos.id'))
   id_empleado = db.Column(db.ForeignKey('empleados.id'))

   #empleado = db.relationship("Empleado", lazy='joined')
   empleado = db.relationship('Empleado', backref="turno_empleado", lazy='joined')
   #turnos = db.relationship("Turno", lazy='joined', back_populates = 'turno_empleado')
   turno = db.relationship('Turno', backref="turno_empleado",lazy='joined')

"""
MODULO CLIENTE.
"""   
class Cliente(db.Model, BaseModelMixin):
   __tablename__ = 'clientes'
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(255)) 
   apellido = db.Column(db.String(255))
   mail = db.Column(db.String(255))
   fecha_nac = db.Column(db.String(255)) 
   telefono = db.Column(db.String(255))
   facebook = db.Column(db.String(255))
   instagram = db.Column(db.String(255))
   twitter = db.Column(db.String(255))

   turnos = db.relationship("Turno", lazy='joined', back_populates="cliente")

"""
MODULO USUARIO.
"""
class Usuario(db.Model, BaseModelMixin):
   __tablename__ = 'usuarios'
   id = db.Column(db.Integer, primary_key = True)
   empleado_id = db.Column(db.Integer, db.ForeignKey("empleados.id"))
   permiso_id = db.Column(db.Integer, db.ForeignKey('permisos.id'))

   empleado = db.relationship('Empleado')
   turnos = db.relationship("Turno", lazy='joined', back_populates="usuario")

class Permiso(db.Model, BaseModelMixin):
   __tablename__ = 'permisos'
   id = db.Column(db.Integer, primary_key = True)
   modificar = db.Column(db.Integer)

   

