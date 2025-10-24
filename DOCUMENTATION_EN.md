# MySindic Documentation - English Version

**Version:** 0.1.0  
**Date:** October 24, 2025  
**Language:** English 🇬🇧

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Architecture](#architecture)
6. [API Reference](#api-reference)
7. [Deployment](#deployment)
8. [Maintenance](#maintenance)
9. [FAQ](#faq)

---

## 🎯 Introduction

### What is MySindic?

MySindic is a Progressive Web App (PWA) for property management specifically designed for the Moroccan market. It provides a modern, mobile-friendly, and comprehensive solution to manage all aspects of condominium administration.

### Main Features

#### For Superadmins (Property Managers)
- 🏢 **Property Management**: Create and manage multiple residences
- 💰 **Financial Control**: Financial dashboards and indicators
- 🔧 **Work Management**: Planning and tracking interventions
- 💳 **Payment Collection**: Payment tracking and automatic reminders
- ⚖️ **Litigation Management**: Dispute handling
- 📝 **Maintenance Log**: Complete intervention history
- 🗳️ **General Assemblies**: Organization and management of GAs
- 📧 **Fund Calls**: Automatic editing and sending
- 📊 **Charge Distribution**: Automatic calculation

#### For Residents
- 📢 **News**: Real-time information
- 🔧 **Maintenance Requests**: Create and track interventions
- 📊 **Polls**: Participate in important decisions
- 📄 **Documents**: Access to receipts and official documents

---

## 💻 Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL
- Node.js (for frontend tools)
- Git

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd MySindic

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your values

# Initialize database
flask db init
flask db migrate
flask db upgrade

# Start the application
python backend/app.py
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file at the project root:

```env
# Flask Configuration
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your_very_long_and_secure_secret_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mysindic

# Email (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password

# VPS Configuration
VPS_PORT=5006
```

### Database Configuration

MySindic uses PostgreSQL. Make sure you have created the database:

```sql
CREATE DATABASE mysindic;
CREATE USER mysindic_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE mysindic TO mysindic_user;
```

---

## 🚀 Usage

### Starting the Application

#### Development Mode (Replit)
```bash
python backend/app.py
```
The application will be accessible at `http://0.0.0.0:5000`

#### Production Mode (VPS)
Use the deployment script:
```bash
chmod +x deploy_vps.sh
./deploy_vps.sh
```
The application will be accessible on port 5006

### Accessing the Application

1. **Homepage**: `/`
2. **Login**: `/login`
3. **Superadmin Dashboard**: `/admin/dashboard`
4. **Resident Dashboard**: `/resident/dashboard`

### Getting Started

1. **Create a Superadmin Account**
   - Go to `/register`
   - Fill in the information
   - Confirm via email

2. **Create a Residence**
   - Log in as Superadmin
   - Go to "Residence Management"
   - Click "New Residence"

3. **Add Residents**
   - In the residence, go to "Residents"
   - Click "Add Resident"
   - Send invitation

---

## 🏗️ Architecture

### Project Structure

```
MySindic/
├── backend/
│   ├── app.py              # Flask entry point
│   ├── config.py           # Configuration
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # API routes
│   ├── utils/              # Utility functions
│   ├── static/             # CSS, JS, images
│   └── templates/          # HTML templates
├── frontend/
│   ├── css/               # Tailwind styles
│   ├── js/                # JavaScript
│   └── images/            # Images
└── docs/                  # Documentation
```

### Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Vanilla)
- **Database**: PostgreSQL
- **Authentication**: Flask-Login, JWT
- **PWA**: Service Workers, Web App Manifest

---

## 🔌 API Reference

### Authentication

#### POST `/api/auth/login`
User login

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**Response:**
```json
{
  "success": true,
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "superadmin"
  }
}
```

### Residence Management

#### GET `/api/residences`
Get list of residences

**Response:**
```json
{
  "success": true,
  "residences": [
    {
      "id": 1,
      "name": "Al Andalous Residence",
      "address": "Casablanca, Morocco",
      "units": 45
    }
  ]
}
```

*(Complete API documentation coming soon)*

---

## 🌐 Deployment

### VPS Deployment

The `deploy_vps.sh` script automates deployment:

```bash
# Make the script executable
chmod +x deploy_vps.sh

# Launch deployment
./deploy_vps.sh
```

**The script automatically:**
1. Pulls code from Git
2. Checks/creates virtual environment
3. Activates environment
4. Checks/creates .env file
5. Installs dependencies
6. Starts application on port 5006

### Replit Deployment

The application is configured to work directly on Replit:
- Port: 5000 (mandatory)
- Workflow configured automatically
- Integrated PostgreSQL database

---

## 🔧 Maintenance

### Updates

```bash
# Update code
git pull origin main

# Update dependencies
pip install -r backend/requirements.txt --upgrade

# Apply migrations
flask db upgrade
```

### Backups

Regular backups are recommended for:
- PostgreSQL database
- Uploaded files
- .env file

### Logs

Logs are stored in:
- `logs/app.log`: Application logs
- `logs/error.log`: Errors only

---

## ❓ FAQ

### How to reset a user's password?
Via Superadmin dashboard > Users > Select user > Reset password

### How to add a new residence?
Superadmin Dashboard > Residences > New Residence

### Is the application mobile-compatible?
Yes, MySindic is a PWA optimized for mobile and can be installed as a native app.

### How to contact support?
Email: support@mysindic.ma

---

## 📞 Support

For any questions or issues:
- 📧 Email: support@mysindic.ma
- 📱 Phone: +212 XXX XXX XXX
- 🌐 Website: www.mysindic.ma

---

**Last Updated:** October 24, 2025  
**Version:** 0.1.0
