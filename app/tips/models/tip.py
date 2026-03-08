from datetime import datetime, timezone
from app.core.extensions import db

class Tip(db.Model):
    __tablename__ = "tips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    species = db.Column(db.String(50), nullable=False)       
    category = db.Column(db.String(50), nullable=False)     
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

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.title,
            "contenido": self.content,
            "especie": self.species,
            "categoria": self.category,
            "creado_en": self.created_at.isoformat(),
            "actualizado_en": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Tip {self.title}>"