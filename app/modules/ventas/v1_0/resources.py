import collections
from pickle import LIST
from flask import request, Blueprint
from flask_restful import Api, Resource

from app.common.error_handling import ObjectNotFound
from app.common.util import transformData
from .schemas import VentaSchema, PresupuestoSchema, ItemSchema, ItemPresSchema
from ...models import Venta, Presupuesto, ItemPresupuesto, ItemVenta, Item

ventas_v1_bp = Blueprint('ventas_v1_0_bp', __name__)
venta_schema = VentaSchema()
presupuesto_schema = PresupuestoSchema()
item_schema = ItemSchema()
item_rel_schema = ItemPresSchema()

api = Api(ventas_v1_bp)

################## ITEMS ##################

class ItemListResource(Resource):
   def get(self):
      items = Item.get_all()
      result = item_schema.dump(items, many=True)
      return result

   def post(self):
      data = request.get_json()
      item_dict = item_schema.load(data)
      item = Item(**item_dict)
      item.save()
      resp = item_schema.dump(item)
      return resp, 201

class ItemResource(Resource):
   def get(self, item_id):
      item = Item.get_by_id(item_id)
      if item is None:
         raise ObjectNotFound('El item no existe')
      resp = item_schema.dump(item)
      return resp
   
   def put(self, item_id):
      item = Item.get_by_id(item_id)
      if item is None:
         raise ObjectNotFound('El item no existe')
      data = request.get_json()
      item_dict = item_schema.load(data)
      item.update(item_dict)
      resp = item_schema.dump(item)
      return resp, 201
   
   def delete(self, item_id):
      item = Item.get_by_id(item_id)
      if item is None:
         raise ObjectNotFound('El item no existe')
      item.delete()
      resp = item_schema.dump(item)
      return resp, 201

api.add_resource(ItemListResource, '/api/v1.0/items/', endpoint='item_list_resource')

api.add_resource(ItemResource, '/api/v1.0/items/<int:item_id>', endpoint='item_resource')

################## PRESUPUESTO ##################

class PresupuestoListResource(Resource):
   def get(self):
      presupuesto = Presupuesto.get_all()
      result = presupuesto_schema.dump(presupuesto, many=True)
      return result
   
   def post(self):
      data = transformData(request.get_json())
      presupuesto_dict = presupuesto_schema.load(data)
            
      items = []
      if presupuesto_dict.get('items') is not None:
         for item_dict in presupuesto_dict.get('items'):
            if item_dict.get('item_id') is not None:
               item = Item.get_by_id(item_dict.get('item_id'))
               itemPresupuesto = ItemPresupuesto(item = item, **item_dict)
            else:
               itemPresupuesto = ItemPresupuesto(**item_dict)
            items.append(itemPresupuesto)
         del presupuesto_dict['items']

      presupuesto = Presupuesto(**presupuesto_dict)
      presupuesto.items = items
      presupuesto.save()
      resp = presupuesto_schema.dump(presupuesto)
      return resp, 201

class PresupuestoResource(Resource):
   def get(self, presupuesto_id):
      presupuesto = Presupuesto.get_by_id(presupuesto_id)
      if presupuesto is None:
         raise ObjectNotFound(f'No se encuentra presupuesto con es id {presupuesto_id}')
      #print(presupuesto.turnos)
      resp = presupuesto_schema.dump(presupuesto)
      return resp
   
   def put(self, presupuesto_id):
      # Buscamos el presupuesto segun su id
      presupuesto = Presupuesto.get_by_id(presupuesto_id)
      if presupuesto is None:
         raise ObjectNotFound(f'No se encuentra presupuesto con id {presupuesto_id}')

      # Procesamos la info a modificar, y guardamos los items en una variable independiente
      data = presupuesto.buscar_cambios(**request.get_json())
      items_dict = data.get('items', [])

      # Cargamos el esquema de cambios de presupuesto
      presupuesto_dict = presupuesto_schema.load(data)

      for datos in items_dict:

         item = presupuesto.buscarRelacionEnLista(
            'items', 
            id = datos.get('id'), 
            item_id = datos.get('item_id')
            )

         if item is not None:
            cambios = item.buscar_cambios(**datos)
            if len(cambios) > 0:
               print('guardando cambios en item')
               item.update(cambios)
         else:
            print('creando relacion item presupuesto')
            presupuesto.items.append(crearRelacionItem(datos, ItemPresupuesto))
      
      if len(presupuesto_dict) > 0:
         print(presupuesto_dict)
         print('guardando cambios en presupuesto')
         presupuesto.update(presupuesto_dict)
      
      resp = presupuesto_schema.dump(presupuesto)
      return resp, 201
   
   def delete(self, item_id):
      item = Item.get_by_id(item_id)
      if item is None:
         raise ObjectNotFound('El item no existe')
      item.delete()
      resp = item_schema.dump(item)
      return resp, 201

def crearRelacionItem(item: dict, model: object):
   item_dict = item_rel_schema.load(item)
   if item_dict.get('item_id') is not None:
      item = Item.get_by_id(item_dict.get('item_id'))
      if item is None:
         raise ObjectNotFound('No se encuentra item con id {}'.format(item_dict['item_id']))
      return model(item = item, **item_dict)
   else:
      return model(**item_dict)

def encontrarItemRelacion(list_obj: list[object], **kwargs):
         
   for k, v in kwargs.items():
      if v is not None:
         obj = list(
            filter(
               lambda x: getattr(x, k, None) is not None and getattr(x, k) == v,
               list_obj
            )
         )
         if obj[0] is not None:
            return obj[0]

def buscarCambiosEnObject(obj: object, **kwargs) -> dict:
   cambios = {}
   for k, v in kwargs.items():
      if hasattr(obj, k) and getattr(obj,k) != v:
         if type(getattr(obj, k)) is collections.OrderedDict or type(getattr(obj, k)) is object:
            sub_object = buscarCambiosEnObject(getattr(obj, k), **v)
            if len(sub_object.keys()) > 0:
               cambios[k] = sub_object
         else:
            cambios[k] = v
   return cambios
api.add_resource(PresupuestoListResource, '/api/v1.0/presupuestos/', endpoint='presupuestos_list_resource')

api.add_resource(PresupuestoResource, '/api/v1.0/presupuestos/<int:presupuesto_id>', endpoint='presupuesto_resource')