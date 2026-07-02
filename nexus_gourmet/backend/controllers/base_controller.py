from flask import jsonify

class BaseController:
    def init(self, app):
        self.app = app

    def json_response(self, success=True, message=None, data=None, status=200):
        """Padroniza todas as respostas da API em JSON"""
        response = {"success": success}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data
            
        return jsonify(response), status
