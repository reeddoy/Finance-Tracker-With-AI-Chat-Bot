from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import google.generativeai as genai
import json
from models import db, Category, Expense, Budget
from datetime import datetime, timedelta



# Create a Blueprint for home routes
home_route = Blueprint('home', __name__)

GEMINI_API_KEY = "AIzaSyD2aaDrAfDtPXtKAmenn8OTF0K0ILwM0_c"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

# Define a route for the home page
@home_route.route('/')
def home():
    return 'Server is running'



def query_expenses(user_id, start_date=None, end_date=None, category=None):
    """Fetch expenses based on the provided filters."""
    query = Expense.query.filter_by(user_id=user_id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    if category:
        query = query.filter(Expense.category == category)
    return query.all()



# @home_route.route('/chat', methods=['POST'])
# @jwt_required()
# def chat():
#     user_id = get_jwt_identity()
#     data = request.json
#     message = data.get("message", "").strip()

#     if not message:
#         return jsonify({"error": "Message is required"}), 400

#     # **Fetch expenses and categories from the database**
#     expenses = Expense.query.filter_by(user_id=user_id).all()
#     categories = Category.query.filter_by(user_id=user_id).all()
#     budget = Budget.query.filter_by(user_id=user_id).first()

#     # Convert expenses and categories to JSON format
#     expense_data = [{"date": e.date.strftime("%Y-%m-%d"), "category": e.category, "amount": e.amount} for e in expenses]
#     category_data = [{"name": c.name} for c in categories]
#     budget_amount = budget.amount if budget else "No budget set"

#     # **Pass expense data to AI**
#     CHAT_CONTEXT = f"""
#     You are Finance AI Assistant, developed by Arif Elahi. 
#     You help users manage expenses and budgets. 
#     The user has provided this message: "{message}"
    
#     **User Expense Data:**
#     Expenses: {json.dumps(expense_data, indent=2)}
#     Categories: {json.dumps(category_data, indent=2)}
#     Budget: {budget_amount}

#     **Instructions:**
#     - If the user asks about expenses, filter the data and respond.
#     - If the user asks about setting a budget, confirm or update their budget.
#     - If no relevant expense data is found, politely inform the user.

#     Example queries:
#     - "What was my total expense in January?"
#     - "List all my expenses for food."
#     - "Set my monthly budget to $1000."
#     """

#     # **Send to AI model**
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(CHAT_CONTEXT)

#     bot_reply = response.text if response.text else "I'm sorry, I couldn't process that."

#     return jsonify({"response": bot_reply})






import re

@home_route.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.json
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # **Check for Budget Update Command Before Sending to AI**
    # budget_change_match = re.search(r"set (?:my )?budget to (\d+)", message, re.IGNORECASE)
    budget_change_match = re.search(
    r"(?:set(?: my| the| a)?(?: monthly)? budget(?: to)?|budget(?: set| change| should be| is| make it)?)\s?\$?(\d+)", 
    message, 
    re.IGNORECASE
)


    if budget_change_match:
        new_budget_amount = int(budget_change_match.group(1))

        # **Update or Set the Budget in Database**
        existing_budget = Budget.query.filter_by(user_id=user_id).first()

        if existing_budget:
            existing_budget.amount = new_budget_amount
        else:
            new_budget = Budget(user_id=user_id, amount=new_budget_amount)
            db.session.add(new_budget)

        db.session.commit()

        return jsonify({"response": f"Budget successfully updated to ${new_budget_amount}."})

    # **Fetch expenses, categories, and budget**
    expenses = Expense.query.filter_by(user_id=user_id).all()
    categories = Category.query.filter_by(user_id=user_id).all()
    budget = Budget.query.filter_by(user_id=user_id).first()

    # Convert data to JSON format
    expense_data = [{"date": e.date.strftime("%Y-%m-%d"), "category": e.category, "amount": e.amount} for e in expenses]
    category_data = [{"name": c.name} for c in categories]
    budget_amount = budget.amount if budget else "No budget set"
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # **Pass expense data to AI**
    CHAT_CONTEXT = f"""
    You are Finance AI Assistant, developed by Arif Elahi. 
    You help users manage expenses and budgets. 
    The user has provided this message: "{message}"
    
    **User Expense Data:**
    Expenses: {json.dumps(expense_data, indent=2)}
    Categories: {json.dumps(category_data, indent=2)}
    Budget: {budget_amount}
    Current Date & Time: {current_datetime}

    **Instructions:**
    - Respond naturally as a chatbot.
    - If the user asks about expenses, filter the data and respond.
    - If the user asks about the budget, provide the latest amount.
    - DO NOT return structured JSON unless explicitly requested.
    """

    # **Send to AI model**
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(CHAT_CONTEXT)

    bot_reply = response.text if response.text else "I'm sorry, I couldn't process that."

    return jsonify({"response": bot_reply})