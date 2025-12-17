# Shabaka Syndic - Projet Replit

## Overview

**Shabaka Syndic** is a Progressive Web App (PWA) designed as a comprehensive digital management platform for condominiums (copropriétés) in Morocco. It aims to modernize property management for syndics, administrators, property owners, and residents by offering tools for managing units, finances, maintenance, news, assemblies, and documents with robust role-based access control. The platform provides a complete ecosystem for efficient condominium operations.

## User Preferences

- **Language:** All code comments and documentation in French
- **Workflow:** Iterative development preferred
- **Documentation:** Keep replit.md updated with major changes
- **Communication:** Clear explanations before architectural changes
- **Confirmation:** Ask before adding external dependencies

## System Architecture

The Shabaka Syndic platform is built using a mobile-first, responsive design approach.

**Technology Stack:**
- **Backend:** Flask 3.0.0, PostgreSQL (Replit Database), SQLAlchemy 2.0.23, Flask-Migrate 4.0.5, Flask-Login 0.6.3, PyJWT 2.8.0, Gunicorn 21.2.0, Werkzeug 3.0.1, Flask-Mail 0.9.1, Agora Token Builder.
- **Frontend:** Tailwind CSS (CDN), Feather Icons, Vanilla JS, Jinja2.

**Core Features & Implementations:**

-   **Role-Based Access Control (RBAC):**
    -   **Super Admin:** Full platform access, global data management, residence creation, user management.
    -   **Bureau Syndic / Admin:** Operational management of assigned residences only, financial approvals, assembly creation/management, announcement publishing.
    -   **Propriétaire / Owner:** Property owner access, manage residents in own unit, participate in assemblies, view finances, submit maintenance.
    -   **Résident / Resident:** Tenant access, request and track maintenance, view general news feed.

-   **Residence Management:** Complete CRUD operations for residences and units with a multi-step creation wizard.
-   **General Assembly System:**
    -   Management of ordinary/extraordinary assemblies, scheduling, convocations, attendance tracking, resolution management, and minute generation.
    -   **Live Assembly Integration:** Real-time video/audio conferencing via Agora.io (RTC tokens), real-time voting, and cloud recording for online/hybrid sessions.
-   **Voting System:**
    -   **Resolution Voting:** Linked to assemblies with multiple vote types (simple, double majority, unanimity), real-time counting, and attendance verification.
    -   **Polls:** Community surveys with multiple choice, anonymous/named voting, real-time results, and status management.
-   **Maintenance Management:** Full workflow for tracking requests with unique numbers, comments, document attachments, priority levels, status tracking, and technician assignment. Includes a comprehensive Maintenance Log (Carnet d'Entretien) for historical records.
-   **Financial Management:** Charge creation (recurring/one-time) with automatic distribution, payment recording, and approval workflow.
-   **Dual News Feed System:**
    -   **Fil d'actualité (Feed):** General residence information accessible to all users.
    -   **Actualités et annonces (Announcements):** Official communications restricted to Super Admin, Admin, and Owners.
-   **Document Management:** Upload, categorize, and control visibility of documents per residence with role-based access.
-   **Litigation Management:** Tracking legal cases and disputes with status, dates, and related information.

**Project Structure:**
The project is organized into `backend/` and `frontend/` directories. The backend includes `app.py` (Flask app factory), `config.py`, `models/` (22 SQLAlchemy models), `routes/` (API endpoints for auth, admin, resident), `services/` (business logic like charge calculation, notifications, Agora service), and `utils/`. The frontend contains `static/` assets and `templates/` (Jinja2 templates for admin, resident, and authentication views).

**Security Best Practices:**
Password hashing (Werkzeug), secure session management (Flask-Login), SQL injection protection (SQLAlchemy), CORS configuration, environment variables for secrets, role-based authorization decorators, and server-side input validation.

## External Dependencies

-   **PostgreSQL:** Main relational database, hosted via Replit Database.
-   **Agora.io:** Used for Real-Time Communication (RTC) in live General Assemblies (video, audio, RTM messaging). Requires `AGORA_APP_ID` and `AGORA_APP_CERTIFICATE` environment variables.
-   **Flask-Mail:** For email notifications. Requires SMTP server configuration (`MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`).
-   **Tailwind CSS (CDN):** For styling the frontend.
-   **Feather Icons:** For UI iconography.

## Documentation

The `docs/` folder contains comprehensive documentation:

| Document | Description |
|----------|-------------|
| [README.md](docs/README.md) | Overview and quick start guide |
| [GUIDE_UTILISATEUR.md](docs/GUIDE_UTILISATEUR.md) | User manual for all roles |
| [GUIDE_COMMERCIAL.md](docs/GUIDE_COMMERCIAL.md) | Commercial presentation and features |
| [ARCHITECTURE_TECHNIQUE.md](docs/ARCHITECTURE_TECHNIQUE.md) | Technical architecture and code structure |
| [API_REFERENCE.md](docs/API_REFERENCE.md) | Complete REST API documentation |
| [INSTALLATION.md](docs/INSTALLATION.md) | Installation and deployment guide |
| [SECURITE.md](docs/SECURITE.md) | Security measures and best practices |

## Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@mysindic.ma | Admin123! |
| Syndic Admin | admin.syndic@mysindic.ma | Admin123! |
| Owner | owner@mysindic.ma | Owner123! |
| Resident | resident@mysindic.ma | Resident123! |