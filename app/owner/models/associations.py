from app.core.extensions import db

#Relación muchos a muchos entre Ower y Pet
pet_owner = db.Table(
    "pet_owner",
    db.Column("pet_id", db.Integer, db.ForeignKey("pets.id"), primary_key=True),
    db.Column("owner_id",db.Integer, db.ForeignKey("owners.id"), primary_key=True)
)