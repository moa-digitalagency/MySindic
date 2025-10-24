# Changelog - MySindic

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Versioning Sémantique](https://semver.org/lang/fr/).

---

## [Non publié]

### Prochaines étapes
- Configuration de la base de données PostgreSQL
- Système d'authentification (Flask-Login)
- Modèles de données (User, Residence, Maintenance, etc.)
- Routes API de base
- Interface utilisateur complète avec Tailwind CSS

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
