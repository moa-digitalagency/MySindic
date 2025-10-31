# Shabaka Syndic

Solution complète et digitale pour la gestion de copropriété au Maroc.

## 🎯 Description

Shabaka Syndic est une plateforme moderne de gestion de copropriété qui facilite la communication entre les syndics et les résidents. Elle offre une solution complète pour gérer les charges, les demandes de maintenance, les actualités, les assemblées générales et bien plus encore.

## ✨ Fonctionnalités Principales

### Pour les Résidents
- 📱 **Dashboard personnalisé** avec vue d'ensemble des informations importantes
- 🔧 **Demandes de maintenance** avec suivi en temps réel
- 💰 **Gestion financière** : consultation des charges et paiements
- 📰 **Actualités** de la résidence
- 📄 **Documents** partagés par le syndic
- 🗳️ **Assemblées générales** et votes en ligne

### Pour les Administrateurs
- 🏢 **Gestion des résidences** et unités
- 👥 **Gestion des utilisateurs** et attribution des rôles
- 💵 **Gestion financière** complète (charges, paiements, appels de fonds)
- 🔧 **Suivi des maintenances** et carnet d'entretien
- 📊 **Statistiques et rapports** détaillés
- ⚖️ **Gestion des litiges**
- 📰 **Publication d'actualités** et communications

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- PostgreSQL
- Navigateur web moderne

### Installation

1. Installer les dépendances :
```bash
python -m pip install -r requirements.txt
```

2. Configurer la base de données (automatique au premier lancement)

3. Lancer l'application :
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port main:app
```

## 👤 Comptes de Démonstration

Utilisez ces identifiants pour tester les différents rôles :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Super Admin** | admin@mysindic.ma | Admin123! |
| **Admin Syndic** | admin.syndic@mysindic.ma | Admin123! |
| **Propriétaire** | owner@mysindic.ma | Owner123! |
| **Résident** | resident@mysindic.ma | Resident123! |

## 📚 Structure du Projet

```
.
├── backend/               # Code backend (Python/Flask)
│   ├── models/           # Modèles de base de données
│   ├── routes/           # Routes API
│   ├── services/         # Services métier
│   ├── app.py           # Application Flask
│   └── config.py        # Configuration
├── frontend/             # Interface utilisateur
│   ├── templates/       # Templates HTML
│   ├── static/          # CSS, JS, images
│   └── ...
├── documentation/        # Documentation
└── main.py              # Point d'entrée

```

## 🔒 Sécurité

- Authentification sécurisée avec hashage des mots de passe
- Protection CSRF
- Validation des données côté serveur
- Contrôle d'accès basé sur les rôles
- Sessions sécurisées

## 📝 Licence

© 2025 Shabaka Syndic - Tous droits réservés
Développé par Aisance KALONJI

## 📧 Contact

Pour toute question ou support :
- Email : moa@myoneart.com
- Web : www.myoneart.com
