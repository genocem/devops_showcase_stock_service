"""
Stock routes for inventory management
"""
from flask import Blueprint, jsonify, request
from app.services.stock_service import *

stock_bp = Blueprint('stock', __name__)

error_map = {
    "NOT_UNIQUE_ERROR": 400,
    "VALIDATION_ERROR": 409,
    "NOT_FOUND": 404
}

@stock_bp.route('', methods=['GET'])
def get_stock():
    """Get all products in stock"""
    result = get_all_stock()

    if result["ok"]:
        return jsonify({
            'success': True,
            'products': result['products']
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': result['message']
        }), 500


@stock_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by id"""
    result = get_stock_by_id(product_id)

    if result["ok"]:
        return jsonify({
            'success': True,
            'product': result['product']
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': result['message']
        }), error_map.get(result.get("error", ""), 500)


#  the following will be a an  admin part for adding more stock
#  making a whole authentication system will be too much for a project that has the sole purpose of showcasing devops skill
#  which is why i'm holding off on adding authentification for the time being

# 13/01/2026
# after looking into it more i decided add it eventually cause i want to see how authentification should be handled with traefik and kubernetes api gateway (idk how yet)
# probably gonna have to clean up these route names
@stock_bp.route("", methods=["POST"])
def add_product():
    data = request.get_json() or {}
    price = data.get("price", 0)
    result = create_stock(data["product_name"], data["amount"], price)

    if not result["ok"]:
        return jsonify({
            'success': False,
            'message': result["message"]
        }), error_map.get(result.get("error", ""), 500)
    return jsonify({
    'success': True,
    'message': result["message"]
}), 201

@stock_bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product's stock quantity"""
    data = request.get_json() or {}
    result = update_stock(product_id, data)

    if result["ok"]:
        return jsonify({
            'success': True,
            'message': result['message'],
            'product': result['product']
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': result['message']
        }), error_map.get(result.get("error", ""), 500)


@stock_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product from stock"""
    result = delete_stock(product_id)

    if result["ok"]:
        return jsonify({
            'success': True,
            'message': result['message']
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': result['message']
        }), error_map.get(result.get("error", ""), 500)
