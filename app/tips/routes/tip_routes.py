from flask import Blueprint
from app.tips.controllers.tip_controller import get_tips, create_tip

tips_bp = Blueprint("tips", __name__)

tips_bp.get("")(get_tips)
tips_bp.post("")(create_tip)