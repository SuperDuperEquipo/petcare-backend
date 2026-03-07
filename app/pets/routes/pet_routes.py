from flask import Blueprint
from app.pets.controllers.pet_controller import (
    get_pets,
    create_pet,
    get_pet,
    update_pet,
    delete_pet,
)

pets_bp = Blueprint("pets", __name__)

pets_bp.get("")(get_pets)
pets_bp.post("")(create_pet)
pets_bp.get("/<int:pet_id>")(get_pet)
pets_bp.put("/<int:pet_id>")(update_pet)
pets_bp.delete("/<int:pet_id>")(delete_pet)