# 🚗 CEA (SGAC)
## Sistema de Gestión de Acceso a Cursos
Plataforma Integral para Escuelas de Conducción

# 📌 Descripción General

CEA es un sistema de gestión web diseñado para optimizar la administración de una escuela de conducción.
Permite controlar roles de usuario, gestionar inscripciones a cursos, registrar instructores y asesores, y mantener un control completo de documentos y vehículos.

### El sistema prioriza:

## 🔒 Seguridad

## ⚙️ Escalabilidad

## 🌐 Accesibilidad

## 🧩 Facilidad de uso para administradores




# 🛠️ Tecnologías Utilizadas

| Categoría         | Tecnología                             |
| ----------------- | -------------------------------------- |
| **Lenguaje**      | Python 3.x                             |
| **Framework Web** | Flask (Jinja2 Templates)               |
| **ORM**           | SQLAlchemy                             |
| **Frontend**      | HTML5 · CSS3 · Bootstrap · JS          |
| **Base de Datos** | SQLite *(migrable a PostgreSQL/MySQL)* |
| **Autenticación** | Flask-Login                            |
| **Formularios**   | Flask-WTF *(con CSRF)*                 |
| **Archivos**      | WTForms (manejo seguro)                |



## 🎯 Objetivo del Sistema

### CEA busca resolver problemas comunes en escuelas de conducción:

✔ Falta de un flujo digital unificado

✔ Ausencia de control de acceso por roles

✔ Procesos manuales de registro y seguimiento

✔ Gestión deficiente de documentos y vehículos

### Con CEA podrás:

- Digitalizar el proceso de matrícula y pagos

- Asignar roles como Instructor o Asesor

- Gestionar documentos vehiculares (SOAT, RTM, licencias, etc.)

- Mantener historiales completos de estudiantes y saldos

  

# 🔐 Control de Acceso y Roles


CEA implementa un sistema seguro basado en permisos:

## 🛡️ Panel de Administrador

Registro de instructores y asesores

Gestión completa de usuarios

Administración de vehículos y documentos

Subida de imágenes y archivos asociados

## 👨‍🏫 Panel de Instructor (Próximamente)

Consulta de estudiantes asignados

Acceso a materiales académicos

## 👨‍💼 Panel de Asesor (Próximamente)

Registro de estudiantes

Control de pagos e historial financiero

#### Seguridad implementada con:

# 🔐 Flask-Login

🔑 Werkzeug (hash seguro de contraseñas)

📚 Funcionalidades Principales
✅ Gestión de Usuarios

#### Registro y autenticación con roles

#### Validación única de correo e identificación

📘 Matrículas e Inscripciones

Registro de estudiantes

Selección de curso

Control de abonos y saldos pendientes

🚗 Gestión de Vehículos

Carga de documentos del vehículo

Control de vencimientos (SOAT, RTM, etc.)

📄 Manejo de Documentos

Subida de PDF e imágenes

Acceso desde los paneles internos

💡 Accesibilidad y Diseño

UI limpia creada con Bootstrap

Formularios intuitivos y centrados en UX

Vista optimizada para dispositivos móviles

Sistema modular basado en plantillas (base.html, componentes, bloques)

---

# 🧪 Instalación y Configuración
1. **Clonar el repositorio**:
bash
   git clone https://github.com/TxilorAlvarez/CEA/driving-school-platform.git
   cd driving-school-platform
   git clone https://github.com/TxilorAlvarez/CEA/driving-school-platform.git
   cd driving-school-platform

## 2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux / MacOS
venv\Scripts\activate      # Windows

## 3️⃣ Instalar dependencias
pip install -r requirements.txt

## 4️⃣ Ejecutar el servidor
flask run



---


### 📎 Futuras Mejoras

Dashboard completo para instructores y asesores

Notificaciones por vencimiento de documentos

Integración con pasarelas de pago

Módulo avanzado de reportes y estadísticas

🤝 Contribuciones

¡Las contribuciones son bienvenidas!
Realiza un fork, crea tu rama de mejoras y abre un pull request.

