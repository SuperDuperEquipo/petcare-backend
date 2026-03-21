import email

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from app.core.extensions import db, revoked_tokens
from app.auth.models.user import User


def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return (
            jsonify({"error": "Los campos name, email y password son obligatorios"}),
            422,
        )

    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 422

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 409

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )

    return (
        jsonify(
            {
                "message": "Usuario registrado exitosamente",
                "user": user.to_dict(),
                "access_token": access_token,
            }
        ),
        201,
    )


def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Los campos email y password son obligatorios"}), 422

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    if not user.is_active:
        return jsonify({"error": "Cuenta desactivada. Contacta al soporte"}), 403

    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )

    return (
        jsonify(
            {
                "message": "Inicio de sesión exitoso",
                "user": user.to_dict(),
                "access_token": access_token,
            }
        ),
        200,
    )


@jwt_required()
def logout():
    jti = get_jwt().get("jti")
    revoked_tokens.add(jti)
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200


@jwt_required()
def get_profile():
    current_user_id = int(get_jwt_identity())
    user = db.session.get(User, current_user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return (
        jsonify(
            {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": getattr(user, "email", ""),
                }
            }
        ),
        200,
    )


@jwt_required()
def update_profile():
    current_user_id = int(get_jwt_identity())
    user = db.session.get(User, current_user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json(silent=True)
    if data:
        if "name" in data:
            user.name = data["name"].strip()
        if "email" in data:
            user.email = data["email"].strip()

        db.session.commit()

    return jsonify({"mensaje": "Perfil actualizado exitosamente"}), 200
