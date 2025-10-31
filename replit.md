# Shabaka Syndic - Projet Replit

## Overview

**Shabaka Syndic** is a Progressive Web App (PWA) designed for condominium management in the Moroccan market. It provides a comprehensive solution for syndics (superadmins) and residents, aiming to modernize property management, offer a mobile-first and responsive experience, automate administrative tasks like fund calls and charge distribution, and facilitate communication between all stakeholders.

## Recent Changes (October 31, 2025)

### Import to Replit Environment Completed ✅
- PostgreSQL database created and initialized
- Demo data loaded successfully (4 users, 1 residence, 5 units, 3 maintenance requests)
- Workflow configured and running on port 5000
- All backend APIs tested and functional
- Frontend templates verified and operational

### Access Credentials
```
Super Admin: admin@mysindic.ma / Admin123!
Admin Syndic: admin.syndic@mysindic.ma / Admin123!
Résident 1: resident@mysindic.ma / Resident123!
Résident 2: karim@mysindic.ma / Resident123!
Propriétaire: owner@mysindic.ma / Owner123!
```

## User Preferences

- **Workflow:** Iterative development is preferred.
- **Documentation:** The `PROJECT_TRACKING.md` file must always be read and updated before and after any major modification. This file is the reference document for project tracking. Mark tasks as completed once done and add new tasks identified during development.
- **Coding Style:** All comments and documentation should be in French.
- **Communication:** Provide clear and detailed explanations.
- **Interaction:** Ask for confirmation before making significant architectural changes or adding new external dependencies.

## System Architecture

Shabaka Syndic is built as a PWA with a Python Flask backend and an HTML/CSS frontend utilizing Tailwind CSS. PostgreSQL is used for the database, integrated via Replit Database.

### Project Structure

Le projet est organisé en deux dossiers principaux:
- **`backend/`**: Code Python Flask (models, routes, utils, config)
- **`frontend/`**: Interface utilisateur (static assets et templates HTML)

### UI/UX Decisions

- **Design Approach:** Mobile-first and responsive design using Tailwind CSS for a modern aesthetic. Interface réseau social pour les résidents.
- **Unified Admin Interface:** Modern admin dashboard with reusable base template (`admin_base.html`) featuring persistent sidebar navigation, gradient stat cards, and consistent layouts. All admin pages extend this base template using block inheritance for maintainability and DRY principles.
- **Residence Creation Wizard:** Multi-step fluid wizard for creating residences with:
  - Step 1: Basic residence information
  - Step 2: Division type selection (lot, immeuble, bâtiment, zone)
  - Step 3: Unit configuration with dynamic forms
  - Step 4: Admin assignment to residences
- **Icons:** Feather Icons et emojis pour une iconographie moderne.
- **Frontend Framework:** Vanilla JavaScript for client-side interactions.
- **Responsive Design:**
  - Desktop: Layout à 2 colonnes (feed + sidebar)
  - Mobile: Navigation en bas de page avec onglets
- **Modern Design System:** Rounded corners, soft shadows, gradient buttons, smooth transitions, pastel colors, and card-based layouts with hover animations.
- **Button Design Standards (Oct 2025):** 
  - All clickable buttons use solid borders (2px) with consistent border-radius (8-10px)
  - Informational/decorative blocks retain dashed borders for visual hierarchy
  - Primary actions: Indigo buttons, secondary actions: green/orange variants
  - Hover effects with background color transitions and subtle transforms

### Technical Implementations

- **Backend:** Flask is the web framework, with SQLAlchemy as the ORM. Flask-Migrate handles database migrations, Flask-Login manages user sessions, and Flask-CORS provides CORS support. PyJWT is used for authentication tokens. Gunicorn is the WSGI server.
- **Frontend Architecture:** Template inheritance system with reusable base templates:
  - `admin_base.html`: Unified admin shell with persistent sidebar, header, and quick actions
  - Block structure: `admin_content`, `admin_extra_css`, `admin_extra_js` for page-specific content
  - Eliminates code duplication across all 9 admin pages (including news management)
- **Data Models:** 19 core data models cover users, residences, residence-admin assignments, financial management, maintenance (with tracking numbers, comments, and documents), communication, documents, general assemblies, and litigation.
- **Business Services:**
    - **ChargeCalculator:** Automates charge distribution.
    - **NotificationService:** Centralized service for sending email notifications.
- **API Structure:**
    - **Admin Routes (`/api/admin/*`):** Comprehensive CRUD operations and dashboards for superadmins.
      - **Residence Creation Wizard (`/api/admin/residences/wizard`):** Transactional endpoint that creates residence, units, and admin assignments in a single commit with rollback on failure.
      - **Admin Assignment Routes:** CRUD operations for managing many-to-many admin-residence assignments.
      - **News Management (`/admin/news`):** Superadmin interface for viewing and publishing actualités (Oct 2025)
      - **Maintenance Management (Oct 2025):** Full-featured system with unique tracking numbers, comments with @mentions, document attachments, residence filtering, and admin assignment workflow.
    - **Resident Routes (`/api/resident/*`):** Secure, personalized dashboards for residents with maintenance request tracking.
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