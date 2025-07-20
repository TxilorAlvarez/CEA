from functools import wraps
from flask import abort
from flask_login import current_user



def role_required(role):
    """Decorador para verificar que el usuario tenga el rol especificado."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                # Si no está autenticado, redirige al login
                return abort(401)  # HTTP 401 Unauthorized
            if current_user.rol != role:
                # Si no tiene el rol necesario, regresa 403 Forbidden
                return abort(403)  # HTTP 403 Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
