from flask import jsonify


class ResponseHandler:

    @staticmethod
    def success(data, status_code=200):
        response = {
            'status': 'success',
            'data': data
        }
        return jsonify(response), status_code

    @staticmethod
    def error(message, status_code=400):
        response = {
            'status': 'error',
            'message': message
        }
        return jsonify(response), status_code
