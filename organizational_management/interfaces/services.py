from flask import Blueprint, request, jsonify
from flasgger import swag_from

from organizational_management.application.services import OrganizationalManagementService

organizational_management_api = Blueprint('organizational_management', __name__)

organizational_management_service = OrganizationalManagementService()

"""
Endpoint a hotel associated with an owner.
"""
@organizational_management_api.route('/organizational_management/hotel', methods=['GET'])
@swag_from({
    'tags': ['Organizational Management'],
})
def get_hotel_by_owner_id():
    """
    Retrieves a hotel associated with an owner.
    ---
    parameters:
      - in: query
        name: owner_id
        type: integer
        required: true
        description: The ID of the owner to retrieve the hotel for.
    responses:
      200:
        description: Hotel retrieved successfully
      404:
        description: Hotel not found
      500:
        description: Internal server error
    """
    
    owner_id = request.args.get('owner_id', type=int)
    
    if not owner_id:
        return jsonify({"error": "Owner ID is required"}), 400
    
    try:
        hotel = organizational_management_service.get_hotel_by_owner_id(owner_id)
        
        if not hotel:
            return jsonify({"error": "Hotel not found"}), 404
        
        return jsonify(hotel.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

