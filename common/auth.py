
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import verify_jwt_in_request
from flask import jsonify

def iot_roles_required(roles=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print('Processing with func iot_roles_required...')
            print('Claims from token: ', claims)
            if roles in claims["roles"] or 'super-admin' in claims["roles"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="roles " + roles + " required"), 403
        return decorator
    return wrapper
