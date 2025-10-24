# Documentation MySindic - Version Française

**Version :** 0.1.0  
**Date :** 24 octobre 2025  
**Langue :** Français 🇫🇷

---

## 📖 Table des Matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Utilisation](#utilisation)
5. [Architecture](#architecture)
6. [API Reference](#api-reference)
7. [Déploiement](#déploiement)
8. [Maintenance](#maintenance)
9. [FAQ](#faq)

---

## 🎯 Introduction

### Qu'est-ce que MySindic ?

MySindic est une application web Progressive Web App (PWA) de gestion de copropriété spécialement conçue pour le marché marocain. Elle offre une solution moderne, mobile-friendly et complète pour gérer tous les aspects d'une copropriété.

### Fonctionnalités Principales

#### Pour les Superadmins (Syndics)
- 🏢 **Gestion des copropriétés** : Créer et gérer plusieurs résidences
- 💰 **Contrôle de gestion** : Tableaux de bord financiers et indicateurs
- 🔧 **Gestion des travaux** : Planification et suivi des interventions
- 💳 **Recouvrement** : Suivi des paiements et relances automatiques
- ⚖️ **Contentieux** : Gestion des litiges
- 📝 **Carnet d'entretien** : Historique complet des interventions
- 🗳️ **Assemblées générales** : Organisation et gestion des AG
- 📧 **Appels de fonds** : Édition et envoi automatique
- 📊 **Répartition des charges** : Calcul automatique

#### Pour les Résidents
- 📢 **Actualités** : Information en temps réel
- 🔧 **Demandes de maintenance** : Création et suivi des interventions
- 📊 **Sondages** : Participation aux décisions importantes
- 📄 **Documents** : Accès aux quittances et documents officiels

---

## 💻 Installation

### Prérequis

- Python 3.9 ou supérieur
- PostgreSQL
- Node.js (pour les outils frontend)
- Git

### Installation locale

```bash
# Cloner le repository
git clone <repository-url>
cd MySindic

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r backend/requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# Initialiser la base de données
flask db init
flask db migrate
flask db upgrade

# Lancer l'application
python backend/app.py
```

---

## ⚙️ Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
# Configuration Flask
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=votre_clé_secrète_très_longue_et_sécurisée

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/mysindic

# Email (pour les notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre_email@example.com
MAIL_PASSWORD=votre_mot_de_passe

# Configuration VPS
VPS_PORT=5006
```

### Configuration de la Base de Données

MySindic utilise PostgreSQL. Assurez-vous d'avoir créé la base de données :

```sql
CREATE DATABASE mysindic;
CREATE USER mysindic_user WITH PASSWORD 'votre_password';
GRANT ALL PRIVILEGES ON DATABASE mysindic TO mysindic_user;
```

---

## 🚀 Utilisation

### Démarrage de l'Application

#### Mode Développement (Replit)
```bash
python backend/app.py
```
L'application sera accessible sur `http://0.0.0.0:5000`

#### Mode Production (VPS)
Utilisez le script de déploiement :
```bash
chmod +x deploy_vps.sh
./deploy_vps.sh
```
L'application sera accessible sur le port 5006

### Accès à l'Application

1. **Page d'accueil** : `/`
2. **Connexion** : `/login`
3. **Dashboard Superadmin** : `/admin/dashboard`
4. **Dashboard Résident** : `/resident/dashboard`

### Premiers Pas

1. **Créer un compte Superadmin**
   - Accéder à `/register`
   - Remplir les informations
   - Confirmer par email

2. **Créer une résidence**
   - Se connecter en tant que Superadmin
   - Aller dans "Gestion des résidences"
   - Cliquer sur "Nouvelle résidence"

3. **Ajouter des résidents**
   - Dans la résidence, aller dans "Résidents"
   - Cliquer sur "Ajouter un résident"
   - Envoyer l'invitation

---

## 🏗️ Architecture

### Structure du Projet

```
MySindic/
├── backend/
│   ├── app.py              # Point d'entrée Flask
│   ├── config.py           # Configuration
│   ├── models/             # Modèles SQLAlchemy
│   ├── routes/             # Routes API
│   ├── utils/              # Fonctions utilitaires
│   ├── static/             # CSS, JS, images
│   └── templates/          # Templates HTML
├── frontend/
│   ├── css/               # Styles Tailwind
│   ├── js/                # JavaScript
│   └── images/            # Images
└── docs/                  # Documentation
```

### Technologies Utilisées

- **Backend** : Flask, SQLAlchemy, Flask-Migrate
- **Frontend** : HTML5, Tailwind CSS, JavaScript (Vanilla)
- **Base de données** : PostgreSQL
- **Authentification** : Flask-Login, JWT
- **PWA** : Service Workers, Web App Manifest

---

## 🔌 API Reference

### Authentification

#### POST `/api/auth/login`
Connexion d'un utilisateur

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "motdepasse"
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

### Gestion des Résidences

#### GET `/api/residences`
Récupérer la liste des résidences

**Response:**
```json
{
  "success": true,
  "residences": [
    {
      "id": 1,
      "name": "Résidence Al Andalous",
      "address": "Casablanca, Maroc",
      "units": 45
    }
  ]
}
```

*(Documentation API complète à venir)*

---

## 🌐 Déploiement

### Déploiement sur VPS

Le script `deploy_vps.sh` automatise le déploiement :

```bash
# Rendre le script exécutable
chmod +x deploy_vps.sh

# Lancer le déploiement
./deploy_vps.sh
```

**Le script effectue automatiquement :**
1. Pull du code depuis Git
2. Vérification/création de l'environnement virtuel
3. Activation de l'environnement
4. Vérification/création du fichier .env
5. Installation des dépendances
6. Démarrage de l'application sur le port 5006

### Déploiement sur Replit

L'application est configurée pour fonctionner directement sur Replit :
- Port : 5000 (obligatoire)
- Workflow configuré automatiquement
- Base de données PostgreSQL intégrée

---

## 🔧 Maintenance

### Mises à Jour

```bash
# Mettre à jour le code
git pull origin main

# Mettre à jour les dépendances
pip install -r backend/requirements.txt --upgrade

# Appliquer les migrations
flask db upgrade
```

### Sauvegardes

Il est recommandé de sauvegarder régulièrement :
- La base de données PostgreSQL
- Les fichiers uploadés
- Le fichier .env

### Logs

Les logs sont stockés dans :
- `logs/app.log` : Logs de l'application
- `logs/error.log` : Erreurs uniquement

---

## ❓ FAQ

### Comment réinitialiser le mot de passe d'un utilisateur ?
Via le dashboard Superadmin > Utilisateurs > Sélectionner l'utilisateur > Réinitialiser mot de passe

### Comment ajouter une nouvelle résidence ?
Dashboard Superadmin > Résidences > Nouvelle résidence

### L'application est-elle compatible mobile ?
Oui, MySindic est une PWA optimisée pour mobile et peut être installée comme une application native.

### Comment contacter le support ?
Email : support@mysindic.ma

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email : support@mysindic.ma
- 📱 Téléphone : +212 XXX XXX XXX
- 🌐 Site web : www.mysindic.ma

---

**Dernière mise à jour :** 24 octobre 2025  
**Version :** 0.1.0
