# Shabaka Syndic - Projet Replit

## Overview

**Shabaka Syndic** is a Progressive Web App (PWA) designed for condominium management in the Moroccan market. It aims to modernize property management for syndics (superadmins) and residents, offering a mobile-first, responsive experience. Key capabilities include automating administrative tasks like fund calls and charge distribution, facilitating communication, and providing comprehensive tools for managing units, finances, maintenance, news, and general assemblies. The project focuses on user-friendly design and robust functionality to streamline condominium operations.

## Recent Changes (November 21, 2025)

### Dual News Feed System Implementation
- Implemented two separate news feed types with role-based access control:
  - **Fil d'actualité** (feed): Accessible to all users (super admin, bureau syndic, propriétaires, résidents)
  - **Actualités et annonces** (announcement): Restricted to super admin, bureau syndic, and propriétaires only
- Added `news_type` field to News model ('feed' or 'announcement')
- Created separate frontend pages for both feed types (admin/feed.html, admin/announcements.html, resident/feed.html, resident/announcements.html)
- Updated navigation menus to display both feeds as separate menu items with appropriate role-based visibility
- Implemented proper access control at both route and API levels (403 Forbidden for unauthorized access)

### Role-Based Access Control (RBAC) Complete Implementation
- Comprehensive RBAC system with four distinct user roles and specific menu access for each:
  - **Super Admin**: Dashboard Super Admin, Fil d'actualité, Actualités et annonces, Résidences (create/view/assign admins), Utilisateurs, Finances, Maintenance, Carnet d'Entretien, Assemblées, Documents, Paramètres + Quick action "Nouvelle Résidence"
  - **Bureau Syndic (admin)**: Dashboard Syndic, Fil d'actualité, Actualités et annonces, Résidences (view assigned only, cannot create/modify/delete), Utilisateurs, Finances (approve payments), Maintenance, Carnet d'Entretien, Assemblées, Documents, Paramètres (view only)
  - **Propriétaire (owner)**: Dashboard Propriétaire, Fil d'actualité, Actualités et annonces, Maintenance, Finances, Assemblées, Documents
  - **Résident**: Dashboard Résident, Fil d'actualité (feed only), Maintenance (request and tracking only)
- All role checks use User model helper methods with precise role validation
- Role badge visible in user interface for all roles

### Demo Data Creation & Documentation
- Updated `clean_and_recreate_demo.py` script to create comprehensive demo data including:
  - 4 user accounts (one for each role)
  - 1 residence with 5 units
  - 4 news articles (2 feed + 2 announcements)
- New demo account credentials:
  - **superadmin@shabaka.ma** (password: Super123!)
  - **syndic@shabaka.ma** (password: Syndic123!)
  - **proprietaire@shabaka.ma** (password: Owner123!)
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
**Tous les droits sur la plateforme** - Le seul rôle avec droits complets

**Menus accessibles :**
- 📊 Dashboard Super Admin
- 📱 Fil d'actualité (accessible à tous)
- 📰 Actualités et annonces (super admin, syndic, propriétaires uniquement)
- 🏢 Résidences (voir toutes les résidences de la plateforme, créer, modifier, assigner bureau syndic)
- 👥 Utilisateurs
- 💰 Finances
- 🔧 Maintenance
- 📝 Carnet d'Entretien
- 🗳️ Assemblées
- 📄 Documents
- ⚙️ Paramètres
- 🚪 Déconnexion

**Action rapide :** 🏗️ Nouvelle Résidence (seul le super admin peut créer des résidences)

**Droits spécifiques :**
- Voir toutes les résidences de la plateforme
- Créer une résidence et assigner un ou plusieurs membres du bureau syndic
- Gestion globale de toutes les données

#### 2. Bureau Syndic (`admin`)
**Gestion opérationnelle des résidences assignées**

**Menus accessibles :**
- 📊 Dashboard Syndic
- 📱 Fil d'actualité (accessible à tous)
- 📰 Actualités et annonces (super admin, syndic, propriétaires uniquement)
- 🏢 Résidences (voir uniquement les résidences assignées - **ne peut pas créer/modifier/supprimer**)
- 👥 Utilisateurs (ajouter et gérer propriétaires/résidents)
- 💰 Finances (gérer charges, appels de fonds, **approuver déclarations de paiement après vérification**)
- 🔧 Maintenance
- 📝 Carnet d'Entretien
- 🗳️ Assemblées (créer, gérer et suivre les assemblées générales)
- 📄 Documents
- ⚙️ Paramètres (consultation uniquement)
- 🚪 Déconnexion

**Rôle visible :** Le rôle "Bureau Syndic" est affiché dans l'interface utilisateur

**Droits spécifiques :**
- Gère uniquement sa/ses résidences assignées
- Seul à pouvoir approuver les déclarations de paiement après vérification
- Publier des actualités pour informer les résidents

#### 3. Propriétaire (`owner`)
**Propriétaire d'un logement dans la résidence**

**Menus accessibles :**
- 📊 Dashboard Propriétaire
- 📱 Fil d'actualité (accessible à tous)
- 📰 Actualités et annonces (super admin, syndic, propriétaires uniquement)
- 🔧 Maintenance (demande, commentaire et suivi)
- 💰 Finances (consulter charges de son unité et historique des paiements)
- 🗳️ Assemblées (accès et participation aux AG de sa résidence)
- 📄 Documents (consulter les documents de la résidence)
- 🚪 Déconnexion

**Droits spécifiques :**
- Créer/ajouter/bloquer/supprimer un résident dans son unité
- Participer aux assemblées générales

#### 4. Résident (`resident`)
**Résident locataire d'un logement** - Accès limité

**Menus accessibles :**
- 📊 Dashboard Résident
- 📱 Fil d'actualité (accessible à tous - **PAS d'accès aux Actualités et annonces**)
- 🔧 Maintenance (demande, commentaire et suivi uniquement)
- 🚪 Déconnexion

**Restrictions :**
- ❌ Pas d'accès aux Actualités et annonces
- ❌ Pas d'accès aux finances
- ❌ Pas d'accès aux assemblées générales
- ❌ Pas d'accès aux documents

### Dual News Feed System

**Fil d'actualité** (news_type='feed')
- Accessible à **tous les utilisateurs** (super admin, bureau syndic, propriétaires, résidents)
- Actualités générales de la résidence (horaires, événements, informations pratiques)
- Menu séparé dans la navigation

**Actualités et annonces** (news_type='announcement')
- Accessible uniquement à **super admin, bureau syndic, et propriétaires**
- Résidents bloqués avec erreur 403 Forbidden
- Annonces officielles (convocations AG, appels de fonds, décisions importantes)
- Menu séparé dans la navigation

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