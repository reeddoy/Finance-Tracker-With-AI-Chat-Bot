from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Expense, db
from datetime import datetime, timedelta
from sqlalchemy import func

expense = Blueprint('expense', __name__)

@expense.route('/add_expense', methods=['POST'])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.json
    date_string = data['date']
    date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
    new_expense = Expense(
        user_id=user_id,
        amount=data['amount'],
        category=data['category'],
        description=data.get('description', ''),
        payment_method=data['payment_method'],
        date=date_obj
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added!"})

@expense.route('/expense_list', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify({
        "expenses": [
            {
                "id": exp.id,
                "amount": exp.amount,
                "category": exp.category,
                "description": exp.description,
                "date": exp.date.strftime('%Y-%m-%d'),
                "payment_method": exp.payment_method
            } for exp in expenses
        ]
    })

@expense.route('/delete_expense/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.get(id)
    if expense and expense.user_id == user_id:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted"})
    return jsonify({"error": "Expense not found or unauthorized"}), 403




@expense.route('/expense_filter_list', methods=['GET'])
@jwt_required()
def expense_filter_list():
    user_id = get_jwt_identity()
    filter_type = request.args.get('filter', '')  # Get filter type
    start_date = request.args.get('start_date', '')  # For custom date range
    end_date = request.args.get('end_date', '')  # For custom date range

    # Get current date for 1 month, 3 months, and current year filters
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    if filter_type == '1-month':
        start_date = current_date - timedelta(days=30)
        end_date = current_date
    elif filter_type == '3-months':
        start_date = current_date - timedelta(days=90)
        end_date = current_date
    elif filter_type == 'current-year':
        start_date = datetime(current_year, 1, 1)
        end_date = current_date
    elif filter_type == 'date-range' and start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        return jsonify({"message": "Invalid filter type or missing dates"}), 400

    expenses = Expense.query.filter_by(user_id=user_id).filter(
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()

    # Calculate the total amount
    total_amount = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).scalar() or 0  # Default to 0 if no expenses are found

    # Convert expenses to a list of dictionaries
    expense_data = [{
        'category': expense.category,
        'description': expense.description,
        'amount': expense.amount,
        'date': expense.date.strftime('%Y-%m-%d'),
        'payment_method': expense.payment_method
    } for expense in expenses]

    return jsonify({
        'expenses': expense_data,
        'total_amount': total_amount
    })
