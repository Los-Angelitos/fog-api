from flask import Blueprint
from flasgger import swag_from
from iam.interfaces.services import create_device_request, get_all_devices_by_room_id_request

iam = Blueprint('iam', __name__)

@iam.route('/sign-up', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'device_id': {
                        'type': 'string',
                        'example': 'abc123'
                    }
                },
                'required': ['device_id']
            }
        }
    ],
    'responses': {
        201: {'description': 'Successful operation'},
        400: {'description': 'Invalid input'},
        401: {'description': 'Unauthorized'}
    }
})
def auth():
   """
    Authenticate the device by its ID.
    ---
    responses:
        200:
            description: Successful operation
        401:
            description: Unauthorized
    """
   return create_device_request()

@iam.route('/devices',methods=['GET'])
@swag_from({
    'tags': ['Devices'],
    'parameters': [
        {
            'name': 'roomId',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'ID of the room to fetch devices from'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of devices in the specified room',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Device'
                }
            }
        },
        400: {
            'description': 'Missing or invalid roomId parameter'
        }
    }
})
def get_all_devices_by_room_id():
    """
    Get all devices by room ID
    ---
    Fetches all devices associated with a specific room using the roomId query parameter.
    """
    return get_all_devices_by_room_id_request()