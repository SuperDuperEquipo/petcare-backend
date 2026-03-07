from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.auth.models.user import User
from app.core.extensions import db


def require_admin(fn):
    """Decorador que verifica que el usuario sea admin."""
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"error": "Acceso denegado. Se requiere rol admin"}), 403
        return fn(*args, **kwargs)
    return wrapper


@jwt_required()
@require_admin
def get_users():
    """GET /api/v1/admin/users — Lista todos los usuarios."""
    users = User.query.all()
    return jsonify({
        "users": [u.to_dict() for u in users],
        "total": len(users)
    }), 200


@jwt_required()
@require_admin
def delete_user(id):
    """DELETE /api/v1/admin/users/<id> — Elimina un usuario."""
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Usuario {user.email} eliminado exitosamente"}), 200