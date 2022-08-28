from itertools import groupby
from flask import request, Blueprint
from flask_restful import Api, Resource
from sqlalchemy import func
from app.common.error_handling import ObjectNotFound
from .schemas import EmpleadoSchema, HorarioSchema
from ...models import Empleado, Horario

empleados_v1_0_bp = Blueprint('empleados_v1_0_bp', __name__)
empleados_schema = EmpleadoSchema()
horarios_schema = HorarioSchema()

api = Api(empleados_v1_0_bp)

class HorarioTodos(Resource):
   def get(self):
      horarios = Horario.get_all()

      result = horarios_schema.dump(horarios, many=True)
      c = groupby(sorted(result, key=lambda x: x['dia']), key=lambda x: x['dia'])

      dic = {}
      for k, v in c:
         #result = groupby(sorted(list(v), key=lambda x: "{0}/{1}".format(x['hora_entrada'], x['hora_salida'])), key=lambda x: "{0}/{1}".format(x['hora_entrada'], x['hora_salida']))
         dic[k] = sorted(list(v), key=lambda x: x['hora_entrada'])
      
      return dic

class EmpleadoTodos(Resource):
   def get(self):
      empleados = Empleado.get_all()
      result = empleados_schema.dump(empleados, many=True)
      return result

   def post(self):
      data = request.get_json()
      empleados_dict = empleados_schema.load(data)
      horarios = empleados_dict.get('horarios', [])
      del empleados_dict['horarios']
      empleado = Empleado(**empleados_dict)

      for horario in horarios:
         args = Horario(**horario)
         print(args)
         empleado.horarios.append(args)

      empleado.save()
      resp = empleados_schema.dump(empleado)
      return resp, 201
   
class EmpleadoRecurso(Resource):
   def get(self, empleado_id):
      empleado = Empleado.get_by_id(empleado_id)
      if empleado is None:
         raise ObjectNotFound('El empleado no existe')
      resp = empleados_schema.dump(empleado)
      return resp

   def put(self, empleado_id):
      empleado = Empleado.get_by_id(empleado_id)
      if empleado is None:
         raise ObjectNotFound('El empleado no existe')
      data = request.get_json()
      empleados_dict = empleados_schema.load(data)

      horarios = empleados_dict.get('horarios', [])
      del empleados_dict['horarios']

      for kwargs in horarios:
         if not kwargs.get('dia', False):
            raise ObjectNotFound('Debes informar un dia para el horario que quieres guardar')

         horario = [h for h in empleado.horarios if h.dia == kwargs['dia']]

         if len(horario) == 1:
            horario_dict = horarios_schema.load(kwargs)
            horario[0].update(horario_dict)
         else:   
            horario = Horario(**kwargs)
            empleado.horarios.append(horario)

      empleado.update(empleados_dict)
      resp = empleados_schema.dump(empleado)
      return resp

   def delete(self, empleado_id):
      data = request.get_json() or {}
      empleado = Empleado.get_by_id(empleado_id)
      if empleado is None:
         raise ObjectNotFound('El empleado no existe')

      if data is not None and data.get('horarios', False):
         empleados_dict = empleados_schema.load(data)
         horarios = empleados_dict.get('horarios', [])
         del empleados_dict['horarios']
         for kwargs in horarios:
            if not kwargs.get('dia', False):
               raise ObjectNotFound('Debes informar un dia para el horario que quieres eliminar')

            horario = [h for h in empleado.horarios if h.dia == kwargs['dia']]

            if len(horario) == 1:
               print(horario)
               horario[0].delete
               return horarios_schema.dump(horario[0])
            else:
               raise ObjectNotFound('No se encuentra el dia a eliminar asignado a este usuario')

      empleado.delete()
      resp = empleados_schema.dump(empleado)
      return resp


api.add_resource(EmpleadoTodos, '/api/v1.0/empleados/', endpoint='empleados')

api.add_resource(HorarioTodos, '/api/v1.0/empleados/horarios/', endpoint='horarios')

api.add_resource(EmpleadoRecurso, '/api/v1.0/empleados/<int:empleado_id>', endpoint='empleado')