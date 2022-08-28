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

   presupuesto = db.relationship("Presupuesto", lazy='joined', back_populates="turno")
   venta = db.relationship("Venta", lazy='joined', back_populates="turno")
   empleados = db.relationship("TurnoEmpleado", lazy='joined',back_populates="turnos")
   cliente = db.relationship("Cliente", lazy='joined', back_populates="turnos")
   usuario = db.relationship("Usuario", lazy='joined', back_populates="turnos")  

   def __repr__(self):
      return f'Turno({self.id})'

   def __str__(self):
      return """
            id = {0}
            fecha_inicio = {1}
            fecha_fin = {2}
            """.format(self.id, self.fecha_inicio, self.fecha_fin)

"""
MODULO EMPLEADOS
"""
class Empleado(db.Model, BaseModelMixin):
   __tablename__ = 'empleados'
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String(255)) 
   apellido = db.Column(db.String(255))
   mail = db.Column(db.String(255))

   turnos = db.relationship("TurnoEmpleado", lazy='joined', back_populates="empleados")
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
   cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
   usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
   empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))

   turno = db.relationship("Turno", lazy='joined', back_populates="presupuesto")

class Venta(db.Model, BaseModelMixin):
   __tablename__ = 'ventas'
   id = db.Column(db.Integer, primary_key=True)
   fecha = db.Column(db.DateTime)
   cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
   usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
   empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
   presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'))
   #turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'))

   turno = db.relationship("Turno", lazy='joined', back_populates="venta")

   #items

class Items(db.Model, BaseModelMixin):
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
   id = db.Column(db.Integer, primary_key=True)
   presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'))
   item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
   descripcion = db.Column(db.String(255))
   cantidad = db.Column(db.Integer)
   bon_gan = db.Column(db.Float)
   precio = db.Column(db.Float)

   presupuesto = db.relationship("Presupuesto", lazy='joined', backref="items")

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

   empleados = db.relationship("Empleado", lazy='joined', back_populates="turnos")
   turnos = db.relationship("Turno", lazy='joined', back_populates="empleados")

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

   

