from flask import request, jsonify
import re
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.pets.models.pet import Pet
from app.owner.models.owner import Owner


#Verificación correcta del celular
PHONE_REGEX = re.compile(r"^\+?[\d\s\-\(\)]{7,50}$")

def _validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))


@jwt_required()
def get_owners():
    owners = Owner.query.all()

    return jsonify({
        "mensaje": "Los dueños han sido obtenidos exitosamente",
        "dueños": [owner.to_dict() for owner in owners],
        "total": len(owners)
    }), 200


@jwt_required()
def create_owner():
    
    current_user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    address = data.get("address", "").strip()

    if not name or not phone or not address:
        return jsonify({"error": "El nombre, el contacto y la dirección son obligatorios"}), 422
    
    if len(name) > 100:
        return jsonify({"error": "El nombre no puede superar 100 caracteres"}), 422
    if len(phone) > 50:
        return jsonify({"error": "El  número de teléfono no puede superar 50 caracteres"}), 422
    if len(address) > 125:
        return jsonify({"error": "La dirección no puede superar 125 caracteres"}), 422
    
    if not _validate_phone(phone):
        return jsonify({"error": "El formato del contacto no es válido"}), 422

    existing_owner = Owner.query.filter_by(user_id=current_user_id).first()
    if existing_owner:
        return jsonify({"error": "Este usuario ya tiene un perfil creado"}), 422

    owner = Owner(
        name=name,
        phone=phone,
        address=address,
        user_id=current_user_id,
    )

    db.session.add(owner)
    db.session.commit()

    return jsonify({
        "mensaje": "El dueño ha sido creado exitosamente",
        "owner": owner.to_dict(),
    }), 201


@jwt_required()
def get_owner(owner_id):
    owner = db.session.get(Owner, owner_id)

    if not owner:
        return jsonify({"error": "El dueño no ha sido encontrado"}), 404

    return jsonify({
        "mensaje": "El dueño ha sido obtenido exitosamente",
        "owner": owner.to_dict(),
    }), 200


@jwt_required()
def update_owner(owner_id):
    current_user_id = int(get_jwt_identity())
    owner = db.session.get(Owner, owner_id)

    if not owner:
        return jsonify({"error": "El dueño no ha sido encontrado"}), 404

    if owner.user_id != current_user_id:
        return jsonify({"error": "No tienes permiso para actualizar este dueño"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    if "name" in data:
        name = data["name"].strip()
        if not name:
            return jsonify({"error": "Este campo no puede estar vacío"}), 422
        owner.name = name
        
    if "phone" in data:
        phone = data["phone"].strip()
        if not phone:
            return jsonify({"error": "Este campo no puede estar vacío"}), 422
        if not _validate_phone(phone):
            return jsonify({"error": "El formato del télefono no es válido"}), 422
        owner.phone = phone
        
    if "address" in data:
        address = data["address"].strip()
        if not address:
            return jsonify({"error": "Este campo no puede estar vacío"}), 422
        owner.address = address

    db.session.commit()

    return jsonify({
        "mensaje": "El dueño ha sido actualizado exitosamente",
        "owner": owner.to_dict()
    }), 200


@jwt_required()
def delete_owner(owner_id):
    current_user_id = int(get_jwt_identity())
    owner = db.session.get(Owner, owner_id)

    if not owner:
        return jsonify({"error": "El dueño no ha sido encontrado"}), 404

    if owner.user_id != current_user_id:
        return jsonify({"error": "No tienes permiso para eliminar este dueño"}), 403

    db.session.delete(owner)
    db.session.commit()

    return jsonify({
        "mensaje": "El dueño ha sido eliminado exitosamente"
    }), 200


@jwt_required()
def assign_owner_to_pet(pet_id, owner_id):
    current_user_id = int(get_jwt_identity())
    current_owner = Owner.query.filter_by(user_id = current_user_id).first()

    if not current_owner:
        return jsonify({"error": "No tienes un perfil de dueño asociado"}), 404
    
    if current_owner.id != owner_id:
        return jsonify({"error": "No puedes asociar otro dueño en tu nombre"}), 403

    pet = db.session.get(Pet, pet_id)
    if not pet:
        return jsonify({"error": "La mascota no ha sido encontrada"}), 404

    owner = db.session.get(Owner, owner_id)
    if not owner:
        return jsonify({"error": "El dueño no ha sido encontrado"}), 404

    if owner in pet.owners:
        return jsonify({"mensaje": "El dueño ya está asociado a la mascota"}), 200

    pet.owners.append(owner)
    db.session.commit()

    return jsonify({
        "mensaje": "El dueño ha sido asociado a la mascota exitosamente",
        "mascota": pet.to_dict(),
    }), 200