# Changelog - MySindic

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

---

## [Non publié]

### Prochaines étapes
- Développer fonctionnalités PWA avancées (Service Worker, notifications push, mode offline)
- Tests automatisés (unitaires et d'intégration)
- Optimisation des performances et expérience utilisateur
- Déploiement en production (publish sur Replit)

---

## [0.3.0] - 2025-10-24

### Corrigé
- 🐛 **Dashboard administrateur**
  - Correction incompatibilité frontend/backend pour le chargement des statistiques
  - Modification du JavaScript pour utiliser `data.stats` au lieu de `data.data`
  - Ajout d'appels API séparés pour charger les demandes de maintenance et paiements récents
  - Correction du calcul du taux de recouvrement

- 🐛 **Système de déconnexion**
  - Erreur "Method Not Allowed" corrigée sur /api/auth/logout
  - Problème : liens HTML utilisaient GET au lieu de POST
  - Solution : Ajout de la fonction JavaScript `MySindic.logout()` pour faire un POST
  - Conversion des liens `<a>` en boutons `<button>` avec `onclick="MySindic.logout()"`
  - Déconnexion fonctionnelle sur desktop et mobile

- 🐛 **Dashboard résident**
  - Correction de l'erreur de chargement des statistiques
  - Modification de l'accès aux données (data.maintenance_requests, data.news, data.balance)
  - Correction du chargement des charges impayées via /api/resident/charges/unpaid
  - Affichage des charges impayées dans un tableau avec titre, date d'échéance et montant

### Ajouté
- 🗄️ **Migration Replit complète**
  - Création de la base de données PostgreSQL Replit
  - Configuration des variables d'environnement (DATABASE_URL, SESSION_SECRET, SECRET_KEY)
  - Installation de tous les packages via uv (pyproject.toml)
  - Configuration du workflow "Start application" sur port 5000
  - Initialisation de la base de données avec script init_db.py

- 👥 **Comptes de démonstration**
  - Compte superadmin : admin@mysindic.ma / Admin123!
  - Compte résident : resident@mysindic.ma / Resident123!
  - Résidence de test : "Résidence Les Jardins"
  - Unité de test : A101

- 📝 **Documentation mise à jour**
  - PROJECT_TRACKING.md mis à jour avec les corrections
  - CHANGELOG.md mis à jour avec la version 0.3.0
  - replit.md mis à jour avec les détails de la migration

### Testé
- ✅ Application démarre correctement sur Replit (port 5000)
- ✅ Base de données PostgreSQL connectée et opérationnelle
- ✅ Authentification fonctionnelle (login/logout)
- ✅ Dashboard administrateur affiche correctement les statistiques
- ✅ Dashboard résident affiche correctement les données
- ✅ Déconnexion fonctionne sur desktop et mobile
- ✅ Tous les endpoints API fonctionnels

### Notes techniques
- **Migration** : De Replit Agent vers environnement Replit standard
- **Base de données** : PostgreSQL (Replit Database) avec 16 modèles
- **Frontend** : Corrections JavaScript pour compatibilité API
- **Backend** : Aucune modification nécessaire, API déjà conforme
- **Workflow** : Gunicorn avec --reload pour développement

---

## [0.2.0] - 2025-10-24

### Ajouté
- 🗄️ **Modèles de données complets** (12 modèles SQLAlchemy)
  - `User` : Gestion des utilisateurs (superadmin/resident) avec authentification
  - `Residence` : Gestion des copropriétés
  - `Unit` : Gestion des lots/appartements avec tantièmes
  - `MaintenanceRequest` : Demandes d'intervention
  - `Document` : Documents officiels (quittances, PV, etc.)
  - `Charge` & `ChargeDistribution` : Gestion et répartition des charges
  - `Payment` : Suivi des paiements
  - `News` : Actualités de la résidence
  - `Poll`, `PollOption`, `PollVote` : Système de sondages complet
  - Relations SQLAlchemy cohérentes avec cascading rules
  - Méthodes to_dict() pour sérialisation JSON

- ⚙️ **Configuration Flask professionnelle** (`backend/config.py`)
  - Trois environnements : Development, Production, Testing
  - Configuration SQLAlchemy, JWT, Flask-Login, Email
  - Validation des secrets en production
  - Gestion sécurisée des clés

- 🔐 **Système d'authentification complet** (`backend/routes/auth.py`)
  - Flask-Login intégré avec sessions sécurisées
  - Endpoints : `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
  - Endpoints : `/api/auth/me`, `/api/auth/check`
  - Hashing des mots de passe avec Werkzeug
  - Gestion des rôles (superadmin/resident)
  - Mise à jour automatique de last_login

- 👨‍💼 **Routes Superadmin** (`backend/routes/admin.py`)
  - Dashboard avec statistiques globales
  - Gestion des résidences (liste, création)
  - Gestion des utilisateurs
  - Décorateur `@superadmin_required` pour la sécurité
  - Endpoints : `/api/admin/dashboard`, `/api/admin/residences`, `/api/admin/users`

- 🏠 **Routes Résidents** (`backend/routes/resident.py`)
  - Dashboard personnalisé avec demandes et actualités
  - Création et suivi des demandes de maintenance
  - Consultation des actualités de la résidence
  - Endpoints : `/api/resident/dashboard`, `/api/resident/maintenance`, `/api/resident/news`

- 🏗️ **Architecture améliorée**
  - Factory pattern pour l'application Flask
  - Blueprints pour organisation modulaire
  - Gestion centralisée des erreurs (404, 500)
  - Health check avec test de connexion DB
  - Support CORS configuré
  - Flask-Migrate intégré pour les migrations

### Modifié
- 🐍 **Application Flask** (`backend/app.py`)
  - Intégration complète de la configuration
  - Enregistrement automatique des blueprints
  - Initialisation de la base de données
  - User loader pour Flask-Login
  - Création automatique des tables en développement

### Testé
- ✅ Application démarre sans erreur
- ✅ Tous les endpoints API sont accessibles
- ✅ Connexion à la base de données fonctionnelle
- ✅ Validation par l'architecte : PASS
- ✅ Pas de problèmes de sécurité détectés
- ✅ Pas d'imports circulaires
- ✅ Relations SQLAlchemy cohérentes

### Notes techniques
- **Backend** : Flask 3.1.2, SQLAlchemy 2.0.44, Flask-Login 0.6.3
- **Base de données** : SQLite (dev) / PostgreSQL (prod à configurer)
- **Authentification** : Flask-Login + JWT (préparé)
- **Migrations** : Flask-Migrate 4.1.0 (prêt pour PostgreSQL)
- **Architecture** : Factory pattern, Blueprints, Modèles séparés

---

## [0.1.0] - 2025-10-24

### Ajouté
- 📁 Structure de base du projet MySindic
  - Dossiers backend (static, templates, routes, models, utils)
  - Dossiers frontend (css, js, images)
  - Dossier docs pour la documentation
- 📄 Documents de gestion de projet
  - `PROJECT_TRACKING.md` : Document de suivi complet du projet avec toutes les fonctionnalités
  - `CHANGELOG.md` : Ce fichier de changelog
  - `DOCUMENTATION_FR.md` : Documentation complète en français
  - `DOCUMENTATION_EN.md` : Documentation complète en anglais
  - `replit.md` : Fichier de mémoire pour Replit Agent avec préférences et architecture
- 🚀 Script de déploiement VPS
  - `deploy_vps.sh` : Script Bash automatisé et complet pour déploiement VPS
  - Gestion automatique de l'environnement virtuel
  - Installation des dépendances
  - Migrations de base de données
  - Démarrage sur port 5006
- 📋 Spécifications fonctionnelles
  - Définition des fonctionnalités Superadmin (9 modules)
  - Définition des fonctionnalités Résidents (5 modules)
  - Définition de l'architecture technique
- 🐍 Application Flask de base
  - `backend/app.py` : Application Flask fonctionnelle
  - Factory pattern pour configuration
  - Routes de santé (/health, /api/info)
  - Page d'accueil avec design moderne Tailwind CSS
  - Gestion des erreurs (404, 500)
  - Support CORS
- 📦 Gestion des dépendances
  - `backend/requirements.txt` : Liste complète des dépendances Python
  - Installation via uv (Replit)
  - Toutes les dépendances installées (Flask, SQLAlchemy, etc.)
- ⚙️ Configuration Replit
  - Workflow "MySindic Server" configuré et fonctionnel
  - Application accessible sur port 5000
  - Python 3.11 installé
- 🔒 Sécurité
  - `.gitignore` complet pour éviter les fuites de secrets
  - `.env.example` comme modèle de configuration
  - Secrets gérés via variables d'environnement

### Testé
- ✅ Serveur Flask démarre correctement
- ✅ Endpoint `/` retourne la page d'accueil
- ✅ Endpoint `/health` retourne le statut de l'API
- ✅ Endpoint `/api/info` retourne les informations de l'API
- ✅ Frontend se connecte correctement au backend
- ✅ Workflow Replit fonctionne sans erreur

### Notes techniques
- **Backend** : Python 3.11 avec Flask 3.0
- **Frontend** : HTML5/CSS3 avec Tailwind CSS (CDN)
- **Type** : Progressive Web App (PWA) - base créée
- **Base de données** : PostgreSQL (configuration à venir)
- **Déploiement Replit** : Port 5000, workflow configuré
- **Déploiement VPS** : Port 5006, script automatisé

---

## Catégories de Changements

- **Ajouté** : pour les nouvelles fonctionnalités
- **Modifié** : pour les changements aux fonctionnalités existantes
- **Déprécié** : pour les fonctionnalités bientôt supprimées
- **Supprimé** : pour les fonctionnalités supprimées
- **Corrigé** : pour les corrections de bugs
- **Sécurité** : en cas de vulnérabilités

---

**Format des entrées :**
```
## [Version] - AAAA-MM-JJ
### Catégorie
- Description du changement
```

---

**Dernière mise à jour :** 24 octobre 2025
