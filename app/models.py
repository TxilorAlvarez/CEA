from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Modelo de Usuario con UserMixin
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    identificacion = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False)  # Ej. 'administrador', 'asesor', etc.
    imagen_perfil = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Curso(UserMixin, db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(10), nullable=False)  # Ejemplo: 'A2', 'B1'
    horas_teoria = db.Column(db.Integer, nullable=False)
    horas_taller = db.Column(db.Integer, nullable=False)
    horas_practica = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Float, nullable=False)

class Matricula(UserMixin, db.Model):
    __tablename__ = 'matriculas'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    identificacion = db.Column(db.String, db.ForeignKey('usuarios.id'))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False)  # Ej. 'administrador', 'asesor', etc.
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    id_curso_principal = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    id_curso_secundario = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=True)

class Pago(UserMixin, db.Model):
    __tablename__ = 'pagos'
    id = db.Column(db.Integer, primary_key=True)
    id_matricula = db.Column(db.Integer, db.ForeignKey('matriculas.id'), nullable=False)
    valor_abonado = db.Column(db.Float, nullable=False)
    saldo_pendiente = db.Column(db.Float, nullable=False)


class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    numero_placa = db.Column(db.String(20), nullable=False, unique=True)
    tipo_vehiculo = db.Column(db.String(50), nullable=False)  # Ejemplo: "Motocicleta A2"
    licencia_transito = db.Column(db.String(255), nullable=False)  # URL de la licencia
    soat = db.Column(db.String(255), nullable=False)  # URL del SOAT
    vigencia_soat = db.Column(db.Date, nullable=False)
    tecnicomecanica = db.Column(db.String(255), nullable=False)  # URL tecnicomecánica
    vigencia_tecnicomecanica = db.Column(db.Date, nullable=False)
    fotografia = db.Column(db.String(255), nullable=False)  # URL de la foto del vehículo
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vehiculo {self.numero_placa}>'
    
