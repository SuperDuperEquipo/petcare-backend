from datetime import datetime, timezone
from app.core.extensions import db


class Vaccine(db.Model):
    __tablename__ = "vaccines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_applied = db.Column(
        db.Date, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    next_dose = db.Column(db.Date)  # Puede o no tener una siguiente dosis.
    vet = db.Column(db.String(100), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "date_applied": (
                self.date_applied.isoformat() if self.date_applied else None
            ),
            "next_dose": self.next_dose.isoformat() if self.next_dose else None,
            "pet_id": self.pet_id,
            "vet": self.vet,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Vaccine {self.name}>"
