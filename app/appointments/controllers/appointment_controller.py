from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.core.extensions import db
from app.appointments.models.appointment import Appointment
from app.pets.models.pet import Pet
from datetime import datetime


def require_user_role():
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "Acceso restringido para dueños de mascotas"}), 403
    return None


@jwt_required()
def get_appointments():
    err = require_user_role()
    if err: return err

    current_user_id = int(get_jwt_identity())

    appointments = (
        Appointment.query
        .join(Pet)
        .filter(Pet.user_id == current_user_id)
        .all()
    )

    return jsonify({
        "mensaje": "Citas obtenidas exitosamente",
        "citas": [appointment.to_dict() for appointment in appointments],
        "total": len(appointments),
    }), 200


@jwt_required()
def create_appointment():
    err = require_user_role()
    if err: return err

    current_user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    title = data.get("title", "").strip()
    #date = data.get("date")
    #time = data.get("time")
    type_ = data.get("type", "").strip()
    pet_id = data.get("pet_id")
    try:
        date = datetime.strptime(data.get("date", ""), "%Y-%m-%d").date()
        time = datetime.strptime(data.get("time", ""), "%H:%M:%S").time()
    except ValueError:
        return jsonify({"error": "Formato de fecha u hora inválido. Use YYYY-MM-DD y HH:MM:SS"}), 422

    if not title or not date or not time or not type_ or not pet_id:
        return jsonify({"error": "title, date, time, type y pet_id son obligatorios"}), 422

    pet = Pet.query.filter_by(id=pet_id, user_id=current_user_id).first()
    if not pet:
        return jsonify({"error": "Mascota no encontrada o no pertenece al usuario"}), 404

    appointment = Appointment(
        title=title,
        date=date,
        time=time,
        type=type_,
        description=data.get("description"),
        pet_id=pet_id
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({
        "mensaje": "Cita creada exitosamente",
        "cita": appointment.to_dict(),
    }), 201


@jwt_required()
def get_appointment(appointment_id):
    err = require_user_role()
    if err: return err

    current_user_id = int(get_jwt_identity())

    appointment = (
        Appointment.query
        .join(Pet)
        .filter(Appointment.id == appointment_id)
        .filter(Pet.user_id == current_user_id)
        .first()
    )

    if not appointment:
        return jsonify({"error": "Cita no encontrada"}), 404

    return jsonify({
        "mensaje": "Cita obtenida exitosamente",
        "cita": appointment.to_dict(),
    }), 200


@jwt_required()
def update_appointment(appointment_id):
    err = require_user_role()
    if err: return err

    current_user_id = int(get_jwt_identity())

    appointment = (
        Appointment.query
        .join(Pet)
        .filter(Appointment.id == appointment_id)
        .filter(Pet.user_id == current_user_id)
        .first()
    )

    if not appointment:
        return jsonify({"error": "Cita no encontrada"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "El cuerpo de la petición debe ser JSON"}), 400

    if "title" in data: appointment.title = data["title"].strip()
    #if "date" in data: appointment.date = data["date"]
    #if "time" in data: appointment.time = data["time"]
    if "type" in data: appointment.type = data["type"].strip()
    if "description" in data: appointment.description = data["description"]

    try:
        if "date" in data: appointment.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if "time" in data: appointment.time = datetime.strptime(data["time"], "%H:%M:%S").time()
    except ValueError:
        return jsonify({"error": "Formato de fecha u hora inválido. Use YYYY-MM-DD y HH:MM:SS"}), 422

    db.session.commit()

    return jsonify({
        "mensaje": "Cita actualizada exitosamente",
        "cita": appointment.to_dict(),
    }), 200


@jwt_required()
def delete_appointment(appointment_id):
    err = require_user_role()
    if err: return err

    current_user_id = int(get_jwt_identity())

    appointment = (
        Appointment.query
        .join(Pet)
        .filter(Appointment.id == appointment_id)
        .filter(Pet.user_id == current_user_id)
        .first()
    )

    if not appointment:
        return jsonify({"error": "Cita no encontrada"}), 404

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({
        "mensaje": "Cita eliminada exitosamente"
    }), 200
