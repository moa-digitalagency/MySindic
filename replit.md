# MySindic - Mémoire du Projet Replit

**Date de création :** 24 octobre 2025  
**Dernière mise à jour :** 24 octobre 2025

---

## 📋 Vue d'ensemble du Projet

**MySindic** est une Progressive Web App (PWA) de gestion de copropriété destinée au marché marocain. L'application offre une solution complète pour les syndics (superadmins) et les résidents.

### Type d'Application
- **Type :** Progressive Web App (PWA)
- **Backend :** Python avec Flask
- **Frontend :** HTML/CSS avec Tailwind CSS
- **Base de données :** PostgreSQL (Replit Database)

---

## 🎯 Objectifs du Projet

1. Créer une plateforme moderne de gestion de copropriété
2. Offrir une expérience mobile-first et responsive
3. Automatiser les tâches administratives (appels de fonds, répartition des charges)
4. Faciliter la communication entre syndics et résidents

---

## 📊 État Actuel

### Version Actuelle : 0.1.0 (Phase d'initialisation)

**Infrastructure créée :**
- ✅ Structure du projet (backend, frontend, docs)
- ✅ Documents de gestion (PROJECT_TRACKING.md, CHANGELOG.md)
- ✅ Documentation bilingue (FR/EN)
- ✅ Script de déploiement VPS (deploy_vps.sh)
- ✅ Application Flask de base
- ✅ Workflow Replit configuré

**Prochaines étapes :**
- ⏳ Configuration de la base de données PostgreSQL
- ⏳ Système d'authentification (Flask-Login)
- ⏳ Modèles de données (User, Residence, Maintenance, etc.)
- ⏳ Routes API de base
- ⏳ Interface utilisateur avec Tailwind CSS

---

## 🏗️ Structure du Projet

```
MySindic/
├── backend/
│   ├── app.py                 # Point d'entrée Flask
│   ├── config.py              # Configuration de l'app
│   ├── requirements.txt       # Dépendances Python
│   ├── models/                # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py           # Modèle utilisateur
│   │   ├── residence.py      # Modèle résidence
│   │   └── maintenance.py    # Modèle maintenance
│   ├── routes/                # Routes API
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentification
│   │   ├── admin.py          # Routes superadmin
│   │   └── resident.py       # Routes résidents
│   ├── utils/                 # Utilitaires
│   ├── static/                # CSS, JS, images
│   └── templates/             # Templates HTML/Jinja2
├── frontend/
│   ├── css/                   # Styles Tailwind
│   ├── js/                    # JavaScript
│   └── images/                # Images
├── docs/                      # Documentation additionnelle
├── logs/                      # Logs de l'application
├── deploy_vps.sh              # Script déploiement VPS
├── PROJECT_TRACKING.md        # Document de suivi
├── CHANGELOG.md               # Journal des modifications
├── DOCUMENTATION_FR.md        # Doc française
├── DOCUMENTATION_EN.md        # Doc anglaise
└── replit.md                  # Ce fichier
```

---

## 🔑 Fonctionnalités Principales

### Pour les Superadmins (Syndics)

1. **Gestion des copropriétés**
   - Création et configuration de résidences
   - Gestion des lots et appartements

2. **Contrôle de gestion**
   - Tableaux de bord financiers
   - Indicateurs de performance

3. **Gestion des travaux**
   - Planification des interventions
   - Suivi des prestataires

4. **Recouvrement**
   - Suivi des paiements
   - Relances automatiques

5. **Appels de fonds**
   - Génération automatique
   - Envoi par email

6. **Répartition des charges**
   - Calcul automatique selon les tantièmes
   - Édition des décomptes

7. **Assemblées générales**
   - Convocations
   - Procès-verbaux
   - Votes

8. **Carnet d'entretien**
   - Historique des interventions
   - Documents techniques

9. **Contentieux**
   - Gestion des litiges
   - Suivi des procédures

### Pour les Résidents

1. **Actualités**
   - Consulter les informations de la résidence
   - Notifications importantes

2. **Demandes de maintenance**
   - Créer une demande
   - Suivre la progression
   - Voir l'intervenant assigné

3. **Sondages**
   - Participer aux votes
   - Voir les résultats en temps réel

4. **Documents**
   - Accès aux quittances
   - Téléchargement des documents officiels

---

## 🛠️ Technologies et Dépendances

### Backend Python
- **Flask** : Framework web
- **SQLAlchemy** : ORM pour la base de données
- **Flask-Migrate** : Migrations de base de données
- **Flask-Login** : Gestion des sessions utilisateur
- **PyJWT** : Tokens d'authentification
- **Werkzeug** : Sécurité et hashing de mots de passe
- **psycopg2** : Connecteur PostgreSQL

### Frontend
- **Tailwind CSS** : Framework CSS utilitaire
- **JavaScript Vanilla** : Interactions côté client
- **Service Worker** : Fonctionnalités PWA

### Base de données
- **PostgreSQL** : Base de données relationnelle
- Accessible via Replit Database intégrée

---

## ⚙️ Configuration Replit

### Workflow
- **Nom :** MySindic Server
- **Commande :** `python backend/app.py`
- **Port :** 5000 (obligatoire pour Replit)
- **Type de sortie :** webview

### Variables d'Environnement (.env)
```env
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=<généré automatiquement>
DATABASE_URL=<fourni par Replit Database>
```

### Ports
- **Développement (Replit) :** 5000
- **Production (VPS) :** 5006

---

## 📚 Documents Importants

### Documents de Gestion
1. **PROJECT_TRACKING.md** : À LIRE OBLIGATOIREMENT avant toute modification
   - Liste complète des fonctionnalités
   - État d'avancement
   - Architecture technique

2. **CHANGELOG.md** : À METTRE À JOUR après chaque modification
   - Historique des changements
   - Versions

3. **DOCUMENTATION_FR.md** : Documentation en français
   - Guide d'installation
   - Guide d'utilisation
   - API Reference

4. **DOCUMENTATION_EN.md** : Documentation en anglais
   - Version anglaise de la documentation

### Script de Déploiement
**deploy_vps.sh** : Script automatisé pour VPS
- Pull du code
- Gestion de l'environnement virtuel
- Installation des dépendances
- Migrations de base de données
- Démarrage sur port 5006

⚠️ **Note pour l'Agent Replit :** Ce script est pour déploiement VPS externe uniquement. Sur Replit, utiliser le workflow configuré.

---

## 👤 Préférences Utilisateur

### Langue
- Interface : Français (primaire) et Anglais
- Documentation : Bilingue FR/EN
- Code : Commentaires en français

### Style de Code
- **Python :** PEP 8
- **Indentation :** 4 espaces
- **Longueur de ligne :** Max 100 caractères
- **Docstrings :** Format Google

### Organisation
- Séparer la logique métier dans des modules
- Utiliser des blueprints Flask pour organiser les routes
- Modèles SQLAlchemy dans des fichiers séparés
- Utilitaires dans le dossier `utils/`

---

## 🔒 Sécurité

### Authentification
- Hashing des mots de passe avec Werkzeug
- Sessions sécurisées avec Flask-Login
- Tokens JWT pour l'API

### Base de données
- Migrations via Flask-Migrate uniquement
- Jamais de SQL brut (utiliser l'ORM)
- Validation des données côté serveur

### Secrets
- Utiliser les variables d'environnement
- Ne jamais commiter les secrets dans Git
- Fichier .env dans .gitignore

---

## 📈 Décisions Architecturales

### Base de données PostgreSQL
**Raison :** Intégration native Replit, support des transactions, scalabilité

### Flask comme Framework
**Raison :** Léger, flexible, excellent pour les API REST

### Tailwind CSS
**Raison :** Développement rapide, design moderne, mobile-first

### PWA
**Raison :** Expérience native sur mobile, mode offline, notifications push

---

## 🚀 Déploiement

### Sur Replit (Développement)
1. Le workflow démarre automatiquement
2. Application accessible via le webview
3. Port 5000 obligatoire

### Sur VPS (Production)
1. Exécuter `./deploy_vps.sh`
2. Le script gère tout automatiquement
3. Application sur port 5006

---

## 📝 Bonnes Pratiques

### Avant de Coder
1. ✅ Lire PROJECT_TRACKING.md
2. ✅ Vérifier le CHANGELOG.md
3. ✅ Comprendre l'architecture existante

### Pendant le Développement
1. ✅ Suivre le style de code défini
2. ✅ Commenter en français
3. ✅ Tester les fonctionnalités
4. ✅ Gérer les erreurs appropriément

### Après le Développement
1. ✅ Mettre à jour PROJECT_TRACKING.md
2. ✅ Ajouter une entrée dans CHANGELOG.md
3. ✅ Mettre à jour la documentation si nécessaire
4. ✅ Vérifier que le workflow fonctionne
5. ✅ Tester l'application

---

## 🔄 Workflow de Développement

1. **Planification** : Définir la fonctionnalité dans PROJECT_TRACKING.md
2. **Développement** : Coder en suivant les bonnes pratiques
3. **Test** : Vérifier que tout fonctionne
4. **Documentation** : Mettre à jour les docs
5. **Commit** : Message descriptif en français
6. **Mise à jour** : CHANGELOG.md et PROJECT_TRACKING.md

---

## 📞 Support et Contact

- **Email :** support@mysindic.ma
- **Téléphone :** +212 XXX XXX XXX

---

## 🎯 Roadmap

### Phase 1 : Infrastructure (En cours)
- ✅ Création de la structure
- ⏳ Configuration Flask complète
- ⏳ Base de données PostgreSQL
- ⏳ Authentification de base

### Phase 2 : Fonctionnalités Superadmin
- ⏳ Gestion des résidences
- ⏳ Gestion des utilisateurs
- ⏳ Tableau de bord
- ⏳ Appels de fonds
- ⏳ Répartition des charges

### Phase 3 : Fonctionnalités Résidents
- ⏳ Interface résidents
- ⏳ Demandes de maintenance
- ⏳ Consultation documents
- ⏳ Sondages

### Phase 4 : PWA
- ⏳ Service Worker
- ⏳ Manifest
- ⏳ Mode offline
- ⏳ Notifications push

### Phase 5 : Production
- ⏳ Optimisations
- ⏳ Tests de charge
- ⏳ Déploiement final

---

**Dernière mise à jour :** 24 octobre 2025  
**Version :** 0.1.0  
**Statut :** Phase d'initialisation
