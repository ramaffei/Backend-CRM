from itertools import groupby
from flask import request, Blueprint
from flask_restful import Api, Resource
from sqlalchemy import func
from app.common.error_handling import ObjectNotFound
from .schemas import EmpleadoSchema, HorarioSchema
from ...models import Empleado, Horario, TurnoEmpleado
from app.modules.turnos.v1_0.schemas import TurnoSchema

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
class HorarioRecurso(Resource):
   def get(self, horario_id):
      horario = Horario.get_by_id(horario_id)
      if horario is None:
         raise ObjectNotFound('El horario solicitado no existe')
      return horarios_schema.dump(horario)

   def put(self, horario_id):
      horario = Horario.get_by_id(horario_id)
      if horario is None:
         raise ObjectNotFound('El horario no existe')
      data = request.get_json()
      horario_dict = horarios_schema.load(data)
      horario.update(horario_dict)
      return horarios_schema.dump(horario)

   def delete(self, horario_id):
      horario = Horario.get_by_id(horario_id)
      if horario is None:
         raise ObjectNotFound('El horario no existe')
      horario.delete()
      return horarios_schema.dump(horario)
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

      for h in horarios:
         horario_id = h.get('id')
         if horario_id is not None:
            horario = Horario.get_by_id(horario_id)
            if horario is None:
               raise ObjectNotFound(f'El horario {horario_id} no existe')
            if horario.empleado_id != empleado_id:
               raise ObjectNotFound(f'El horario {horario_id} no corresponde al empleado {empleado_id}')
            cambios = horario.buscar_cambios(**h)
            if len(cambios) > 0:
               horario.update(cambios) 
         else:
            horario_empleado = Horario(**horario)
            empleado.horarios.append(horario_empleado)
      empleado.update(empleados_dict)
      resp = empleados_schema.dump(empleado)
      return resp

   def delete(self, empleado_id):
      empleado = Empleado.get_by_id(empleado_id)
      if empleado is None:
         raise ObjectNotFound('El empleado no existe')

      if hasattr(empleado, 'horarios'):
         for horario in empleado.horarios:
            horario.delete()

      empleado.delete()
      resp = empleados_schema.dump(empleado)
      return resp

class EmpleadoTurnoRecurso(Resource):
   def get(self, empleado_id):
      turnos_empleados = TurnoEmpleado.simple_filter_all(id_empleado = empleado_id)
      turnos = [turno.turno for turno in turnos_empleados if turno.turno is not None]
      return TurnoSchema().dump(turnos, many=True)

api.add_resource(EmpleadoTurnoRecurso, '/api/v1.0/empleados/<int:empleado_id>/turnos', endpoint='turnos_empleado')

api.add_resource(EmpleadoTodos, '/api/v1.0/empleados/', endpoint='empleados')

api.add_resource(HorarioTodos, '/api/v1.0/empleados/horarios/', endpoint='horarios')

api.add_resource(HorarioRecurso, '/api/v1.0/empleados/horarios/<horario_id>', endpoint='horario')

api.add_resource(EmpleadoRecurso, '/api/v1.0/empleados/<int:empleado_id>', endpoint='empleado')