from marshmallow import fields, EXCLUDE
from app.ext import BaseSchema

class ClienteSchema(BaseSchema):
   class Meta:
      fields = ('id','nombre','apellido','mail','fecha_nac','telefono','facebook','instagram','twitter')
      unknown = EXCLUDE
      ordered = True
      dump_only = ('id',)
      allow_none = ('fecha_nac', 'telefono', 'facebook', 'instagram', 'twitter')