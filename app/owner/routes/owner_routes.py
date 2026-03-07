from flask import Blueprint
from app.owner.controllers.owner_controller import (
    get_owners,
    create_owner,
    get_owner,
    update_owner,
    delete_owner,
    assign_owner_to_pet
)

owners_bp = Blueprint("owners", __name__)

owners_bp.get("/owners")(get_owners)
owners_bp.post("/owners")(create_owner)
owners_bp.get("/owners/<int:owner_id>")(get_owner)
owners_bp.put("/owners/<int:owner_id>")(update_owner)
owners_bp.delete("/owners/<int:owner_id>")(delete_owner)
owners_bp.post("/pets/<int:pet_id>/owners/<int:owner_id>")(assign_owner_to_pet)