from app.core.extensions import db
from app.owner.models.associations import pet_owner

class Owner(db.Model):
    __tablename__ = "owners"

    id      =      db.Column(db.Integer, primary_key=True)
    name    =      db.Column(db.String(100), nullable=False)
    phone   =      db.Column(db.String(50), nullable=False)
    address =      db.Column(db.String(125), nullable=False)
    user_id =      db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    user = db.relationship("User", backref="owner")
    pets = db.relationship("Pet", secondary= pet_owner, back_populates= "owners")

    def to_dict(self):
        return{
            "id":       self.id,
            "nombre":   self.name,
            "contacto": self.phone,
            "dirección": self.address,
            "user_id": self.user_id,
            "pets": [
                {
                    "id": pet.id,
                    "nombre": pet.name
                }
                for pet in self.pets
            ]
        }
    
    def __repr__(self):
        return f"<Owner {self.name}>"



