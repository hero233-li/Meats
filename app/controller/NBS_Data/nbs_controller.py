from flask import jsonify

from app.common.nbs_com.NBS_MEMU_config import PRO_CONFIG
class NBSDataController:
    def __init__(self):
        pass
    @staticmethod
    def get_category():
        config = "National_menu_config.yaml"
        pro_conf = PRO_CONFIG.get_menu_config(config_file=config)
        menu_data = [
            item.to_frontend_json()
            for item in pro_conf.nbs_config.values()
        ]
        return menu_data


if __name__ == '__main__':
    nbs_controller = NBSDataController()
    nbs_controller.get_category()