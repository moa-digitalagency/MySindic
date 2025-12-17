# Shabaka Syndic

## Plateforme de Gestion de Copropriété

Shabaka Syndic est une application web conçue pour la gestion des copropriétés au Maroc. Elle permet aux syndics, administrateurs et résidents de gérer efficacement tous les aspects de la vie en copropriété : finances, maintenance, assemblées générales, communication et documents.

## Sommaire de la Documentation

| Document | Description |
|----------|-------------|
| [Guide Utilisateur](GUIDE_UTILISATEUR.md) | Mode d'emploi pour tous les profils d'utilisateurs |
| [Guide Commercial](GUIDE_COMMERCIAL.md) | Présentation des fonctionnalités et avantages |
| [Architecture Technique](ARCHITECTURE_TECHNIQUE.md) | Structure du code et choix techniques |
| [Référence API](API_REFERENCE.md) | Documentation des endpoints REST |
| [Installation](INSTALLATION.md) | Procédure d'installation et configuration |
| [Sécurité](SECURITE.md) | Mesures de protection et bonnes pratiques |

## Présentation Rapide

### Contexte

La gestion d'une copropriété implique de nombreuses tâches : collecter les charges, organiser les assemblées générales, gérer les demandes de maintenance, communiquer avec les résidents. Shabaka Syndic centralise toutes ces opérations dans une interface unique accessible depuis n'importe quel navigateur.

### Public Cible

- Syndics professionnels gérant plusieurs résidences
- Conseils syndicaux de copropriétés
- Propriétaires souhaitant suivre leur bien
- Résidents voulant interagir avec leur syndic

### Fonctionnalités Principales

**Gestion Financière**
- Création et publication des appels de fonds
- Répartition automatique des charges par lot
- Suivi des paiements et des impayés
- Historique financier par résident

**Maintenance**
- Signalement de problèmes par les résidents
- Suivi de l'avancement des interventions
- Carnet d'entretien de l'immeuble
- Attribution aux prestataires

**Assemblées Générales**
- Planification et convocations
- Gestion des résolutions
- Vote électronique
- Suivi des présences

**Communication**
- Fil d'actualités pour tous les résidents
- Annonces officielles pour les propriétaires
- Sondages et consultations
- Gestion documentaire

## Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Flask 3.0, Python 3.11 |
| Base de données | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Authentification | Flask-Login |
| Frontend | HTML5, Tailwind CSS, JavaScript |
| Serveur | Gunicorn |

## Structure du Projet

```
shabaka-syndic/
├── backend/
│   ├── models/          # Modèles de données (20 tables)
│   ├── routes/          # API REST (auth, admin, resident)
│   ├── services/        # Logique métier
│   ├── utils/           # Utilitaires et décorateurs
│   ├── app.py           # Application Flask
│   └── config.py        # Configuration
├── frontend/
│   ├── static/          # CSS, JavaScript, images
│   └── templates/       # Templates Jinja2
├── docs/                # Documentation
├── main.py              # Point d'entrée
└── requirements.txt     # Dépendances Python
```

## Démarrage Rapide

1. Cloner le projet
2. Installer les dépendances : `pip install -r requirements.txt`
3. Configurer la base de données PostgreSQL
4. Définir les variables d'environnement
5. Lancer : `gunicorn --bind 0.0.0.0:5000 main:app`

Pour les instructions détaillées, consulter le [Guide d'Installation](INSTALLATION.md).

## Comptes de Démonstration

L'application inclut des données de test :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Super Admin | admin@mysindic.ma | Admin123! |
| Syndic | admin.syndic@mysindic.ma | Admin123! |
| Propriétaire | owner@mysindic.ma | Owner123! |
| Résident | resident@mysindic.ma | Resident123! |

## Licence

Shabaka Syndic - Développé par Aisance KALONJI

Contact : moa@myoneart.com
