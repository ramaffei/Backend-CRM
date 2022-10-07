from flask import request, Blueprint
from flask_restful import Api, Resource

from app.common.error_handling import ObjectNotFound
from .schemas import TurnoSchema, TurnoEmpleadoSchema
from ...models import Empleado, Turno, TurnoEmpleado

turnos_v1_bp = Blueprint('turnos_v1_vp', __name__)
turnosSchema = TurnoSchema()
turnoEmpSchema = TurnoEmpleadoSchema()

api = Api(turnos_v1_bp)

class TurnoListResource(Resource):
   def get(self):
      args = request.args.to_dict()
      if args:
         turno = Turno.simple_filter_all(**args)
      else:
         turno = Turno.get_all()
      result = turnosSchema.dump(turno, many=True)
      return result

   def post(self):
      
      data = request.get_json()
      empleados = data.get('empleados', [])

      turno_dict = turnosSchema.load(data)
      turno = Turno(**turno_dict)
      
      for empleado in empleados:
         crearRelacionEmpleado(empleado, turno)
   
      turno.save()
      resp = turnosSchema.dump(turno)
      return resp, 201

class TurnoResource(Resource):
   def get(self, turno_id):
      turno = Turno.get_by_id(turno_id)
      if turno is None:
         raise ObjectNotFound('El turno no existe')
      resp = turnosSchema.dump(turno)
      return resp

   def put(self, turno_id):
      turno = Turno.get_by_id(turno_id)
      if turno is None:
         raise ObjectNotFound('El turno no existe')
      data = request.get_json()
      empleados = data.get('empleados', [])
      del data['empleados']
      
      for empleado in empleados:
         crearRelacionEmpleado(empleado, turno)

      turnos_dict = turnosSchema.load(data)
      turno.update(turnos_dict)
      resp = turnosSchema.dump(turno)
      return resp
   
   def delete(self, turno_id):
      turno = Turno.get_by_id(turno_id)
      if turno is None:
         raise ObjectNotFound('El turno no existe')
      turno.delete()
      return turnosSchema.dump(turno)

class TurnoEmpleadoResource(Resource):
   def get(self, turno_id, empleado_id):
      turno_empleado = TurnoEmpleado.simple_filter(
         id_turno = turno_id,
         id_empleado = empleado_id
      )
      if turno_empleado is None:
         raise ObjectNotFound(f'No existe ninguna relacion entre el Turno {turno_id} y el empleado {empleado_id}')
      
      return turnoEmpSchema.dump(turno_empleado)

   def delete(self, turno_id, empleado_id):
      turno_empleado = TurnoEmpleado.simple_filter(
         id_turno = turno_id,
         id_empleado = empleado_id
      )
      if turno_empleado is None:
         raise ObjectNotFound(f'No existe ninguna relacion entre el Turno {turno_id} y el empleado {empleado_id}')
      
      turno_empleado.delete()
      return turnoEmpSchema.dump(turno_empleado)

def crearRelacionEmpleado(empleado: dict, turno: Turno) -> None:
   id_empleado = empleado.get('id')
   if id_empleado is None:
      raise ObjectNotFound('Falta id de empleado')

   if len([e for e in turno.empleados if e.id == id_empleado]) == 0:
      empleado = Empleado.get_by_id(id_empleado)
      if empleado is None:
         raise ObjectNotFound(f'El empleado {id_empleado} no existe')

      turno_empleado = TurnoEmpleado(empleado = empleado, 
                                    turno = turno)
      turno_empleado.save()

api.add_resource(TurnoListResource, '/api/v1.0/turnos/', endpoint='turnos_list_resource')

api.add_resource(TurnoResource, '/api/v1.0/turnos/<int:turno_id>', endpoint='turno_resource')

api.add_resource(TurnoEmpleadoResource, '/api/v1.0/turnos/<int:turno_id>/empleado/<int:empleado_id>', endpoint='turno_empl_resource')