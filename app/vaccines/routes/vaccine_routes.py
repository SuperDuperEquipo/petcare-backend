from flask import Blueprint
from app.vaccines.controllers.vaccine_controller import (
    get_vaccines,
    create_vaccine,
    get_vaccine,
    update_vaccine,
    delete_vaccine,
)

vaccine_bp = Blueprint("vaccine", __name__)

vaccine_bp.get("/pets/<int:pet_id>/vaccines")(get_vaccines)
vaccine_bp.post("/pets/<int:pet_id>/vaccines")(create_vaccine)
vaccine_bp.get("/vaccines/<int:vaccine_id>")(get_vaccine)
vaccine_bp.put("/vaccines/<int:vaccine_id>")(update_vaccine)
vaccine_bp.delete("/vaccines/<int:vaccine_id>")(delete_vaccine)
