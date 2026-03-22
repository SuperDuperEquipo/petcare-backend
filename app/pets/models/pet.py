from datetime import datetime, timezone
from app.core.extensions import db


class Pet(db.Model):
    __tablename__ = "pets"

<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
=======
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    species     = db.Column(db.String(50), nullable=False)
    breed       = db.Column(db.String(100), nullable=True)
    birth_date  = db.Column(db.Date, nullable=True)
    weight      = db.Column(db.Float, nullable=True)
    photo_url   = db.Column(db.String(255), nullable=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at  = db.Column(
>>>>>>> Stashed changes
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.name,
            "especie": self.species,
            "raza": self.breed,
            "fecha_nacimiento": (
                self.birth_date.isoformat() if self.birth_date else None
            ),
            "peso": self.weight,
            "foto_url": self.photo_url,
            "user_id": self.user_id,
            "creado_en": self.created_at.isoformat(),
            "actualizado_en": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Pet {self.name}>"
