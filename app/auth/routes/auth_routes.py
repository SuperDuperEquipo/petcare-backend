from flask import Blueprint
from app.auth.controllers.auth_controller import register, login, logout

auth_bp = Blueprint("auth", __name__)

auth_bp.post("/register")(register)
auth_bp.post("/login")(login)
auth_bp.post("/logout")(logout)