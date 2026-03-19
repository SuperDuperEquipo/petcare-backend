from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active     = db.Column(db.Boolean, default=True, nullable=False)
    role          = db.Column(db.String(20), nullable=False, default="user")
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at    = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    #Relación de 1:M entre usuario y mascota
    pets = db.relationship("Pet", backref="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "name":       self.name,
            "email":      self.email,
            "role":       self.role,
            "is_active":  self.is_active,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.email}>"