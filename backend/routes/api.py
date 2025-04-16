from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Importar endpoints específicos DESPUÉS de crear el Blueprint
from . import mrp_routes  # u otros archivos de rutas

# Registrar Blueprints
api_bp.register_blueprint(mrp_routes.mrp_bp, url_prefix='/mrp')