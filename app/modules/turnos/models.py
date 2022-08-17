from app.db import db, BaseModelMixin
   
class Turno(db.Model, BaseModelMixin):
   id = db.Column(db.Integer, primary_key=True)
   fecha_inicio = db.Column(db.DateTime)
   fecha_fin = db.Column(db.DateTime)
   descripcion = db.Column(db.String)

   def __repr__(self):
      return f'Turno({self.id})'

   def __str__(self):
      return """
            id = {0}
            fecha_inicio = {1}
            fecha_fin = {2}
            """.format(self.id, self.fecha_inicio, self.fecha_fin)
