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

### Project Structure

Le projet est organisé en deux dossiers principaux:
- **`backend/`**: Code Python Flask (models, routes, utils, config)
- **`frontend/`**: Interface utilisateur (static assets et templates HTML)

### UI/UX Decisions

- **Design Approach:** Mobile-first and responsive design using Tailwind CSS for a modern aesthetic. Interface réseau social pour les résidents.
- **Icons:** Feather Icons et emojis pour une iconographie moderne.
- **Frontend Framework:** Vanilla JavaScript for client-side interactions.
- **Responsive Design:**
  - Desktop: Layout à 2 colonnes (feed + sidebar)
  - Mobile: Navigation en bas de page avec onglets
- **Modern Design System:** Rounded corners, soft shadows, gradient buttons, smooth transitions, pastel colors, and card-based layouts with hover animations.

### Technical Implementations

- **Backend:** Flask is the web framework, with SQLAlchemy as the ORM. Flask-Migrate handles database migrations, Flask-Login manages user sessions, and Flask-CORS provides CORS support. PyJWT is used for authentication tokens. Gunicorn is the WSGI server.
- **Data Models:** 16 core data models cover users, residences, financial management, maintenance, communication, documents, general assemblies, and litigation.
- **Business Services:**
    - **ChargeCalculator:** Automates charge distribution.
    - **NotificationService:** Centralized service for sending email notifications.
- **API Structure:**
    - **Admin Routes (`/api/admin/*`):** Comprehensive CRUD operations and dashboards for superadmins.
    - **Resident Routes (`/api/resident/*`):** Secure, personalized dashboards for residents.
- **Role Management System:** Supports `superadmin`, `admin`, `owner`, `resident` roles with dedicated management interfaces and permission checks.

### System Design Choices

- **Database:** PostgreSQL for native Replit integration, ACID support, and scalability.
- **Backend Framework:** Flask for its lightweight, flexible nature, suitability for REST APIs, and rich ecosystem.
- **Modularity:** Flask Blueprints for clear separation of concerns.
- **Shared Services:** Business logic encapsulated for reusability and testability.
- **Security:** Password hashing, secure sessions, authorization decorators, server-side validation, environment variables for secrets, and transaction management with rollback.
- **Automatic Database Initialization:** The application automatically detects an empty database on startup and seeds it with comprehensive demo data, including various user roles, residences, financial entries, and maintenance requests. This ensures zero manual setup on deployment.

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
- **Tailwind CSS:** Utility-first CSS framework.
- **Feather Icons:** Open-source icon library.