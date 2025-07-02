# Streamlit User Management System

This is a modular and scalable user management system built with **Streamlit**. It supports **user registration**, **login with JWT authentication**, and a **dashboard interface** that can be extended with custom widgets.

---

## Project Structure
```
streamlit_user_management/
│
├── src/
│ ├── database/
│ │ ├── init.py
│ │ ├── database.py # Database connection and setup
│ │ └── models.py # SQLAlchemy models
│ │
│ ├── ui/
│ │ ├── init.py
│ │ ├── components.py # Reusable UI components
│ │ ├── managers.py # Authentication and session logic
│ │ ├── pages.py # Login, register, and dashboard pages
│ │ └── services.py # Backend services used by the UI
│ │
│ ├── settings.py # Environment configuration and constants
│ ├── .env # Actual environment variables (not committed)
│ ├── example.env # Example .env file
│
├── streamlit_main.py # Entry point for the Streamlit app
├── requirements.txt # Required Python packages
├── .gitignore # Git ignored files
└── README.md # Project documentation
```

---

## Features

- ✅ User registration with secure password hashing
- ✅ JWT-based login system
- ✅ Persistent sessions
- ✅ Dashboard page after login
- ✅ Easily extendable with custom dashboard widgets

---

## 🔧 Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/mariusciurea/streamlit_user_management.git
cd streamlit_user_management
```

2. **Create a virtual environment**
```bash
python -m venv env
source env\Scripts\activate 
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a .env file based on example.env:

```bash
cp example.env .env
```

## Running the App

Once everything is set up, start the Streamlit app with:

```bash
streamlit run streamlit_main.py
```

## Scalability

This app is designed with modularity and scalability in mind. After the user logs in, they are redirected to a dashboard page. 
This dashboard can easily be extended with custom widgets or components, making it ideal for admin panels, analytics apps, 
or any Streamlit-based UI that requires user authentication.

