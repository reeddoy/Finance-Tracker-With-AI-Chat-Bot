from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Budget, Expense, db
from sqlalchemy import func
from datetime import datetime


budget = Blueprint('budget', __name__)

budgets = {}

@budget.route('/set_budget', methods=['POST'])
@jwt_required()
def set_budget():
    user_id = get_jwt_identity()
    data = request.json
    budget_amount = data.get("budget")
    
    if not budget_amount:
        return jsonify({"message": "Budget amount is required"}), 400

    # Check if the user already has a budget set
    existing_budget = Budget.query.filter_by(user_id=user_id).first()

    if existing_budget:
        # If a budget already exists, update it
        existing_budget.amount = budget_amount
        db.session.commit()
        return jsonify({"message": f"Budget updated to ${budget_amount}"}), 200
    else:
        # If no budget exists, create a new one
        new_budget = Budget(user_id=user_id, amount=budget_amount)
        db.session.add(new_budget)
        db.session.commit()
        return jsonify({"message": f"Budget set to ${budget_amount}"}), 201





@budget.route('/check_budget', methods=['GET'])
@jwt_required()
def check_budget():
    user_id = get_jwt_identity()  # Get the logged-in user's ID
    
    # Query the Budget table for the user's budget
    user_budget = Budget.query.filter_by(user_id=user_id).first()
    
    if user_budget:
        # If a budget exists, return the budget details
        return jsonify({
            "budget": user_budget.amount,
            "message": "Budget found"
        }), 200
    else:
        # If no budget is set, return a message indicating no budget is set
        return jsonify({
            "message": "No budget set for this user"
        }), 404
    





@budget.route('/check_dashboard', methods=['GET'])
@jwt_required()
def check_dashboard_budget():
    user_id = get_jwt_identity()  # Get the logged-in user's ID
    # Get the current month and year
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Query the Budget table for the user's budget
    user_budget = Budget.query.filter_by(user_id=user_id).first()
    user_total_expense = Expense.query.filter_by(user_id=user_id)

    # Query to get the total expense for the current month
    user_total_expense = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        func.extract('year', Expense.date) == current_year,
        func.extract('month', Expense.date) == current_month
    ).scalar()

    # If no expense is found for the current month, set to 0
    user_total_expense = user_total_expense or 0

    current_balance = user_budget.amount - user_total_expense
    
    return jsonify({
        "budget": user_budget.amount,
        "total_expense": user_total_expense,
        "available_balance" : current_balance
    }), 200
