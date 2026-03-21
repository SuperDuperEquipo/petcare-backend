from flask import Blueprint
from app.auth.controllers.auth_controller import (
    get_profile,
    register,
    login,
    logout,
    update_profile,
)

auth_bp = Blueprint("auth", __name__)

auth_bp.post("/register")(register)
auth_bp.post("/login")(login)
auth_bp.post("/logout")(logout)

auth_bp.get("/profile")(get_profile)
auth_bp.put("/profile")(update_profile)
