from flask import Blueprint
from flasgger import swag_from
from iam.interfaces.services import authenticate_request, get_or_create_device_request

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
   return get_or_create_device_request()