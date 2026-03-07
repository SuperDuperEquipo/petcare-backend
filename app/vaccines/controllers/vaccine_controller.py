from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.vaccines.models.vaccine import Vaccine


@jwt_required()
def get_vaccines(pet_id):
    vaccines = Vaccine.query.filter_by(pet_id=pet_id).all()
    return (
        jsonify(
            {
                "mensaje": "Vacunas obtenidas exitosamente",
                "vacunas": [vaccine.to_dict() for vaccine in vaccines],
            }
        ),
        200,
    )


@jwt_required()
def create_vaccine(pet_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    vaccine = Vaccine(
        name=data.get("name"),
        vet=data.get("vet"),
        next_dose=(
            datetime.fromisoformat(data["next_dose"]) if data.get("next_dose") else None
        ),
        pet_id=pet_id,
    )

    db.session.add(vaccine)
    db.session.commit()

    return (
        jsonify(
            {
                "mensaje": "Vacuna registrada exitosamente",
                "vacuna": vaccine.to_dict(),
            }
        ),
        201,
    )


@jwt_required()
def get_vaccine(vaccine_id):
    vaccine = Vaccine.query.filter_by(id=vaccine_id).first()

    if not vaccine:
        return jsonify({"error": "Vacuna no encontrada"}), 404

    return (
        jsonify(
            {
                "mensaje": "Vacuna obtenida exitosamente",
                "vacuna": vaccine.to_dict(),
            }
        ),
        200,
    )


@jwt_required()
def update_vaccine(vaccine_id):

    vaccine = Vaccine.query.filter_by(id=vaccine_id).first()

    if not vaccine:
        return jsonify({"error": "Vacuna no encontrada"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    if "name" in data:
        vaccine.name = data["name"].strip()
    if "vet" in data:
        vaccine.vet = data["vet"].strip()
    if "next_dose" in data:
        vaccine.next_dose = (
            datetime.fromisoformat(data["next_dose"]) if data.get("next_dose") else None
        )

    db.session.commit()

    return (
        jsonify(
            {
                "mensaje": "Vacuna actualizada exitosamente",
                "vacuna": vaccine.to_dict(),
            }
        ),
        200,
    )


@jwt_required()
def delete_vaccine(vaccine_id):
    vaccine = Vaccine.query.filter_by(id=vaccine_id).first()

    if not vaccine:
        return jsonify({"error": "Vacuna no encontrada"}), 404

    db.session.delete(vaccine)
    db.session.commit()

    return jsonify({"mensaje": "Vacuna eliminada exitosamente"}), 200
