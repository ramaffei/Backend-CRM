import collections
from pickle import LIST
from xml.etree.ElementInclude import include
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

      #Procesamos los items
      item_nuevo = False
      for datos in items_dict:
      
      #Buscando si el item ya es parte del presupuesto
         item = presupuesto.buscarRelacionEnLista(
            'items', 
            id = datos.get('id'), 
            item_id = datos.get('item_id')
            )

      # Si es parte lo actualiza, sino crea uno nuevo
         if item is not None:
            cambios = item.buscar_cambios(**datos)
            if len(cambios) > 0:
               item.update(cambios)
         else:
            item_nuevo = True
            presupuesto.items.append(crearRelacionItem(datos, ItemPresupuesto))
      
      # Si hay cambios que guardar actualiza el presupuesto
      if len(presupuesto_dict) > 0 or item_nuevo:
         presupuesto.update(presupuesto_dict)
      
      resp = presupuesto_schema.dump(presupuesto)
      return resp, 201
   
class PresupuestoItemsResource(Resource):
   def get(self, presupuesto_id, rel_id):
      item_presupuesto = ItemPresupuesto.simple_filter(id = rel_id, presupuesto_id = presupuesto_id)
      if item_presupuesto is None:
         raise ObjectNotFound(f'No se encuentra el item con id {rel_id} o no esta relacionado al presupuesto con id {presupuesto_id}')
      return item_rel_schema.dump(item_presupuesto)

   def put(self, presupuesto_id, rel_id):
      item_presupuesto = ItemPresupuesto.simple_filter(id = rel_id, presupuesto_id = presupuesto_id)
      if item_presupuesto is None:
         raise ObjectNotFound(f'No se encuentra el item con id {rel_id} o no esta relacionado al presupuesto con id {presupuesto_id}')
      
      data = item_presupuesto.buscar_cambios(**request.get_json())
      data_dict = item_rel_schema.load(data)
      if data_dict.get('item_id'): del data_dict['item_id']
      if data_dict.get('id'): del data_dict['id']

      if len(data_dict) > 0:
         item_presupuesto.update(data_dict)
      
      return item_rel_schema.dump(item_presupuesto)

   def delete(self, presupuesto_id, rel_id):
      item_presupuesto = ItemPresupuesto.simple_filter(id = rel_id, presupuesto_id = presupuesto_id)
      if item_presupuesto is None:
         raise ObjectNotFound(f'No se encuentra el item con id {rel_id} o no esta relacionado al presupuesto con id {presupuesto_id}')

      item_presupuesto.delete()
      return item_rel_schema.dump(item_presupuesto)

class PresupuestoItemsListResource(Resource):
   def get(self, presupuesto_id):
      item_presupuesto = ItemPresupuesto.simple_filter_all(presupuesto_id = presupuesto_id)
      if item_presupuesto is None:
         raise ObjectNotFound(f'No se encuentran el items en el presupuesto con id {presupuesto_id}')

      return item_rel_schema.dump(item_presupuesto, many=True)

   def post(self, presupuesto_id):
      presupuesto = Presupuesto.get_by_id(presupuesto_id)
      if presupuesto is None:
         raise ObjectNotFound(f'No se encuentra presupuesto con es id {presupuesto_id}')

      data = request.get_json()

      if type(data) is not list:
         raise ObjectNotFound('El JSON debe ser un array')

      item_nuevo = False
      for d in data:
      #Buscando si el item ya es parte del presupuesto
         item = presupuesto.buscarRelacionEnLista(
               'items', 
               item_id = d.get('item_id')
               )
         
         if item is not None:
            cambios = item.buscar_cambios(**d)
            cambios = item_rel_schema.load(cambios)
            if cambios.get('id') is not None:
               del cambios['id']

            if len(cambios) > 0:
               item.update(cambios)
         else:
            item_nuevo = True
            item_dict = item_rel_schema.load(d)
            presupuesto.items.append(crearRelacionItem(item_dict, ItemPresupuesto))

      if item_nuevo:
         presupuesto.update({})
      return item_rel_schema.dump(presupuesto.items, many = True)

   def delete(self, presupuesto_id):
      presupuesto = Presupuesto.get_by_id(presupuesto_id)
      if presupuesto is None:
         raise ObjectNotFound(f'No se encuentra presupuesto con es id {presupuesto_id}')
      
      if not presupuesto.items:
         raise ObjectNotFound('No hay items que eliminar')

      for item in presupuesto.items:
         item.delete()

      return presupuesto_schema.dump(presupuesto)

api.add_resource(PresupuestoListResource, '/api/v1.0/presupuestos/', endpoint='presupuestos_list_resource')

api.add_resource(PresupuestoResource, '/api/v1.0/presupuestos/<int:presupuesto_id>', endpoint='presupuesto_resource')

api.add_resource(PresupuestoItemsListResource, '/api/v1.0/presupuestos/<int:presupuesto_id>/items/', endpoint='presupuesto_itemList_resource')

api.add_resource(PresupuestoItemsResource, '/api/v1.0/presupuestos/<int:presupuesto_id>/items/<rel_id>', endpoint='presupuesto_item_resource')

################## VENTAS ##################

class VentaListResource(Resource):
   def get(self):
      venta = Venta.get_all()
      result = venta_schema.dump(venta, many=True)
      return result
   
   def post(self):
      data = transformData(request.get_json())
      venta_dict = venta_schema.load(data)
            
      items = []
      if venta_dict.get('items') is not None:
         for item_dict in venta_dict.get('items'):
            if item_dict.get('item_id') is not None:
               item = Item.get_by_id(item_dict.get('item_id'))
               itemVenta = ItemVenta(item = item, **item_dict)
            else:
               itemVenta = ItemVenta(**item_dict)
            items.append(itemVenta)
         del venta_dict['items']

      venta = Venta(**venta_dict)
      venta.items = items
      venta.save()
      resp = venta_schema.dump(venta)
      return resp, 201

class VentaResource(Resource):
   def get(self, venta_id):
      venta = Venta.get_by_id(venta_id)
      if venta is None:
         raise ObjectNotFound(f'No se encuentra venta con es id {venta_id}')
      #print(venta.turnos)
      resp = venta_schema.dump(venta)
      return resp
   
   def put(self, venta_id):
      # Buscamos el venta segun su id
      venta = Venta.get_by_id(venta_id)
      if venta is None:
         raise ObjectNotFound(f'No se encuentra venta con id {venta_id}')

      # Procesamos la info a modificar, y guardamos los items en una variable independiente
      data = venta.buscar_cambios(**request.get_json())
      items_dict = data.get('items', [])

      # Cargamos el esquema de cambios de venta
      venta_dict = venta_schema.load(data)

      #Procesamos los items
      item_nuevo = False
      for datos in items_dict:
      
      #Buscando si el item ya es parte del venta
         item = venta.buscarRelacionEnLista(
            'items', 
            id = datos.get('id'), 
            item_id = datos.get('item_id')
            )

      # Si es parte lo actualiza, sino crea uno nuevo
         if item is not None:
            cambios = item.buscar_cambios(**datos)
            if len(cambios) > 0:
               item.update(cambios)
         else:
            item_nuevo = True
            venta.items.append(crearRelacionItem(datos, ItemVenta))
      
      # Si hay cambios que guardar actualiza el venta
      if len(venta_dict) > 0 or item_nuevo:
         venta.update(venta_dict)
      
      resp = venta_schema.dump(venta)
      return resp, 201
   
class VentaItemsResource(Resource):
   def get(self, venta_id, rel_id):
      item_venta = ItemVenta.simple_filter(id = rel_id, venta_id = venta_id)
      if item_venta is None:
         raise ObjectNotFound(f'No se encuentra el item con id {rel_id} o no esta relacionado al venta con id {venta_id}')
      return item_rel_schema.dump(item_venta)

   def put(self, venta_id, rel_id):
      item_venta = ItemVenta.simple_filter(id = rel_id, venta_id = venta_id)
      if item_venta is None:
         raise ObjectNotFound(f'No se encuentra el item con id {rel_id} o no esta relacionado al venta con id {venta_id}')
      
      data = item_venta.buscar_cambios(**request.get_json())
      data_dict = item_rel_schema.load(data)
      if data_dict.get('item_id'): del data_dict['item_id']
      if data_dict.get('id'): del data_dict['id']

      if len(data_dict) > 0:
         item_venta.update(data_dict)
      
      return item_rel_schema.dump(item_venta)

   def delete(self, venta_id, rel_id):
      item_venta = ItemVenta.simple_filter(id = rel_id, venta_id = venta_id)
      if item_venta is None:
         raise ObjectNotFound(f'No se encuentra el item con id {rel_id} o no esta relacionado al venta con id {venta_id}')

      item_venta.delete()
      return item_rel_schema.dump(item_venta)

class VentaItemsListResource(Resource):
   def get(self, venta_id):
      item_venta = ItemVenta.simple_filter_all(venta_id = venta_id)
      if item_venta is None:
         raise ObjectNotFound(f'No se encuentran el items en el venta con id {venta_id}')
      print('item',item_venta)
      return item_rel_schema.dump(item_venta, many=True)

   def post(self, venta_id):
      venta = Venta.get_by_id(venta_id)
      if venta is None:
         raise ObjectNotFound(f'No se encuentra venta con es id {venta_id}')

      data = request.get_json()

      if type(data) is not list:
         raise ObjectNotFound('El JSON debe ser un array')

      item_nuevo = False
      for d in data:
      #Buscando si el item ya es parte del venta
         item = venta.buscarRelacionEnLista(
               'items', 
               item_id = d.get('item_id')
               )
         
         if item is not None:
            cambios = item.buscar_cambios(**d)
            cambios = item_rel_schema.load(cambios)
            if cambios.get('id') is not None:
               del cambios['id']

            if len(cambios) > 0:
               item.update(cambios)
         else:
            item_nuevo = True
            item_dict = item_rel_schema.load(d)
            venta.items.append(crearRelacionItem(item_dict, ItemVenta))

      if item_nuevo:
         venta.update({})
      return item_rel_schema.dump(venta.items, many = True)

   def delete(self, venta_id):
      venta = Venta.get_by_id(venta_id)
      if venta is None:
         raise ObjectNotFound(f'No se encuentra venta con es id {venta_id}')
      
      if not venta.items:
         raise ObjectNotFound('No hay items que eliminar')

      for item in venta.items:
         item.delete()

      return venta_schema.dump(venta)

api.add_resource(VentaListResource, '/api/v1.0/ventas/', endpoint='ventas_list_resource')

api.add_resource(VentaResource, '/api/v1.0/ventas/<int:venta_id>', endpoint='venta_resource')

api.add_resource(VentaItemsListResource, '/api/v1.0/ventas/<int:venta_id>/items/', endpoint='venta_itemList_resource')

api.add_resource(VentaItemsResource, '/api/v1.0/ventas/<int:venta_id>/items/<rel_id>', endpoint='venta_item_resource')

################## UTILS ##################

def crearRelacionItem(item: dict, model: object):
   item_dict = item_rel_schema.load(item)
   if item_dict.get('item_id') is not None:
      item = Item.get_by_id(item_dict.get('item_id'))
      if item is None:
         raise ObjectNotFound('No se encuentra item con id {}'.format(item_dict['item_id']))
      return model(item = item, **item_dict)
   else:
      return model(**item_dict)