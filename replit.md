# MySindic - Projet Replit

## Overview

**MySindic** is a Progressive Web App (PWA) designed for condominium management in the Moroccan market. It provides a comprehensive solution for syndics (superadmins) and residents, aiming to modernize property management, offer a mobile-first and responsive experience, automate administrative tasks like fund calls and charge distribution, and facilitate communication between all stakeholders.

## User Preferences

- **Workflow:** Iterative development is preferred.
- **Documentation:** The `PROJECT_TRACKING.md` file must always be read and updated before and after any major modification. This file is the reference document for project tracking. Mark tasks as completed once done and add new tasks identified during development.
- **Coding Style:** All comments and documentation should be in French.
- **Communication:** Provide clear and detailed explanations.
- **Interaction:** Ask for confirmation before making significant architectural changes or adding new external dependencies.

## System Architecture

MySindic is built as a PWA with a Python Flask backend and an HTML/CSS frontend utilizing Tailwind CSS. PostgreSQL is used for the database, integrated via Replit Database.

### UI/UX Decisions

- **Design Approach:** Mobile-first and responsive design using Tailwind CSS for a modern aesthetic.
- **Icons:** Feather Icons are used for modern iconography.
- **Frontend Framework:** Vanilla JavaScript for client-side interactions.
- **PWA Features (Future):** Service Worker, manifest, and offline mode are planned for a native-like mobile experience.

### Technical Implementations

- **Backend:** Flask serves as the web framework, with SQLAlchemy as the ORM for database interactions. Flask-Migrate handles database migrations, Flask-Login manages user sessions, and Flask-CORS provides CORS support. PyJWT is used for authentication tokens. Gunicorn is the WSGI server for production.
- **Data Models:** The application features 16 core data models covering users, residences, financial management (charges, payments), maintenance, communication (news, polls), documents, general assemblies, and litigation.
- **Business Services:**
    - **ChargeCalculator:** Automatically calculates charge distribution based on tantièmes, lot balances, unpaid charges, and payment tracking.
    - **NotificationService:** Centralized service for sending email notifications for maintenance requests, fund calls, and general assemblies.
- **API Structure:**
    - **Admin Routes (`/api/admin/*`):** Comprehensive CRUD operations and dashboards for superadmins, covering residences, units, charges, payments, news, maintenance, general assemblies, litigation, polls, and user management.
    - **Resident Routes (`/api/resident/*`):** Secure, personalized dashboards for residents to view news, create and track maintenance requests, manage finances, participate in polls and general assemblies, and access documents and maintenance logs.

### System Design Choices

- **Database:** PostgreSQL was chosen for its native Replit integration, ACID transaction support, scalability, and ability to handle complex relationships.
- **Backend Framework:** Flask was selected for its lightweight, flexible nature, suitability for REST APIs, and rich ecosystem.
- **Modularity:** Flask Blueprints are used to organize routes, ensuring clear separation of concerns (auth, admin, resident) and promoting modular, maintainable code.
- **Shared Services:** Business logic is encapsulated in shared services (e.g., `ChargeCalculator`, `NotificationService`) for reusability, testability, and clear separation of concerns.
- **Security:**
    - Password hashing with Werkzeug.
    - Secure sessions with Flask-Login.
    - Authorization decorators (`@login_required`, `@superadmin_required`).
    - All resident endpoints verify `residence_id` to prevent horizontal privilege escalation.
    - Foreign keys are derived from `current_user` to avoid trusting client input.
    - Server-side validation and authorization are enforced on all endpoints.
    - Transactions with rollback on errors are used for database operations.
    - Environment variables are used for secrets (`SESSION_SECRET`, `DATABASE_URL`).

## External Dependencies

- **PostgreSQL:** Primary relational database, accessed via Replit Database.
- **Flask:** Python web framework.
- **SQLAlchemy:** Python ORM for database interaction.
- **Flask-Migrate:** Database migration tool.
- **Flask-Login:** User session management.
- **Flask-CORS:** Cross-Origin Resource Sharing support.
- **PyJWT:** JSON Web Token implementation.
- **Werkzeug:** Password hashing and security utilities.
- **psycopg2-binary:** PostgreSQL adapter for Python.
- **Gunicorn:** WSGI HTTP server.
- **Tailwind CSS:** Utility-first CSS framework (via CDN).
- **Feather Icons:** Open-source icon library.

## Recent Changes

### October 24, 2025 - Project Migration to Replit Environment

- Successfully migrated MySindic application from Replit Agent to Replit environment
- Installed Python 3.11 and all required dependencies via `uv` package manager
- Created PostgreSQL database and configured DATABASE_URL environment variable
- Set up SESSION_SECRET and SECRET_KEY environment variables
- Configured deployment with gunicorn on port 5000
- Created workflow "Start application" to run the app with auto-reload
- Initialized database with sample data using init_db.py
- Created demo accounts:
  - Superadmin: admin@mysindic.ma / Admin123!
  - Resident: resident@mysindic.ma / Resident123!
- Verified application is fully functional and accessible

## Environment Setup

### Required Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (automatically set by Replit)
- `SESSION_SECRET`: Secret key for Flask sessions (automatically set)
- `SECRET_KEY`: Application secret key (uses SESSION_SECRET value)
- `FLASK_ENV`: Set to 'development' for local development

### Running the Application

The application runs automatically via the configured workflow. To manually start:

```bash
uv run gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### Database Initialization

To reset and initialize the database with sample data:

```bash
uv run python init_db.py
```

This creates sample residences, units, and demo user accounts.