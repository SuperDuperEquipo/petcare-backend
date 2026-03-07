from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.pets.models.pet import Pet

@jwt_required()
def get_pets():
    current_user_id = int(get_jwt_identity())
    pets = Pet.query.filter_by(owner_id=current_user_id).all()
    return jsonify({
        "mensaje": "Mascotas obtenidas exitosamente",
        "mascotas": [pet.to_dict() for pet in pets],
        "total": len(pets),
    }), 200


@jwt_required()
def create_pet():
    current_user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    name    = data.get("name", "").strip()
    species = data.get("species", "").strip()

    if not name or not species:
        return jsonify({"error": "El nombre y la especie son obligatorios"}), 422

    pet = Pet(
        name = name,
        species = species,
        breed = data.get("breed"),
        birth_date = data.get("birth_date"),
        weight = data.get("weight"),
        photo_url = data.get("photo_url"),
        owner_id = current_user_id,
    )

    db.session.add(pet)
    db.session.commit()

    return jsonify({
        "mensaje": "Mascota creada exitosamente",
        "mascota": pet.to_dict(),
    }), 201


@jwt_required()
def get_pet(pet_id):
    current_user_id = int(get_jwt_identity())
    pet = Pet.query.filter_by(id=pet_id, owner_id=current_user_id).first()

    if not pet:
        return jsonify({"error": "Mascota no encontrada"}), 404

    return jsonify({
        "mensaje": "Mascota obtenida exitosamente",
        "mascota": pet.to_dict(),
    }), 200


@jwt_required()
def update_pet(pet_id):
    current_user_id = int(get_jwt_identity())
    pet = Pet.query.filter_by(id=pet_id, owner_id=current_user_id).first()

    if not pet:
        return jsonify({"error": "Mascota no encontrada"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    if "name" in data: pet.name = data["name"].strip()
    if "species" in data: pet.species = data["species"].strip()
    if "breed" in data: pet.breed = data["breed"]
    if "birth_date" in data: pet.birth_date = data["birth_date"]
    if "weight" in data: pet.weight = data["weight"]
    if "photo_url" in data: pet.photo_url = data["photo_url"]

    db.session.commit()

    return jsonify({
        "mensaje": "Mascota actualizada exitosamente",
        "mascota": pet.to_dict(),
    }), 200


@jwt_required()
def delete_pet(pet_id):
    current_user_id = int(get_jwt_identity())
    pet = Pet.query.filter_by(id=pet_id, owner_id=current_user_id).first()

    if not pet:
        return jsonify({"error": "Mascota no encontrada"}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({"mensaje": "Mascota eliminada exitosamente"}), 200