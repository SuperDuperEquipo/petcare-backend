from datetime import datetime, timezone
from app.core.extensions import db

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    pet = db.relationship("Pet", backref="appointments")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.title,
            "fecha": self.date.isoformat(),
            "tipo": self.type,
            "descripcion": self.description,
            "id_mascota": self.pet_id,
            "creado_en": self.created_at.isoformat(),
            "actualizado_en": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Appointment {self.title}>"