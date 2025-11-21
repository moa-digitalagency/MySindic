# Shabaka Syndic - Projet Replit

## Overview

**Shabaka Syndic** is a Progressive Web App (PWA) designed for condominium management in the Moroccan market. It aims to modernize property management for syndics (superadmins) and residents, offering a mobile-first, responsive experience. Key capabilities include automating administrative tasks like fund calls and charge distribution, facilitating communication, and providing comprehensive tools for managing units, finances, maintenance, news, and general assemblies. The project focuses on user-friendly design and robust functionality to streamline condominium operations.

## Recent Changes (November 21, 2025)

### CSS Border-Radius Standardization
- Fixed critical CSS bug where `rounded-[10px]-[10px]` typo prevented border-radius from applying correctly
- Standardized all border-radius values to **uniform 10px** across all templates (buttons, inputs, cards, modals)
- Preserved special cases: badges (9999px for pill shape) and loading spinner (50% for circular shape)
- Updated both inline styles and Tailwind CSS classes to use consistent 10px border-radius

### Role-Based Access Control (RBAC) Implementation
- Implemented comprehensive RBAC in `admin_base.html` with proper menu filtering:
  - **Super Admin**: Dashboard, Actualités, Résidences, Utilisateurs, Finances, Maintenance, Carnet d'Entretien, Assemblées, Documents, Paramètres + Quick action "Nouvelle Résidence"
  - **Bureau Syndic (admin)**: Dashboard, Actualités, Résidences, Utilisateurs, Finances, Maintenance, Carnet d'Entretien, Assemblées, Documents, Paramètres
- Implemented RBAC in `resident_base.html` with role-specific menu visibility:
  - **Owner**: Dashboard, Actualités, Maintenance, Finances, Assemblées, Documents
  - **Resident**: Dashboard, Actualités, Maintenance (request/tracking only)
- All role checks use User model helper methods: `is_superadmin()`, `is_admin()`, `is_owner()`, `is_resident()`

### Demo Data Refresh
- Created `clean_and_recreate_demo.py` script to safely delete and recreate demo data
- Recreated demo accounts with correct role assignments:
  - **superadmin@shabaka.ma** (password: Superadmin123!)
  - **syndic@shabaka.ma** (password: Syndic123!)
  - **proprietaire@shabaka.ma** (password: Proprietaire123!)
  - **resident@shabaka.ma** (password: Resident123!)

## User Preferences

- **Workflow:** Iterative development is preferred.
- **Documentation:** The `PROJECT_TRACKING.md` file must always be read and updated before and after any major modification. This file is the reference document for project tracking. Mark tasks as completed once done and add new tasks identified during development.
- **Coding Style:** All comments and documentation should be in French.
- **Communication:** Provide clear and detailed explanations.
- **Interaction:** Ask for confirmation before making significant architectural changes or adding new external dependencies.

## System Architecture

Shabaka Syndic is built as a PWA with a Python Flask backend and an HTML/CSS frontend utilizing Tailwind CSS. PostgreSQL serves as the database.

### UI/UX Decisions

- **Design Approach:** Mobile-first, responsive design using Tailwind CSS, featuring a social network-like interface for residents.
- **Unified Admin Interface:** Modern admin dashboard with a reusable base template (`admin_base.html`), persistent sidebar navigation, gradient stat cards, and consistent layouts.
- **Residence Creation Wizard:** A multi-step wizard for creating residences, including basic information, division type selection, dynamic unit configuration, and admin assignment.
- **Icons:** Feather Icons and emojis for modern iconography.
- **Frontend Framework:** Vanilla JavaScript for client-side interactions.
- **Responsive Design:** Two-column layout for desktop (feed + sidebar) and bottom navigation with tabs for mobile.
- **Modern Design System:** Rounded corners, soft shadows, gradient buttons, smooth transitions, pastel colors, and card-based layouts with hover animations.
- **Button Design Standards:** Consistent solid borders (2px, **uniform 10px border-radius**) for all clickable buttons. Informational blocks use dashed borders. Primary actions are indigo, secondary actions are green/orange, with hover effects. Special cases: badges use 9999px for pill shape, loading spinner uses 50% for circular shape.

### Technical Implementations

- **Backend:** Flask framework with SQLAlchemy ORM, Flask-Migrate for database migrations, Flask-Login for user sessions, Flask-CORS for CORS support, and PyJWT for authentication tokens. Gunicorn is the WSGI server.
- **Frontend Architecture:** Template inheritance system using reusable base templates like `admin_base.html` to reduce code duplication.
- **Data Models:** 19 core data models covering users, residences, financial management, maintenance (with tracking, comments, and documents), communication, general assemblies, and litigation.
- **Business Services:** Includes `ChargeCalculator` for automated charge distribution and `NotificationService` for email notifications.
- **API Structure:**
    - **Admin Routes (`/api/admin/*`):** Comprehensive CRUD operations and dashboards for superadmins, including a transactional residence creation wizard and management of admin assignments, news, and maintenance requests.
    - **Resident Routes (`/api/resident/*`):** Secure, personalized dashboards for residents, including maintenance request tracking.
- **Role Management System:** Supports `superadmin`, `admin`, `owner`, and `resident` roles with dedicated interfaces and permission checks.

### Roles & Permissions

#### 1. Super Admin (`superadmin`)
- **Droits complets** : Accès à toutes les fonctionnalités de la plateforme
- **Gestion des résidences** : Créer une résidence et assigner un ou plusieurs membres du bureau syndic
- **Gestion globale** : Visualiser et gérer toutes les résidences, tous les utilisateurs, toutes les données

#### 2. Bureau Syndic (`admin`)
- **Gestion de résidences** : Gérer les résidences qui leur sont assignées
- **Gestion des utilisateurs** : Ajouter et gérer les propriétaires et résidents de leurs résidences
- **Assemblées générales** : Créer, gérer et suivre les assemblées générales
- **Maintenances** : Gérer les demandes de maintenance et le carnet d'entretien
- **Finances** : Gérer les charges, appels de fonds, paiements
- **Documents** : Gérer les documents de la résidence
- **Communications** : Publier des actualités pour informer les résidents

#### 3. Propriétaire (`owner`)
- **Assemblées générales** : Accès et participation aux AG de sa résidence
- **Gestion des résidents** : Créer, ajouter, bloquer et supprimer un résident dans son unité
- **Fil d'actualités** : Consulter les actualités de sa résidence
- **Maintenances** : Faire des demandes de maintenance et suivre leur statut
- **Finances** : Consulter les charges de son unité et l'historique des paiements
- **Documents** : Consulter les documents de la résidence

#### 4. Résident (`resident`)
- **Fil d'actualités** : Consulter les actualités de sa résidence
- **Maintenances** : Faire des demandes de maintenance et suivre leur statut uniquement
- **Accès limité** : Pas d'accès aux finances, assemblées générales ou documents

### System Design Choices

- **Database:** PostgreSQL for native Replit integration, ACID compliance, and scalability.
- **Backend Framework:** Flask chosen for its lightweight, flexible nature, and suitability for REST APIs.
- **Modularity:** Flask Blueprints used for clear separation of concerns.
- **Shared Services:** Business logic encapsulated for reusability and testability.
- **Security:** Implements password hashing, secure sessions, authorization decorators, server-side validation, environment variables for secrets, and transaction management with rollback.
- **Automatic Database Initialization:** Automatically detects an empty database on startup and seeds it with comprehensive demo data for zero manual setup.

## External Dependencies

- **PostgreSQL:** Primary relational database (via Replit Database).
- **Flask:** Python web framework.
- **SQLAlchemy:** Python ORM.
- **Flask-Migrate:** Database migration tool.
- **Flask-Login:** User session management.
- **Flask-CORS:** Cross-Origin Resource Sharing support.
- **PyJWT:** JSON Web Token implementation.
- **Werkzeug:** Password hashing and security utilities.
- **psycopg2-binary:** PostgreSQL adapter for Python.
- **Gunicorn:** WSGI HTTP server.
- **Tailwind CSS:** Utility-first CSS framework.
- **Feather Icons:** Open-source icon library.