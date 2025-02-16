from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Category

category = Blueprint('category', __name__)

# Add Category
@category.route('/category_add', methods=['POST'])
@jwt_required()
def add_category():
    user_id = get_jwt_identity()
    data = request.json


    new_category = Category(
        user_id=user_id,
        name=str(data["category"]),
    )
    
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify({"message": "Category added successfully!"}), 201


# List Categories
@category.route('/category_list', methods=['GET'])
@jwt_required()
def list_categories():
    user_id = get_jwt_identity()
    categories = Category.query.filter_by(user_id=user_id).all()

    return jsonify({
        "categories": [
            {"name": cat.name, "date": cat.date.strftime('%Y-%m-%d'),"id":cat.id}
            for cat in categories
        ]
    })


# Delete Category
@category.route('/category_delete/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    user_id = get_jwt_identity()
    
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({"message": "Category deleted successfully!"}), 200
