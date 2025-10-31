# Shabaka Syndic

Complete digital solution for property management in Morocco.

## 🎯 Description

Shabaka Syndic is a modern property management platform that facilitates communication between property managers and residents. It offers a complete solution for managing fees, maintenance requests, news, general assemblies, and much more.

## ✨ Key Features

### For Residents
- 📱 **Personalized dashboard** with overview of important information
- 🔧 **Maintenance requests** with real-time tracking
- 💰 **Financial management**: view charges and payments
- 📰 **News** from the residence
- 📄 **Shared documents** from the property manager
- 🗳️ **General assemblies** and online voting

### For Administrators
- 🏢 **Property management** and units
- 👥 **User management** and role assignment
- 💵 **Complete financial management** (charges, payments, fund calls)
- 🔧 **Maintenance tracking** and maintenance log
- 📊 **Detailed statistics and reports**
- ⚖️ **Litigation management**
- 📰 **News publication** and communications

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL
- Modern web browser

### Installation

1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

2. Configure database (automatic on first launch)

3. Run the application:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

## 👤 Demo Accounts

Use these credentials to test different roles:

| Role | Email | Password |
|------|-------|----------|
| **Super Admin** | admin@mysindic.ma | Admin123! |
| **Syndic Admin** | admin.syndic@mysindic.ma | Admin123! |
| **Owner** | owner@mysindic.ma | Owner123! |
| **Resident** | resident@mysindic.ma | Resident123! |

## 📚 Project Structure

```
.
├── backend/               # Backend code (Python/Flask)
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   ├── services/         # Business services
│   ├── app.py           # Flask application
│   └── config.py        # Configuration
├── frontend/             # User interface
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JS, images
│   └── ...
├── documentation/        # Documentation
└── main.py              # Entry point
```

## 🔒 Security

- Secure authentication with password hashing
- CSRF protection
- Server-side data validation
- Role-based access control
- Secure sessions

## 📝 License

© 2025 Shabaka Syndic - All rights reserved
Developed by Aisance KALONJI

## 📧 Contact

For questions or support:
- Email: moa@myoneart.com
- Web: www.myoneart.com
