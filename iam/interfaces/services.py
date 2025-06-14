from dataclasses import asdict
from flask import Blueprint, request, jsonify

from iam.application.services import AuthApplicationService
iam_api = Blueprint('iam', __name__)

auth_service = AuthApplicationService()

def authenticate_request():
    retrieved_device_id = request.json.get('device_id') if request.json else None
    api_key = request.headers.get('X-API-Key')
    if not retrieved_device_id or not api_key:
        return jsonify({"error": "Missing device_id or API key"}), 401
    if not auth_service.authenticate(retrieved_device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401
    return None

def create_device_request():
    """
    Register or authenticate a device with device_id and api_key.
    """
    body = request.get_json()

    if not body or 'device_id' not in body:
        return jsonify({"error": "Invalid device id."}), 400

    response = auth_service.create_device(body)

    if response:
        device_dict = response.to_dict()
        return jsonify(device_dict), 201
    else:
        return jsonify(), 400