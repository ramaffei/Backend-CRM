from flask import request, Blueprint
from flask_restful import Api, Resource

from app.common.error_handling import ObjectNotFound
from .schemas import ClienteSchema
from ...models import Cliente

clientes_v1_0_bp = Blueprint('clientes_v1_0_bp', __name__)
clientes_schema = ClienteSchema()

api = Api(clientes_v1_0_bp)

class ClienteTodos(Resource):

   def get(self):
      args = request.args.to_dict()
      if args:
         clientes = Cliente.simple_filter_all(**args)
      else:
         clientes = Cliente.get_all()
      result = clientes_schema.dump(clientes, many=True)
      return result

   def post(self):
      data = request.get_json()
      clientes_dict = clientes_schema.load(data)
      cliente = Cliente(**clientes_dict)
      cliente.save()
      resp = clientes_schema.dump(cliente)
      return resp, 201
   
class ClienteRecurso(Resource):
   def get(self, cliente_id):
      cliente = Cliente.get_by_id(cliente_id)
      if cliente is None:
         raise ObjectNotFound('El cliente no existe')
      resp = clientes_schema.dump(cliente)
      return resp

   def put(self, cliente_id):
      cliente = Cliente.get_by_id(cliente_id)
      if cliente is None:
         raise ObjectNotFound('El cliente no existe')
      data = request.get_json()
      clientes_dict = clientes_schema.load(data)
      cliente.update(clientes_dict)
      resp = clientes_schema.dump(cliente)
      return resp

   def delete(self, cliente_id):
      cliente = Cliente.get_by_id(cliente_id)
      if cliente is None:
         raise ObjectNotFound('El cliente no existe')

      cliente.delete()
      return clientes_schema.dump(cliente)

api.add_resource(ClienteTodos, '/api/v1.0/clientes/', endpoint='clientes')

api.add_resource(ClienteRecurso, '/api/v1.0/clientes/<int:cliente_id>', endpoint='cliente')