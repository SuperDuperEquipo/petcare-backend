from flask import Blueprint
from app.admin.controllers.admin_controller import get_users, delete_user

admin_bp = Blueprint("admin", __name__)

admin_bp.get("/users")(get_users)
admin_bp.delete("/users/<int:id>")(delete_user)