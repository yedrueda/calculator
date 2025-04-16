from flask import Flask
from flask_cors import CORS
from models.database import db, init_db
from routes.api import api_bp
from routes.mrp_routes import mrp_bp
from flask_migrate import Migrate
app = Flask(__name__)
migrate = Migrate(app, db)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración desde variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}'

init_db(app)

# Registrar Blueprints
app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

@app.cli.command('init-db')
def init_db_command():
    """Crea las tablas en la base de datos"""
    db.create_all()
    print('Base de datos inicializada')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)