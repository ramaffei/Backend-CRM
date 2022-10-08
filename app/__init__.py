from flask import Flask, got_request_exception, jsonify
from flask_restful import Api
from app.common.error_handling import InvalidAPIUsage, ObjectNotFound, AppErrorBaseClass
from app.common.errors import custom_api_error_handler
from app.db import db
from app.modules.clientes.v1_0.resources import clientes_v1_0_bp
from app.modules.empleados.v1_0.resources import empleados_v1_0_bp
from app.modules.turnos.v1_0.resources import turnos_v1_bp
from app.modules.ventas.v1_0.resources import ventas_v1_bp
from .ext import ma, migrate
from flask_cors import CORS

def create_app(settings_module):
   app = Flask(__name__)
   app.config.from_object(settings_module)
   
   # Inicializa las extensiones
   db.init_app(app)
   ma.init_app(app)
   migrate.init_app(app, db)
   cors = CORS(app, resources={r'/*': {'origins':'*'}})

   # Captura todos los errores 404
   #Api(app, catch_all_404s=True)

   # Deshabilita el modo estricto de acabado de una URL con /
   app.url_map.strict_slashes = False

   # Registra los blueprints
   app.register_blueprint(clientes_v1_0_bp)
   app.register_blueprint(empleados_v1_0_bp)
   app.register_blueprint(turnos_v1_bp)
   app.register_blueprint(ventas_v1_bp)

   # Registra manejadores de errores personalizados
   if settings_module != 'config.local':
      got_request_exception.connect(custom_api_error_handler, app)
      register_error_handlers(app)
   return app

def register_error_handlers(app):
   @app.errorhandler(Exception)
   def handle_500_error(e):
      return jsonify({'msg': f'Error: {e}'}), 500

   @app.errorhandler(405)
   def handle_405_error(e):
      return jsonify({'msg': 'Metodo no permitido'}), 405

   @app.errorhandler(403)
   def handle_403_error(e):
      return jsonify({'msg': 'Forbidden error'}), 403

   @app.errorhandler(404)
   def handle_404_error(e):
      return jsonify({'msg': 'URL no encontrada'}), 404

   @app.errorhandler(AppErrorBaseClass)
   def handle_app_base_error(e):
      return jsonify({'msg': str(e)}), 500
      
   @app.errorhandler(ObjectNotFound)
   def handle_object_not_found_error(e):
      return jsonify({'msg': str(e)}), 404