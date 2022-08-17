from app.db import db, BaseModelMixin
   
class Cliente(db.Model, BaseModelMixin):
   id = db.Column(db.Integer, primary_key=True)
   nombre = db.Column(db.String) 
   apellido = db.Column(db.String)
   mail = db.Column(db.String)
   fecha_nac = db.Column(db.String)
   telefono = db.Column(db.String)
   facebook = db.Column(db.String)
   instagram = db.Column(db.String)
   twitter = db.Column(db.String)

   def __repr__(self):
      return f'Film({self.title})'

   def __str__(self):
      return f'{self.title}'

