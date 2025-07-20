import os
from flask import Flask
from flask_dance.contrib.google import make_google_blueprint
from app.extensions import db, migrate, login_manager, init_mail

def create_app():
    app = Flask(__name__)

    # ==============================
    # CONFIGURACIONES GENERALES
    # ==============================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'datos_demo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_super_secreta')

    # Subidas (vehículos)
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads', 'vehiculos')

    # Permitir login con OAuth en entorno local (no HTTPS)
    app.config['OAUTHLIB_INSECURE_TRANSPORT'] = True

    # ==============================
    # CONFIGURACIÓN DE GOOGLE OAUTH
    # ==============================
    app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.getenv('GOOGLE_OAUTH_CLIENT_ID', 'TU_CLIENT_ID')
    app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', 'TU_SECRET')

    google_bp = make_google_blueprint(
        client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
        client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
        redirect_to='routes.google_login'
    )
    app.register_blueprint(google_bp, url_prefix='/login')

    # ==============================
    # INICIALIZACIÓN DE EXTENSIONES
    # ==============================
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    init_mail(app)

    # ==============================
    # MODELOS Y CARGA DE USUARIO
    # ==============================
    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # ==============================
    # CREACIÓN DE TABLAS
    # ==============================
    with app.app_context():
        try:
            db.create_all()
            print("Base de datos conectada y tablas creadas.")
        except Exception as e:
            print(f"Error creando la base de datos: {e}")

    # ==============================
    # BLUEPRINTS DE RUTAS
    # ==============================
    from app.routes import routes
    app.register_blueprint(routes)

    return app
