from app.db import db, BaseModelMixin
   
class Empleado(db.Model, BaseModelMixin):
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String) 
   apellido = db.Column(db.String)
   mail = db.Column(db.String)
   
   def __repr__(self):
      return f'Film({self.title})'
   def __str__(self):
      return f'{self.title}'

class Horario(db.Model, BaseModelMixin):
   id = db.Column(db.Integer, primary_key=True)
   dia = db.Column(db.Date)
   hora_inicio = db.Column(db.DateTime)
   hora_fin = db.Column(db.DateTime)

   def __repr__(self):
      return f'Actor({self.name})'

   def __str__(self):
      return f'{self.name}'

if __name__ == 'main':

   empleado1 = Empleado(nombre = 'Gustavo', apellido = 'Achaval', mail = 'gustavo_achaval@gmail.com')