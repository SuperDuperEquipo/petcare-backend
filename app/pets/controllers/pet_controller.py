from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.core.extensions import db
from app.pets.models.pet import Pet


def get_current_user():
    return int(get_jwt_identity())


def require_user_role():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "Acceso restringido para dueños de mascotas"}), 403
    return None


@jwt_required()
def get_pets():
    err = require_user_role()
    if err:
        return err
    user_id = get_current_user()

    if not user_id:
        return jsonify({"error": "No hay dueño para esta mascota"}), 404

    pets = Pet.query.filter_by(user_id=user_id).all()

    return (
        jsonify(
            {
                "mensaje": "Mascotas obtenidas exitosamente",
                "mascotas": [pet.to_dict() for pet in pets],
                "total": len(pets),
            }
        ),
        200,
    )


@jwt_required()
def create_pet():
    err = require_user_role()
    if err:
        return err
    user_id = get_current_user()
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    name = data.get("name", "").strip()
    species = data.get("species", "").strip()

    if not name or not species:
        return jsonify({"error": "El nombre y la especie son obligatorios"}), 422

    birth_date = None
    if data.get("birth_date"):
        try:
            birth_date = datetime.strptime(data["birth_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 422

    pet = Pet(
        name=name,
        species=species,
        breed=data.get("breed"),
        birth_date=birth_date,
        weight=data.get("weight"),
        photo_url=data.get("photo_url"),
        user_id=user_id,
    )

    db.session.add(pet)
    db.session.commit()

    return (
        jsonify(
            {
                "mensaje": "Mascota creada exitosamente",
                "mascota": pet.to_dict(),
            }
        ),
        201,
    )


@jwt_required()
def get_pet(pet_id):
    err = require_user_role()
    if err:
        return err
    user_id = get_current_user()

    pet = Pet.query.filter_by(id=pet_id, user_id=user_id).first()

    if not pet:
        return jsonify({"error": "Mascota no encontrada"}), 404

    return (
        jsonify(
            {
                "mensaje": "Mascota obtenida exitosamente",
                "mascota": pet.to_dict(),
            }
        ),
        200,
    )


@jwt_required()
def update_pet(pet_id):
    err = require_user_role()
    if err:
        return err
    user_id = get_current_user()
    pet = Pet.query.filter_by(id=pet_id, user_id=user_id).first()

    if not pet:
        return jsonify({"error": "Mascota no encontrada"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    if "name" in data:
        pet.name = data["name"].strip()
    if "species" in data:
        pet.species = data["species"].strip()
    if "breed" in data:
        pet.breed = data["breed"]
    if "weight" in data:
        pet.weight = data["weight"]
    if "photo_url" in data:
        pet.photo_url = data["photo_url"]

    if "birth_date" in data:
        if data["birth_date"]:
            try:
                pet.birth_date = datetime.strptime(
                    data["birth_date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                return (
                    jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}),
                    422,
                )
        else:
            pet.birth_date = None

    db.session.commit()

    return (
        jsonify(
            {
                "mensaje": "Mascota actualizada exitosamente",
                "mascota": pet.to_dict(),
            }
        ),
        200,
    )


@jwt_required()
def delete_pet(pet_id):
    err = require_user_role()
    if err:
        return err
    user_id = get_current_user()
    pet = Pet.query.filter_by(id=pet_id, user_id=user_id).first()

    if not pet:
        return jsonify({"error": "Mascota no encontrada"}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"mensaje": "Mascota eliminada exitosamente"}), 200
