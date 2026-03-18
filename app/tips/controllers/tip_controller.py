from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.core.extensions import db
from app.tips.models.tip import Tip


def require_admin_role():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Acceso restringido para administradores"}), 403
    return None


@jwt_required()
def get_tips():
    tips = Tip.query.all()
    return jsonify({
        "mensaje": "Tips obtenidos exitosamente",
        "tips": [tip.to_dict() for tip in tips],
        "total": len(tips),
    }), 200


@jwt_required()
def create_tip():
    err = require_admin_role()
    if err: return err

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    title    = data.get("title", "").strip()
    content  = data.get("content", "").strip()
    species  = data.get("species", "").strip()
    category = data.get("category", "").strip()

    if not title or not content or not species or not category:
        return jsonify({"error": "Todos los campos (title, content, species, category) son obligatorios"}), 422

    tip = Tip(
        title=title,
        content=content,
        species=species,
        category=category
    )

    db.session.add(tip)
    db.session.commit()

    return jsonify({
        "mensaje": "Tip creado exitosamente",
        "tip": tip.to_dict(),
    }), 201