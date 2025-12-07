from flask import Blueprint

from app.controller.NBS_Data.nbs_controller import NBSDataController

api_bp = Blueprint('api', __name__,url_prefix='/api/v1')

nbs_controller=NBSDataController()

@api_bp.route('/options/topTree', methods=['POST'])
def top_tree():
    return nbs_controller.get_category()