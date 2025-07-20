from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, HiddenField, DecimalField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Length, Regexp


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar Sesión')

class RegistroForm(FlaskForm):
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    rol = SelectField('Rol', choices=[
        ('aprendiz', 'Aprendiz'),
        ('asesor', 'Asesor'),
        ('instructor', 'Instructor')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrarse')

class Agregar_instructorForm(FlaskForm): 
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    identificacion = StringField('Identificación', validators=[DataRequired(), Length(min=4, max=20)])  # Nuevo campo
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')

class Agregar_asesorForm(FlaskForm): 
    nombre_usuario = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    identificacion = StringField('Identificación', validators=[DataRequired(), Length(min=4, max=20)])  # Nuevo campo
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')


class Registrar_MatriculaForm(FlaskForm):
    # Datos del usuario
    nombre_usuario = StringField('Nombre del Usuario', validators=[DataRequired(), Length(min=4, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    identificacion = StringField('Identificación', validators=[DataRequired(), Length(min=4, max=20)])
    contacto = StringField('Número de Contacto', validators=[DataRequired(), Length(min=7, max=15)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    rol = StringField('Rol', validators=[DataRequired(), Length(max=50)])
    imagen_perfil = StringField('URL Imagen de Perfil', validators=[Length(max=255)])
    
    # Datos del curso
    curso_principal = SelectField(
        'Categoría Principal', 
        coerce=int,  # Esto asegura que las opciones se conviertan a enteros
        choices=[
            (1, 'Elige la categoría ' ),
            (2, 'A1'),
            (3, 'A2'),
            (4, 'B1'),
            (5, 'C1'),
            (6, 'RC1')
        ],
        validators=[DataRequired()]
    )
    curso_secundario = SelectField(
        'Categoría Secundaria (opcional)', 
        coerce=int, 
        choices=[
            (1, 'Matricula otra categoría '),
            (2, 'A1'),
            (3, 'A2'),
            (4, 'B1'),
            (5, 'C1'),
            (6, 'RC1')
        ]
    )
    
    # Datos del pago
    valor_abonado = DecimalField('Valor Abonado', validators=[DataRequired(), NumberRange(min=0)])
    saldo_pendiente = DecimalField('Saldo Pendiente', validators=[DataRequired(), NumberRange(min=0)])
    precio_total = HiddenField('Precio Total', default=0)  # Campo oculto para almacenar el precio total
    submit = SubmitField('Registrar Matrícula')


class AgregarVehiculoForm(FlaskForm):
    numero_placa = StringField('Número de Placa', validators=[
        DataRequired(), Length(min=6, max=10), Regexp('^[A-Z0-9]+$', message='Solo letras y números permitidos')
    ])
    tipo_vehiculo = SelectField('Tipo de Vehículo', choices=[
        ('Motocicleta A2', 'Motocicleta A2'),
        ('Automóvil', 'Automóvil'),
        ('Camión', 'Camión'),
        ('Otro', 'Otro')
    ], validators=[DataRequired()])
    licencia_transito = FileField('Licencia de Tránsito', validators=[DataRequired()])
    soat = FileField('SOAT', validators=[DataRequired()])
    vigencia_soat = DateField('Vigencia del SOAT', validators=[DataRequired()], format='%Y-%m-%d')
    tecnicomecanica = FileField('Técnico Mecánica', validators=[DataRequired()])
    vigencia_tecnicomecanica = DateField('Vigencia Técnico Mecánica', validators=[DataRequired()], format='%Y-%m-%d')
    fotografia = FileField('Fotografía del Vehículo', validators=[DataRequired()])
    submit = SubmitField('Registrar Vehículo')