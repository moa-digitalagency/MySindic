# MySindic - Document de Suivi du Projet

**Date de création :** 24 octobre 2025  
**Dernière mise à jour :** 24 octobre 2025

## 📋 Vue d'ensemble

MySindic est une application web PWA de gestion de copropriété au Maroc, avec un design moderne et mobile-friendly.

### Stack Technique
- **Backend :** Python (Flask)
- **Frontend :** HTML/CSS avec Tailwind CSS
- **Type :** Progressive Web App (PWA)
- **Déploiement :** VPS (port 5006)

---

## 🎯 Fonctionnalités

### 👨‍💼 SUPERADMIN

| Fonctionnalité | Description | Statut | Testé | Priorité |
|----------------|-------------|--------|-------|----------|
| Création de copropriété | Créer et configurer une nouvelle résidence | ⏳ À faire | ❌ | 🔴 Haute |
| État de contrôle de gestion | Tableau de bord financier et indicateurs | ⏳ À faire | ❌ | 🔴 Haute |
| Gestion des travaux | Planification et suivi des travaux | ⏳ À faire | ❌ | 🟡 Moyenne |
| Gestion du recouvrement | Suivi des paiements et relances | ⏳ À faire | ❌ | 🔴 Haute |
| Gestion des contentieux | Gestion des litiges et procédures | ⏳ À faire | ❌ | 🟡 Moyenne |
| Carnet d'entretien | Historique des interventions | ⏳ À faire | ❌ | 🟡 Moyenne |
| Assemblées générales | Organisation et gestion des AG | ⏳ À faire | ❌ | 🔴 Haute |
| Appels de fonds | Édition et envoi automatique | ⏳ À faire | ❌ | 🔴 Haute |
| Répartition des charges | Calcul automatique des charges | ⏳ À faire | ❌ | 🔴 Haute |

### 🏠 RÉSIDENTS

| Fonctionnalité | Description | Statut | Testé | Priorité |
|----------------|-------------|--------|-------|----------|
| Actualités de la résidence | Consultation des informations | ⏳ À faire | ❌ | 🔴 Haute |
| Demandes de maintenance | Créer et suivre les demandes | ⏳ À faire | ❌ | 🔴 Haute |
| Suivi des interventions | Voir qui traite les demandes | ⏳ À faire | ❌ | 🔴 Haute |
| Sondages | Participer et voir les résultats | ⏳ À faire | ❌ | 🟡 Moyenne |
| Accès documents | Quittances et documents officiels | ⏳ À faire | ❌ | 🔴 Haute |

### 🔐 AUTHENTIFICATION & SÉCURITÉ

| Fonctionnalité | Description | Statut | Testé | Priorité |
|----------------|-------------|--------|-------|----------|
| Système d'authentification | Login/Logout sécurisé | ⏳ À faire | ❌ | 🔴 Haute |
| Gestion des rôles | Superadmin / Résident | ⏳ À faire | ❌ | 🔴 Haute |
| Sécurité des données | HTTPS, hashing passwords | ⏳ À faire | ❌ | 🔴 Haute |

---

## 🛠️ Implémentation Technique

### Structure du Projet

```
MySindic/
├── backend/
│   ├── app.py                  # Application Flask principale
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Dépendances Python
│   ├── models/                # Modèles de données
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── residence.py
│   │   └── maintenance.py
│   ├── routes/                # Routes de l'API
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── admin.py
│   │   └── resident.py
│   ├── utils/                 # Utilitaires
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── static/                # Fichiers statiques
│   └── templates/             # Templates HTML
├── frontend/
│   ├── css/
│   ├── js/
│   └── images/
├── docs/
├── deploy_vps.sh             # Script de déploiement VPS
├── PROJECT_TRACKING.md       # Ce document
├── CHANGELOG.md              # Journal des modifications
├── DOCUMENTATION_FR.md       # Documentation française
├── DOCUMENTATION_EN.md       # Documentation anglaise
└── replit.md                 # Mémoire du projet Replit
```

### Base de données

- **Type :** PostgreSQL (via Replit Database)
- **ORM :** SQLAlchemy
- **Migrations :** Flask-Migrate

### Architecture

1. **Backend API RESTful** : Flask avec routes organisées par module
2. **Frontend responsive** : HTML/CSS/JS avec Tailwind CSS
3. **PWA** : Service Worker pour le mode offline
4. **Sécurité** : JWT pour l'authentification, HTTPS obligatoire

---

## 📦 Déploiement

### Déploiement sur VPS

Un script automatisé `deploy_vps.sh` est fourni pour le déploiement sur VPS :

**Fonctionnalités du script :**
- Pull du code depuis le repository
- Vérification/création de l'environnement virtuel Python
- Gestion du fichier .env
- Installation des dépendances (requirements.txt)
- Démarrage de l'application sur le port 5006

**Instructions pour l'agent Replit :**
> ⚠️ **Important** : Le script `deploy_vps.sh` est conçu pour le déploiement sur VPS externe. Pour tester l'application sur Replit, utilisez le workflow configuré qui démarre l'application sur le port 5000.

### Déploiement sur Replit

- **Port de développement :** 5000 (obligatoire pour Replit)
- **Port VPS :** 5006
- **Workflow :** Flask app configurée pour bind sur 0.0.0.0:5000

---

## ✅ États des Fonctionnalités

**Légende :**
- ✅ Implémenté et testé
- 🚧 En cours de développement
- ⏳ À faire
- ❌ Non testé
- ✔️ Testé et validé

### Phase 1 - Infrastructure (En cours)
- ✅ Structure du projet créée
- ✅ Documents de suivi créés
- ⏳ Configuration Flask
- ⏳ Base de données PostgreSQL
- ⏳ Système d'authentification

### Phase 2 - Fonctionnalités Superadmin
- ⏳ Toutes les fonctionnalités à implémenter

### Phase 3 - Fonctionnalités Résidents
- ⏳ Toutes les fonctionnalités à implémenter

### Phase 4 - PWA & Mobile
- ⏳ Service Worker
- ⏳ Manifest PWA
- ⏳ Design responsive

---

## 📝 Notes Importantes

### Pour les développeurs
1. **Toujours lire ce document** avant de commencer à travailler
2. **Mettre à jour le CHANGELOG** après chaque modification
3. **Tester les fonctionnalités** avant de les marquer comme terminées
4. **Documenter le code** en français
5. **Respecter la structure** du projet

### Bonnes Pratiques
- Commits réguliers avec messages descriptifs
- Tests unitaires pour les fonctions critiques
- Validation des données côté serveur
- Gestion d'erreurs appropriée
- Logs structurés

---

## 🔄 Prochaines Étapes

1. ✅ Créer la structure de base du projet
2. ⏳ Configurer Flask et la base de données
3. ⏳ Implémenter l'authentification
4. ⏳ Créer le tableau de bord superadmin
5. ⏳ Implémenter la gestion des résidences
6. ⏳ Développer les fonctionnalités résidents

---

**Dernière mise à jour par :** Agent Replit  
**Date :** 24 octobre 2025
