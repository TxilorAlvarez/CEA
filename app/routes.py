import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from app.extensions import db
import string
import random
from flask_mail import Message
from app.utils import role_required
from flask_dance.contrib.google import google
from flask import redirect, url_for, flash

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crear el Blueprint
routes = Blueprint('routes', __name__)

# Ruta de inicio
@routes.route("/")
def index():
    logger.debug("Acceso a la página principal")
    return render_template("index.html")

# Ruta de inicio de sesión
@routes.route('/log', methods=['GET', 'POST'])
def login():
    from app.models import Usuario  # Importación interna
    from app.forms import LoginForm

    form = LoginForm()
    if form.validate_on_submit():
        logger.debug(f"Intento de inicio de sesión con  : {form.email.data}")
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        
        if usuario and usuario.check_password(form.password.data):  # Usamos check_password del modelo
            login_user(usuario)
            logger.info(f"Inicio de sesión exitoso para usuario: {usuario.nombre_usuario}")
            
             # Redirección según rol
            if usuario.rol == 'administrador':
                return redirect(url_for('routes.admin'))
            elif usuario.rol == 'asesor':
                return redirect(url_for('routes.asesor_dashboard'))
            elif usuario.rol == 'instructor':
                return redirect(url_for('routes.instructor_dashboard'))
            elif usuario.rol == 'aprendiz':
                return redirect(url_for('routes.aprendiz_dashboard'))
            else:
                logger.warning("Rol no reconocido para el usuario")
                flash('Rol no reconocido.', 'danger')
                return redirect(url_for('routes.login'))
        logger.warning("Usuario o contraseña incorrectos.")
        flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

# Ruta de registro
@routes.route('/registro', methods=['GET', 'POST'])
def registro():
    from app.models import Usuario  # Importación interna
    from app.forms import RegistroForm

    form = RegistroForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=16)
        nuevo_aprendiz = Usuario(
            nombre_usuario=form.nombre_usuario.data,
            email=form.email.data,
            identificacion=form.identificacion.data,  # Captura el dato del formulario
            password_hash=hashed_password,
            rol='aprendiz'
        )
        try:
            db.session.add(nuevo_aprendiz)
            db.session.commit()
            logger.info(f"Usuario registrado exitosamente: {nuevo_aprendiz.nombre_usuario}")
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('routes.login'))
        except IntegrityError:
            db.session.rollback()
            logger.error("Error: La identificación o el email ya están en uso.")
            flash('La identificación o el email ya están en uso.', 'danger')
    return render_template('registro.html', form=form)

# Rutas de ingreso por Google
@routes.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    if resp.ok:
        info = resp.json()
        email = info["email"]
        # Aquí deberías buscar en tu base de datos y crear el usuario si no existe
        # ...
        flash(f"Sesión iniciada con {email}", "success")
        return redirect(url_for("routes.index"))
    flash("Fallo al autenticar con Google", "danger")
    return redirect(url_for("routes.login"))

# Ruta de logout
@routes.route('/logout')
@login_required
def logout():
    logger.info(f"Usuario desconectado: {current_user.nombre_usuario}")
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('routes.login'))

# Ruta principal del dashboard del aprendiz
@routes.route('/aprendiz_dashboard', methods=['GET'])
@login_required
@role_required('aprendiz')  # Verifica si es aprendiz
def aprendiz_dashboard():
    logger.debug(f"Acceso al dashboard del aprendiz: {current_user.nombre_usuario}")
    return render_template('aprendiz_dashboard.html')

# Ruta principal del dashboard del asesor
@routes.route('/asesor_dashboard', methods=['GET'])
@login_required
@role_required('asesor')  # Verifica si es asesor
def asesor_dashboard():
    logger.debug(f"Acceso al dashboard del asesor: {current_user.nombre_usuario}")
    return render_template('asesor_dashboard.html')

# Ruta principal del dashboard del instructor
@routes.route('/instructor_dashboard', methods=['GET'])
@login_required
@role_required('instructor')  # Verifica si es instructor
def instructor_dashboard():
    logger.debug(f"Acceso al dashboard del instructor: {current_user.nombre_usuario}")
    return render_template('instructor_dashboard.html')

# Ruta de contacto
@routes.route('/contactanos')
def contactanos():
    logger.debug("Acceso a la página de contacto")
    return render_template('contacto.html')

# Ruta de cursos
@routes.route('/cursos')
def cursos():
    logger.debug("Acceso a la página de cursos")
    return render_template('cursos.html')

# Ruta principal del dashboard del administrador
@routes.route('/admin')
@login_required
@role_required('administrador')  # Verifica si es administrador
def admin():
    logger.debug(f"Acceso al dashboard del administrador: {current_user.nombre_usuario}")
    return render_template('dashboard_admin.html')


# Ruta de registro instructores
@routes.route('/agregar_instructor', methods=['GET', 'POST'])
def agregar_instructor():
    from app.models import Usuario  # Importación interna
    from app.forms import Agregar_instructorForm

    form = Agregar_instructorForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=16)
        nuevo_instructor = Usuario(
            nombre_usuario=form.nombre_usuario.data,
            email=form.email.data,
            identificacion=form.identificacion.data,  # Captura el dato del formulario
            password_hash=hashed_password,
            rol='instructor'
        )
        try:
            db.session.add(nuevo_instructor)
            db.session.commit()
            logger.info(f"Instructor registrado exitosamente: {nuevo_instructor.nombre_usuario}")
            flash('Instructor registrado exitosamente.', 'success')
            return redirect(url_for('routes.agregar_instructor'))
        except IntegrityError:
            db.session.rollback()
            logger.error("Error: La identificación o el email ya están en uso.")
            flash('La identificación o el email ya están en uso.', 'danger')
    return render_template('agregar_instructor.html', form=form)

# Ruta de registro asesor
@routes.route('/agregar_asesor', methods=['GET', 'POST'])
def agregar_asesor():
    from app.models import Usuario  # Importación interna
    from app.forms import Agregar_asesorForm

    form = Agregar_asesorForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=16)
        nuevo_asesor = Usuario(
            nombre_usuario=form.nombre_usuario.data,
            email=form.email.data,
            identificacion=form.identificacion.data,  # Captura el dato del formulario
            password_hash=hashed_password,
            rol='asesor'
        )
        try:
            db.session.add(nuevo_asesor)
            db.session.commit()
            logger.info(f"Instructor registrado exitosamente: {nuevo_asesor.nombre_usuario}")
            flash('Instructor registrado exitosamente.', 'success')
            return redirect(url_for('routes.admin'))
        except IntegrityError:
            db.session.rollback()
            logger.error("Error: La identificación o el email ya están en uso.")
            flash('La identificación o el email ya están en uso.', 'danger')
    return render_template('agregar_asesor.html', form=form)


@routes.route('/registrar_matricula', methods=['GET', 'POST'])
def registrar_matricula():
    from app.forms import Registrar_MatriculaForm
    from app.models import Usuario, Curso, Matricula, Pago
    from app.extensions import db
    from flask import flash, redirect, render_template
    import random
    import string

    form = Registrar_MatriculaForm()
    
    # Poblar las opciones de los SelectField con las categorías de la base de datos
    categorias = [(curso.id, curso.nombre) for curso in Curso.query.all()]
    if not categorias:
        flash('No hay categorías disponibles. Por favor, agrega cursos primero.', 'warning')
        return render_template('registrar_matricula.html', form=form)
    
    form.curso_principal.choices = categorias
    form.curso_secundario.choices = [(0, 'Sin categoría secundaria')] + categorias

    if form.validate_on_submit():
        # Generar una contraseña aleatoria
        password_generada = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Crear un nuevo usuario con rol 'aprendiz'
        try:
            nuevo_usuario = Usuario(
                nombre_usuario=form.nombre_usuario.data,
                email=form.email.data,
                identificacion=form.identificacion.data,
                rol='aprendiz',
            )
            nuevo_usuario.set_password(password_generada)
            db.session.add(nuevo_usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al registrar el usuario. Inténtalo de nuevo.', 'danger')
            return render_template('registrar_matricula.html', form=form)

        # Enviar la contraseña al correo electrónico del usuario
        enviar_correo = ()
        try:
            enviar_correo(form.email.data, password_generada)
        except Exception as e:
            db.session.rollback()
            flash('Error al enviar el correo. Inténtalo nuevamente.', 'danger')
            return render_template('registrar_matricula.html', form=form)

        # Procesar la matrícula
        try:
            matricula = Matricula(
                id_usuario=nuevo_usuario.id,
                nombre_usuario=form.nombre_usuario.data,
                identificacion=form.identificacion.data,
                email=form.email.data,
                id_curso_principal=form.curso_principal.data,
                id_curso_secundario=form.curso_secundario.data if form.curso_secundario.data != 0 else None,
            )
            db.session.add(matricula)
            db.session.commit()

            # Agregar el pago correspondiente
            pago = Pago(
                id_matricula=matricula.id,
                valor_abonado=form.valor_abonado.data,
                saldo_pendiente=form.saldo_pendiente.data
            )
            db.session.add(pago)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al registrar la matrícula. Inténtalo de nuevo.', 'danger')
            return render_template('registrar_matricula.html', form=form)

        flash('Matrícula registrada exitosamente. La contraseña fue enviada al correo.', 'success')
        return redirect('/registrar_matricula')

    return render_template('asesor_dashboard.html', form=form)

@routes.route('/agregar_vehiculo', methods=['GET', 'POST'])  
def agregar_vehiculo():  
   from app.forms import AgregarVehiculoForm  
   from app.models import Vehiculo  
   from app.extensions import db  
   from flask import flash, redirect, render_template, url_for  
   import os  
   from werkzeug.utils import secure_filename  
  
   form = AgregarVehiculoForm()  
  
   if form.validate_on_submit():  
      try:  
        # Guardar archivos en una carpeta específica  
        uploads_dir = os.path.join('static', 'uploads', 'vehiculos')  
        if not os.path.exists(uploads_dir):  
           os.makedirs(uploads_dir)  
  
        # Guardar cada archivo  
        licencia_filename = secure_filename(form.licencia_transito.data.filename)  
        licencia_path = os.path.join(uploads_dir, licencia_filename)  
        form.licencia_transito.data.save(licencia_path)  
  
        soat_filename = secure_filename(form.soat.data.filename)  
        soat_path = os.path.join(uploads_dir, soat_filename)  
        form.soat.data.save(soat_path)  
  
        tecno_filename = secure_filename(form.tecnicomecanica.data.filename)  
        tecno_path = os.path.join(uploads_dir, tecno_filename)  
        form.tecnicomecanica.data.save(tecno_path)  
  
        foto_filename = secure_filename(form.fotografia.data.filename)  
        foto_path = os.path.join(uploads_dir, foto_filename)  
        form.fotografia.data.save(foto_path)  
  
        # Validar duplicados  
        if Vehiculo.query.filter_by(numero_placa=form.numero_placa.data.upper()).first():  
           flash('Ya existe un vehículo con esa placa.', 'danger')  
           return render_template('agregar_vehiculo.html', form=form)  
  
        # Crear nueva entrada en la base de datos  
        nuevo_vehiculo = Vehiculo(  
           numero_placa=form.numero_placa.data.upper(),  
           tipo_vehiculo=form.tipo_vehiculo.data,  
           licencia_transito=f'static/uploads/vehiculos/{licencia_filename}',  
           soat=f'static/uploads/vehiculos/{soat_filename}',  
           vigencia_soat=form.vigencia_soat.data,  
           tecnicomecanica=f'static/uploads/vehiculos/{tecno_filename}',  
           vigencia_tecnicomecanica=form.vigencia_tecnicomecanica.data,  
           fotografia=f'static/uploads/vehiculos/{foto_filename}',  
        )  
  
        db.session.add(nuevo_vehiculo)  
        db.session.commit()
  
        flash('Vehículo registrado exitosamente.', 'success')  
        return redirect(url_for('ver_vehiculos'))  
  
      except Exception as e:  
        db.session.rollback()  
        flash(f'Error al registrar el vehículo: {str(e)}', 'danger')  
  
   return render_template('agregar_vehiculo.html', form=form)

@routes.route("/motos")
def motos():
    logger.debug("Acceso a la página de motos")
    return render_template("motos.html")

@routes.route("/carros")
def carros():
    logger.debug("Acceso a la página de carros")
    return render_template("carros.html")

@routes.route("/camiones")
def camiones():
    logger.debug("Acceso a la página de carros")
    return render_template("camiones.html")

@routes.route("/tracto_camiones")
def tracto_camiones():
    logger.debug("Acceso a la página de carros")
    return render_template("tracto_camiones.html")

@routes.route('/usuarios')
@login_required
def ver_usuarios():
    return render_template("gestionar_usuarios.html")

@routes.route('/cursos_vendidos')
@login_required
def ver_cursos():
    return "Aquí iría la gestión de cursos"

@routes.route('/matriculas')
@login_required
def ver_matriculas():
    return "Aquí iría la gestión de matrículas"

@routes.route('/pagos')
@login_required
def ver_pagos():
    return "Aquí iría la gestión de pagos"
