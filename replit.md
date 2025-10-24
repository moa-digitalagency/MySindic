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

### Version Actuelle : 0.2.0 (Backend MVP Complet)

**Backend Complet ✅**
- ✅ Tous les modèles de base de données créés et testés
- ✅ Services partagés (ChargeCalculator, NotificationService)
- ✅ Routes admin complètes avec toutes les fonctionnalités superadmin
- ✅ Routes résidents complètes avec contrôles de sécurité
- ✅ Système d'autorisation sécurisé (protection contre escalade de privilèges)
- ✅ API REST complète et fonctionnelle
- ✅ Application Flask déployée sur port 5000

**Frontend Landing Page ✅**
- ✅ Page d'accueil responsive avec Tailwind CSS
- ✅ Navigation et design moderne
- ✅ API connectée et testée

**Prochaines étapes :**
- ⏳ Interfaces utilisateur complètes (dashboard admin, dashboard résident)
- ⏳ Formulaires interactifs pour toutes les fonctionnalités
- ⏳ Fonctionnalités PWA (Service Worker, manifest, mode offline)
- ⏳ Tests d'intégration pour les contrôles d'autorisation
- ⏳ Optimisation pour production

---

## 🏗️ Architecture Backend (Complète)

### Modèles de Données Implémentés

**Modèles de Base ✅**
1. `User` - Utilisateurs (superadmins et résidents)
2. `Residence` - Copropriétés/résidences
3. `Unit` - Lots/appartements avec tantièmes

**Gestion Financière ✅**
4. `Charge` - Charges de copropriété
5. `ChargeDistribution` - Répartition automatique des charges
6. `Payment` - Paiements des résidents

**Maintenance ✅**
7. `MaintenanceRequest` - Demandes de maintenance
8. `MaintenanceLog` - Carnet d'entretien (historique des interventions)

**Communication ✅**
9. `News` - Actualités de la résidence
10. `Poll`, `PollOption`, `PollVote` - Système de sondages

**Documents ✅**
11. `Document` - Gestion documentaire

**Assemblées Générales ✅**
12. `GeneralAssembly` - Assemblées générales
13. `Resolution` - Résolutions à voter
14. `Vote` - Votes des résidents
15. `Attendance` - Présences aux AG

**Contentieux ✅**
16. `Litigation` - Gestion des litiges

### Services Métier Implémentés

**ChargeCalculator** ✅
- Calcul automatique de la répartition des charges selon les tantièmes
- Calcul du solde d'un lot
- Liste des charges impayées
- Suivi des paiements

**NotificationService** ✅
- Notifications pour nouvelles demandes de maintenance
- Notifications pour appels de fonds
- Notifications pour assemblées générales
- Service centralisé d'envoi d'emails

### Routes API Complètes

**Routes Admin (`/api/admin/*`)** ✅
- Dashboard avec statistiques complètes
- CRUD résidences
- CRUD lots/unités
- Gestion complète des charges (création, publication, distribution automatique)
- Validation des paiements
- Gestion des actualités
- Gestion des demandes de maintenance
- Carnet d'entretien
- Assemblées générales (création, convocation, résolutions)
- Gestion des contentieux
- Système de sondages
- Gestion des utilisateurs

**Routes Résidents (`/api/resident/*`)** ✅ **SÉCURISÉES**
- Dashboard personnalisé
- Consultation des actualités
- Création et suivi des demandes de maintenance
- Consultation des charges et solde
- Déclaration de paiements
- Accès aux documents publics
- Participation aux sondages
- Consultation et participation aux AG
- Vote sur les résolutions
- Consultation du carnet d'entretien

**Sécurité Renforcée** ✅
- Tous les endpoints résidents vérifient `residence_id` avant de retourner des données
- Protection contre l'escalade de privilèges horizontale
- Codes HTTP appropriés (403 Forbidden, 404 Not Found)
- Dérivation des foreign keys de `current_user` (pas de confiance en l'input client)
- Validation et autorisation sur tous les endpoints

---

## 🔑 Fonctionnalités Implémentées

### Pour les Superadmins (Syndics) - COMPLET ✅

1. **Gestion des copropriétés** ✅
   - Création et configuration de résidences
   - Gestion des lots et appartements avec tantièmes
   - Configuration des paramètres financiers

2. **Contrôle de gestion** ✅
   - Tableaux de bord financiers complets
   - Indicateurs de performance (taux de recouvrement, charges en attente)
   - Statistiques de maintenance et AG

3. **Gestion des travaux** ✅
   - Réception et traitement des demandes de maintenance
   - Assignation aux prestataires
   - Mise à jour du statut des interventions

4. **Recouvrement** ✅
   - Suivi des paiements en temps réel
   - Validation des paiements déclarés
   - Calcul automatique des soldes

5. **Appels de fonds** ✅
   - Création des charges
   - Publication avec distribution automatique selon tantièmes
   - Suivi des paiements

6. **Répartition des charges** ✅
   - Calcul automatique selon les tantièmes
   - Distribution aux lots
   - Historique des distributions

7. **Assemblées générales** ✅
   - Création et planification des AG
   - Envoi des convocations
   - Gestion des résolutions
   - Comptage des votes
   - Suivi des présences

8. **Carnet d'entretien** ✅
   - Enregistrement de toutes les interventions
   - Historique complet avec dates et coûts
   - Consultation par les résidents

9. **Contentieux** ✅
   - Ouverture de dossiers de contentieux
   - Suivi des procédures et statuts
   - Historique des litiges

10. **Communication** ✅
    - Publication d'actualités (épinglées ou normales)
    - Création de sondages
    - Gestion des documents

### Pour les Résidents - COMPLET ✅

1. **Actualités** ✅
   - Consulter les informations de la résidence
   - Actualités épinglées en priorité
   - Détails complets des annonces

2. **Demandes de maintenance** ✅
   - Créer une demande avec catégorie et priorité
   - Suivre la progression en temps réel
   - Voir les interventions assignées
   - Historique de toutes les demandes

3. **Finances** ✅
   - Consultation des charges du lot
   - Visualisation du solde en temps réel
   - Liste des charges impayées
   - Déclaration de paiements
   - Historique des paiements

4. **Sondages** ✅
   - Participer aux votes
   - Voir les résultats (si autorisé)
   - Historique des sondages

5. **Documents** ✅
   - Accès aux documents publics
   - Consultation des quittances
   - Documents officiels de la copropriété

6. **Assemblées générales** ✅
   - Consultation des AG passées et à venir
   - Enregistrement de présence
   - Vote sur les résolutions
   - Consultation des résultats

7. **Carnet d'entretien** ✅
   - Consultation de l'historique des interventions
   - Transparence sur les travaux réalisés

---

## 🏗️ Structure du Projet

```
MySindic/
├── backend/
│   ├── app.py                      # ✅ Application Flask configurée
│   ├── main.py                     # ✅ Point d'entrée
│   ├── models/
│   │   ├── __init__.py             # ✅ Tous les modèles exportés
│   │   ├── user.py                 # ✅ Modèle User complet
│   │   ├── residence.py            # ✅ Residence et Unit
│   │   ├── charge.py               # ✅ Charge et ChargeDistribution
│   │   ├── payment.py              # ✅ Payment
│   │   ├── maintenance.py          # ✅ MaintenanceRequest
│   │   ├── maintenance_log.py      # ✅ MaintenanceLog
│   │   ├── news.py                 # ✅ News
│   │   ├── poll.py                 # ✅ Poll, PollOption, PollVote
│   │   ├── document.py             # ✅ Document
│   │   ├── general_assembly.py     # ✅ GeneralAssembly, Resolution, Vote, Attendance
│   │   └── litigation.py           # ✅ Litigation
│   ├── routes/
│   │   ├── __init__.py             # ✅ Blueprints enregistrés
│   │   ├── auth.py                 # ✅ Authentification complète
│   │   ├── admin.py                # ✅ Routes admin complètes
│   │   └── resident.py             # ✅ Routes résidents sécurisées
│   ├── utils/
│   │   ├── charge_calculator.py    # ✅ Service de calcul des charges
│   │   └── notification_service.py # ✅ Service de notifications
│   ├── static/
│   │   ├── css/                    # ✅ Styles
│   │   └── js/                     # ✅ JavaScript
│   └── templates/
│       └── index.html              # ✅ Landing page
├── docs/
├── PROJECT_TRACKING.md             # ✅ Suivi complet du projet
├── CHANGELOG.md                    # ✅ Journal des modifications
├── DOCUMENTATION_FR.md             # ✅ Documentation française
├── DOCUMENTATION_EN.md             # ✅ Documentation anglaise
└── replit.md                       # ✅ Ce fichier
```

---

## 🛠️ Technologies et Dépendances

### Backend Python
- **Flask** : Framework web
- **SQLAlchemy** : ORM pour la base de données
- **Flask-Migrate** : Migrations de base de données
- **Flask-Login** : Gestion des sessions utilisateur
- **Flask-CORS** : Support CORS
- **PyJWT** : Tokens d'authentification
- **Werkzeug** : Sécurité et hashing de mots de passe
- **psycopg2-binary** : Connecteur PostgreSQL
- **Gunicorn** : Serveur WSGI de production

### Frontend
- **Tailwind CSS** : Framework CSS utilitaire (via CDN)
- **JavaScript Vanilla** : Interactions côté client
- **Feather Icons** : Icônes modernes
- **Service Worker** : (À implémenter) Fonctionnalités PWA

### Base de données
- **PostgreSQL** : Base de données relationnelle
- Accessible via Replit Database intégrée

---

## ⚙️ Configuration Replit

### Workflow
- **Nom :** Start application
- **Commande :** `gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app`
- **Port :** 5000 (obligatoire pour Replit)
- **Type de sortie :** webview
- **Statut :** ✅ RUNNING

### Variables d'Environnement
```env
SESSION_SECRET=<généré automatiquement par Replit>
DATABASE_URL=<fourni par Replit Database>
```

---

## 🔒 Sécurité - RENFORCÉE ✅

### Authentification
- ✅ Hashing des mots de passe avec Werkzeug (sans méthode spécifique)
- ✅ Sessions sécurisées avec Flask-Login
- ✅ Décorateurs d'autorisation (`@login_required`, `@superadmin_required`)

### Autorisation et Contrôles d'Accès
- ✅ **Tous les endpoints résidents vérifient l'appartenance à la résidence**
- ✅ Protection contre escalade de privilèges horizontale
- ✅ Codes HTTP appropriés (403 Forbidden vs 404 Not Found)
- ✅ Dérivation des foreign keys de `current_user` (unit_id, user_id, residence_id)
- ✅ Validation côté serveur sur toutes les mutations
- ✅ Pas de confiance en l'input client pour les relations

### Base de données
- ✅ Migrations via Flask-Migrate uniquement
- ✅ Utilisation exclusive de l'ORM SQLAlchemy
- ✅ Validation des données côté serveur
- ✅ Transactions appropriées avec rollback sur erreur

### Secrets
- ✅ Utilisation des variables d'environnement Replit
- ✅ Pas de secrets dans le code
- ✅ SESSION_SECRET géré par Replit

---

## 📈 Décisions Architecturales

### PostgreSQL pour la Base de données
**Raison :** Intégration native Replit, support des transactions ACID, scalabilité, relations complexes

### Flask comme Framework Backend
**Raison :** Léger, flexible, excellent pour les API REST, écosystème riche

### Blueprints Flask pour l'Organisation
**Raison :** Séparation claire des responsabilités (auth, admin, resident), code modulaire et maintenable

### Services Partagés (ChargeCalculator, NotificationService)
**Raison :** Réutilisabilité, testabilité, séparation de la logique métier

### Sécurité par Défaut
**Raison :** Protection contre les vulnérabilités communes (CSRF, injection SQL, escalade de privilèges)

### Tailwind CSS
**Raison :** Développement rapide, design moderne, mobile-first, personnalisable

### PWA (À venir)
**Raison :** Expérience native sur mobile, mode offline, notifications push

---

## 📝 Bonnes Pratiques Appliquées

### Code Quality
- ✅ PEP 8 pour Python
- ✅ Commentaires en français
- ✅ Docstrings explicites
- ✅ Gestion appropriée des erreurs avec try/except
- ✅ Validation des données entrantes
- ✅ Retours JSON cohérents (`{'success': True/False, ...}`)

### Sécurité
- ✅ Jamais de SQL brut
- ✅ Hashing des mots de passe
- ✅ Vérifications d'autorisation systématiques
- ✅ Pas de foreign keys hard-codées
- ✅ Validation côté serveur obligatoire

### Architecture
- ✅ Séparation des responsabilités
- ✅ Services métier dans `utils/`
- ✅ Modèles dans des fichiers séparés
- ✅ Routes organisées par rôle (blueprints)
- ✅ Configuration centralisée

---

## 🎯 Roadmap

### ✅ Phase 1 : Infrastructure Backend (TERMINÉE)
- ✅ Création de la structure complète
- ✅ Configuration Flask complète
- ✅ Base de données PostgreSQL avec tous les modèles
- ✅ Authentification et autorisation sécurisée

### ✅ Phase 2 : Fonctionnalités Backend (TERMINÉE)
- ✅ Gestion des résidences et unités
- ✅ Système financier complet (charges, paiements, recouvrement)
- ✅ Appels de fonds avec distribution automatique
- ✅ Maintenance et carnet d'entretien
- ✅ Assemblées générales avec votes
- ✅ Contentieux
- ✅ Communication (news, sondages, documents)
- ✅ Services métier (ChargeCalculator, NotificationService)
- ✅ Correction des vulnérabilités de sécurité

### ⏳ Phase 3 : Frontend Complet (EN COURS)
- ✅ Landing page responsive
- ⏳ Dashboard superadmin avec toutes les fonctionnalités
- ⏳ Dashboard résident avec toutes les fonctionnalités
- ⏳ Formulaires interactifs
- ⏳ Tableaux de données
- ⏳ Modales et notifications
- ⏳ Design system cohérent

### ⏳ Phase 4 : PWA
- ⏳ Service Worker
- ⏳ Manifest
- ⏳ Mode offline
- ⏳ Notifications push
- ⏳ Installation sur écran d'accueil

### ⏳ Phase 5 : Tests et Production
- ⏳ Tests d'intégration pour l'autorisation
- ⏳ Tests unitaires
- ⏳ Optimisations de performance
- ⏳ Tests de charge
- ⏳ Déploiement final sur VPS

---

## 📊 Métriques de Développement

### Backend API
- **Modèles :** 16 modèles de données
- **Routes Admin :** 30+ endpoints
- **Routes Résidents :** 20+ endpoints
- **Services :** 2 services métier
- **Sécurité :** Vulnérabilités critiques corrigées ✅

### Code
- **Lignes de code Python :** ~2500+
- **Fichiers de modèles :** 11
- **Fichiers de routes :** 3
- **Services utilitaires :** 2

---

## 🚀 Prochain Sprint

### Priorité 1 : Interfaces Utilisateur
1. Dashboard superadmin complet
2. Formulaires de création/édition
3. Tableaux de données avec recherche/tri
4. Modales pour les actions

### Priorité 2 : UX/UI
1. Design system cohérent
2. Composants réutilisables
3. Feedback utilisateur (toasts, confirmations)
4. Loading states

### Priorité 3 : Tests
1. Tests d'intégration pour l'autorisation
2. Tests de validation des formulaires
3. Tests de flux utilisateur complets

---

## 📞 Notes pour les Développeurs

### Important à Savoir
1. **Port 5000 obligatoire** - Replit ne supporte que le port 5000
2. **Toujours vérifier residence_id** - Sur tous les endpoints résidents
3. **Jamais de SQL brut** - Utiliser l'ORM SQLAlchemy uniquement
4. **Dériver les FK de current_user** - Ne jamais faire confiance à l'input client
5. **Lire PROJECT_TRACKING.md** - Avant toute modification majeure

### Workflow de Développement
1. Créer/mettre à jour les modèles si nécessaire
2. Créer les routes API
3. Tester avec Postman/curl
4. Créer l'interface frontend
5. Tester le flux complet
6. Mettre à jour la documentation
7. Commit avec message descriptif en français

---

**Dernière mise à jour :** 24 octobre 2025  
**Version :** 0.2.0  
**Statut :** Backend MVP Complet ✅ | Frontend En Cours ⏳
