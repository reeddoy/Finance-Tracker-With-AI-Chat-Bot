# Finance Tracker

Finance Tracker is a task assignment and financial tracking web application built using Flask for the backend and JWT for secure authentication. This project enables users to manage their finances efficiently by tracking tasks and related transactions.

## 🚀 Live Demo
🔗 [Finance Tracker Live](https://reeddoy.github.io/Finance_Tracker_Frontend/)

## 🛠️ Technologies Used
- **Backend:** Flask (Python)
- **Authentication:** JWT (JSON Web Tokens)
- **Frontend:** Raw Html, Css, Javascript (Hosted separately)
- **Database:** SQLite / PostgreSQL (depending on configuration)
- **API:** RESTful APIs built with Flask

## 📌 Features
- User authentication and authorization using JWT
- Add Expense Category
- Expense filter with Day, month
- AI Chatbot with Finance user record
- AI Chatbot which has the ability to set budget
- Secure API endpoints for user and finance management


## 📦 Installation & Setup
### Prerequisites
- Python 3.x installed
- Virtual environment (optional but recommended)

### Clone the Repository
```bash
 git clone https://github.com/reeddoy/Finance-Tracker-With-AI-Chat-Bot.git
 cd Finance-Tracker-With-AI-Chat-Bot
```

### Set Up Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirement.txt
```

### Run Migrations (If using a database like PostgreSQL)
```bash
flask db upgrade
```

### Start the Application
```bash
python app.py
or
flask run
```
The server will run on `http://127.0.0.1:5000/`

## 🔐 API Endpoints
### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Authenticate user and return JWT
- `POST /auth/logout` - Logout user

### Dashboard Api
- `GET /api/check_dashboard` - Get Dashboard Information
- `POST /chat` - AI Chatbot API

### Budget Management
- `GET /api/check_budget` - Check Current Budget
- `POST /api/set_budget` - Add or Set Monthly Budget

### Category Management
- `GET /api/category_list` - Get the category list
- `POST /api/category_add` - Create/Add new category 
- `DELETE /category_delete/<int:category_id>` - Delete a category

### Expense Management
- `GET /api/expense_list` - Get the Expense list
- `GET /api/expense_filter_list` - Get the Expense Filter
- `POST /api/add_expense` - Create/Add new Expense
- `DELETE /delete_expense/<int:id>` - Delete an Expense

## 🛡 Security Measures
- JWT-based authentication for secure API access
- Password hashing using bcrypt
- Different users get different dashboards with filtered user data

## 🎯 Future Enhancements
- Dashboard with graphical financial reports
- Multi-user collaboration with team finance tracking
- Integration with third-party financial APIs
- Mobile app version


## 📧 Contact
For any inquiries or support, feel free to reach out:
- **Developer:** Arif Elahi
- **Email:** [reeddoy@gmail.com]
- **GitHub:** [reeddoy](https://github.com/reeddoy)

