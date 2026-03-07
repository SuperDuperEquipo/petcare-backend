from flask import Blueprint
from app.appointments.controllers.appointment_controller import (
    get_appointments,
    create_appointment,
    get_appointment,
    update_appointment,
    delete_appointment,
)

appointments_bp = Blueprint("appointments", __name__)

appointments_bp.get("")(get_appointments)
appointments_bp.post("")(create_appointment)
appointments_bp.get("/<int:appointment_id>")(get_appointment)
appointments_bp.put("/<int:appointment_id>")(update_appointment)
appointments_bp.delete("/<int:appointment_id>")(delete_appointment)