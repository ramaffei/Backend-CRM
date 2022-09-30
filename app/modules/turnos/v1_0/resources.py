from flask import request, Blueprint
from flask_restful import Api, Resource

from app.common.error_handling import ObjectNotFound
from .schemas import TurnoSchema, TurnoEmpleadoSchema
from ...models import Empleado, Turno, TurnoEmpleado

turnos_v1_bp = Blueprint('turnos_v1_vp', __name__)
turnosSchema = TurnoSchema()
turnoEmpSchema = TurnoEmpleadoSchema

api = Api(turnos_v1_bp)

class TurnoListResource(Resource):
   def get(self):
      turno = Turno.get_all()
      result = turnosSchema.dump(turno, many=True)
      return result

   def post(self):
      data = request.get_json()
      turno_dict = turnosSchema.load(data)
      empleados = turno_dict.get('empleados', [])
      del turno_dict['empleados']
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
      turnos_dict = turnosSchema.load(data)
      empleados = turnos_dict.get('empleados', [])
      del turnos_dict['empleados']
      for empleado in empleados:
         crearRelacionEmpleado(empleado, turno)

      turno.update(turnos_dict)
      resp = turnosSchema.dump(turno)
      return resp

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