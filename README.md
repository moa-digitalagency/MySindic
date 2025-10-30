# MySindic - Gestion Moderne de Copropriété

![MySindic Banner](frontend/static/images/modern_apartment_bui_04cc653f.jpg)

**Solution complète et digitale pour les syndics et résidents au Maroc**

MySindic est une application web progressive (PWA) moderne conçue pour simplifier et digitaliser la gestion des copropriétés au Maroc. Elle offre une interface intuitive et responsive pour les administrateurs de syndic et les résidents.

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Comptes de Démonstration](#-comptes-de-démonstration)
- [API Documentation](#-api-documentation)
- [Sécurité](#-sécurité)
- [Déploiement](#-déploiement)

## ✨ Fonctionnalités

### 👨‍💼 Pour les Superadmins

#### Gestion des Résidences
- ✅ Création et configuration de nouvelles résidences avec assistant wizard
- ✅ Gestion complète des copropriétés (CRUD)
- ✅ Gestion des lots/unités avec informations propriétaires
- ✅ Support multi-résidences

#### Gestion Financière
- ✅ **Appels de fonds** : Création et publication des charges
- ✅ **Répartition automatique** : Calcul par tantièmes/surface
- ✅ **Suivi des paiements** : Validation et historique
- ✅ **Recouvrement** : Suivi des impayés par lot
- ✅ **Solde en temps réel** : Consultation du solde de chaque lot

#### Maintenance et Travaux
- ✅ Suivi des demandes de maintenance des résidents
- ✅ Gestion du statut (pending, in_progress, completed)
- ✅ Attribution aux prestataires
- ✅ **Carnet d'entretien** : Historique complet des interventions
- ✅ Documentation des travaux avec factures et garanties

#### Assemblées Générales
- ✅ Organisation complète des AG (convocation, ordre du jour)
- ✅ Gestion des résolutions avec vote électronique
- ✅ Envoi automatique des convocations
- ✅ Suivi des présences
- ✅ Gestion des votes (pour, contre, abstention)

#### Communication
- ✅ **Actualités** : Publication de news avec épinglage
- ✅ **Sondages** : Création de questionnaires avec options multiples
- ✅ Notifications automatiques

#### Gestion des Contentieux
- ✅ Suivi des litiges et procédures juridiques
- ✅ Gestion des contentieux par lot

#### Administration
- ✅ Gestion des utilisateurs et rôles
- ✅ Dashboard avec statistiques clés
- ✅ Gestion des documents officiels
- ✅ Paramètres de l'application
- ✅ Code personnalisé (injection <head>)

### 🏠 Pour les Résidents

#### Dashboard Personnalisé
- ✅ Vue d'ensemble : maintenance, solde, AG, actualités
- ✅ Indicateurs clés en temps réel
- ✅ Notifications importantes

#### Maintenance
- ✅ **Création de demandes** : Formulaire simplifié par catégorie
- ✅ **Suivi en temps réel** : Statut et progression
- ✅ Consultation de l'historique des interventions
- ✅ Accès au carnet d'entretien de la résidence

#### Finances
- ✅ **Consultation des charges** : Historique et détails
- ✅ **Charges impayées** : Liste claire des dus
- ✅ **Solde du compte** : Situation financière à jour
- ✅ **Déclaration de paiement** : Enregistrement facile
- ✅ Historique complet des paiements

#### Information et Communication
- ✅ **Actualités** : Fil d'infos de la résidence
- ✅ **Documents** : Accès aux documents publics
- ✅ **Sondages** : Participation et résultats
- ✅ Notifications personnalisées

#### Assemblées Générales
- ✅ Consultation des AG (passées et à venir)
- ✅ Confirmation de présence en ligne
- ✅ Vote sur les résolutions
- ✅ Consultation des résultats

### 🔐 Authentification et Sécurité

- ✅ Inscription et connexion sécurisées
- ✅ Hashing des mots de passe (Werkzeug)
- ✅ Gestion des rôles (Superadmin, Admin Syndic, Propriétaire, Résident)
- ✅ Protection des routes par authentification
- ✅ Validation stricte residence_id (protection escalade privilèges)
- ✅ Sessions sécurisées avec Flask-Login

## 🛠 Technologies

### Backend
- **Framework** : Flask 3.0.0
- **ORM** : SQLAlchemy 2.0.23 + Flask-SQLAlchemy 3.1.1
- **Base de données** : PostgreSQL (Neon)
- **Migrations** : Flask-Migrate 4.0.5
- **Authentification** : Flask-Login 0.6.3
- **Sécurité** : Werkzeug 3.0.1, PyJWT 2.8.0, cryptography 41.0.7
- **Serveur** : Gunicorn 21.2.0
- **CORS** : Flask-CORS 4.0.0
- **Email** : Flask-Mail 0.9.1

### Frontend
- **HTML5** : Templates Jinja2
- **CSS** : Tailwind CSS 3.x (CDN)
- **JavaScript** : Vanilla JS moderne (ES6+)
- **Icons** : Feather Icons
- **PWA** : Service Workers, Manifest

### Base de Données

**18 Modèles de Données** :
1. User - Utilisateurs
2. Residence - Copropriétés
3. Unit - Lots/appartements
4. MaintenanceRequest - Demandes de maintenance
5. MaintenanceLog - Carnet d'entretien
6. Document - Documents officiels
7. Charge - Appels de fonds
8. ChargeDistribution - Répartition des charges
9. Payment - Paiements
10. News - Actualités
11. Poll - Sondages
12. PollOption - Options de sondage
13. PollVote - Votes sur sondages
14. GeneralAssembly - Assemblées générales
15. Resolution - Résolutions d'AG
16. Vote - Votes sur résolutions
17. Attendance - Présences aux AG
18. Litigation - Litiges

## 🚀 Installation

### Prérequis
- Python 3.11+
- PostgreSQL
- pip

### Installation Locale

```bash
# Cloner le repository
git clone <repo-url>
cd mysindic

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
export DATABASE_URL="postgresql://user:password@localhost/mysindic"
export SESSION_SECRET="votre-secret-key-aleatoire"

# Initialiser la base de données avec données de démo
python init_db.py

# Lancer l'application
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### Sur Replit

L'application est pré-configurée pour Replit :
1. Les dépendances s'installent automatiquement
2. La base de données PostgreSQL est provisionnée
3. Le workflow démarre automatiquement sur le port 5000
4. Les données de démo sont initialisées au premier lancement

## 📖 Utilisation

### Accès à l'Application

**URL locale** : `http://localhost:5000`
**URL Replit** : Fournie par Replit dans l'onglet Webview

### 🔑 Comptes de Démonstration

L'application est initialisée avec 5 comptes de test :

| Rôle | Email | Mot de passe | Description |
|------|-------|--------------|-------------|
| **Super Admin** | admin@mysindic.ma | Admin123! | Accès complet à toutes les fonctionnalités |
| **Admin Syndic** | admin.syndic@mysindic.ma | Admin123! | Administration d'une résidence spécifique |
| **Propriétaire** | owner@mysindic.ma | Owner123! | Propriétaire d'un lot (Lot 101) |
| **Résident 1** | resident@mysindic.ma | Resident123! | Résident (Lot 201) |
| **Résident 2** | karim@mysindic.ma | Resident123! | Résident (Lot 301) |

### Données de Démo Incluses

- **1 résidence** : "Les Jardins de l'Atlas" à Casablanca
- **5 unités** : Appartements de 75m² à 150m²
- **1 appel de fonds** : Charges Q1 2025 (50,000 MAD)
- **2 paiements validés**
- **2 demandes de maintenance** (fuite d'eau, problème électrique)
- **2 entrées carnet d'entretien**
- **2 actualités**

## 📚 API Documentation

### Endpoints Authentification (5)

```
POST   /api/auth/register      - Inscription
POST   /api/auth/login         - Connexion
POST   /api/auth/logout        - Déconnexion
GET    /api/auth/me            - Utilisateur actuel
GET    /api/auth/check         - Vérifier authentification
```

### Endpoints Admin (32)

#### Dashboard
```
GET    /api/admin/dashboard    - Statistiques complètes
```

#### Résidences et Unités
```
GET    /api/admin/residences                    - Liste des résidences
POST   /api/admin/residences                    - Créer résidence
PUT    /api/admin/residences/:id                - Modifier résidence
GET    /api/admin/residences/:id/units          - Liste des unités
POST   /api/admin/residences/:id/units          - Créer unité
POST   /api/admin/units                         - Créer unité (simplifié)
```

#### Finances
```
GET    /api/admin/charges                       - Liste des charges
POST   /api/admin/charges                       - Créer charge
POST   /api/admin/charges/:id/publish           - Publier et répartir
GET    /api/admin/charges/:id/distributions     - Répartitions
GET    /api/admin/payments                      - Liste des paiements
POST   /api/admin/payments/:id/validate         - Valider paiement
GET    /api/admin/units/:id/balance             - Solde d'un lot
```

#### Actualités
```
GET    /api/admin/news         - Liste actualités
POST   /api/admin/news         - Créer actualité
PUT    /api/admin/news/:id     - Modifier actualité
DELETE /api/admin/news/:id     - Supprimer actualité
```

#### Maintenance
```
GET    /api/admin/maintenance           - Liste demandes
PUT    /api/admin/maintenance/:id       - Modifier demande
```

#### Carnet d'Entretien
```
GET    /api/admin/maintenance-logs      - Liste interventions
POST   /api/admin/maintenance-logs      - Créer intervention
```

#### Assemblées Générales
```
GET    /api/admin/assemblies                           - Liste AG
POST   /api/admin/assemblies                           - Créer AG
PUT    /api/admin/assemblies/:id                       - Modifier AG
POST   /api/admin/assemblies/:id/resolutions           - Créer résolution
POST   /api/admin/assemblies/:id/send-convocations     - Envoyer convocations
```

#### Documents
```
GET    /api/admin/documents     - Liste documents
POST   /api/admin/documents     - Upload document
DELETE /api/admin/documents/:id - Supprimer document
```

#### Litiges
```
GET    /api/admin/litigations   - Liste litiges
POST   /api/admin/litigations   - Créer litige
PUT    /api/admin/litigations/:id - Modifier litige
```

#### Sondages
```
GET    /api/admin/polls         - Liste sondages
POST   /api/admin/polls         - Créer sondage
POST   /api/admin/polls/:id/close - Fermer sondage
```

#### Utilisateurs
```
GET    /api/admin/users         - Liste utilisateurs
PUT    /api/admin/users/:id     - Modifier utilisateur
```

#### Paramètres
```
GET    /api/admin/settings/custom-head      - Code <head>
POST   /api/admin/settings/custom-head      - Sauvegarder code
```

### Endpoints Résidents (24)

#### Dashboard
```
GET    /api/resident/dashboard  - Vue d'ensemble personnalisée
```

#### Actualités
```
GET    /api/resident/news       - Liste actualités
GET    /api/resident/news/:id   - Détail actualité
```

#### Maintenance
```
POST   /api/resident/maintenance        - Créer demande
GET    /api/resident/maintenance        - Mes demandes
GET    /api/resident/maintenance/:id    - Détail demande
GET    /api/resident/maintenance-logs   - Carnet d'entretien
```

#### Finances
```
GET    /api/resident/charges            - Mes charges
GET    /api/resident/charges/unpaid     - Charges impayées
GET    /api/resident/balance            - Mon solde
POST   /api/resident/payments           - Déclarer paiement
GET    /api/resident/payments           - Historique paiements
```

#### Documents
```
GET    /api/resident/documents          - Documents publics
GET    /api/resident/documents/:id      - Détail document
```

#### Sondages
```
GET    /api/resident/polls              - Sondages actifs
GET    /api/resident/polls/:id          - Détail sondage
POST   /api/resident/polls/:id/vote     - Voter
```

#### Assemblées Générales
```
GET    /api/resident/assemblies                 - Liste AG
GET    /api/resident/assemblies/:id             - Détail AG
POST   /api/resident/assemblies/:id/attend      - Confirmer présence
POST   /api/resident/resolutions/:id/vote       - Voter résolution
```

### Format des Réponses

#### Succès
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation réussie"
}
```

#### Erreur
```json
{
  "success": false,
  "error": "Description de l'erreur"
}
```

## 🔒 Sécurité

### Mesures Implémentées

1. **Authentification**
   - Hashing sécurisé des mots de passe (Werkzeug scrypt)
   - Sessions sécurisées avec Flask-Login
   - Token CSRF automatique

2. **Autorisation**
   - Contrôle d'accès basé sur les rôles (RBAC)
   - Décorateurs `@login_required` et `@superadmin_required`
   - Validation stricte `residence_id` sur tous les endpoints

3. **Protection des Données**
   - Aucune exposition de secrets ou clés
   - Filtrage par `residence_id` et `user_id` automatique
   - Protection contre l'escalade de privilèges

4. **Validation**
   - Validation des entrées utilisateur
   - Protection contre les injections SQL (ORM)
   - Sanitization des données

5. **HTTPS**
   - Proxy Fix configuré pour HTTPS
   - Headers de sécurité appropriés

## 🚀 Déploiement

### Déploiement sur Replit

L'application est configurée pour le déploiement automatique sur Replit :

```yaml
deployment_target: autoscale
run: ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

Cliquez sur le bouton "Deploy" dans Replit pour publier.

### Variables d'Environnement Requises

```bash
DATABASE_URL=postgresql://...       # Fourni automatiquement par Replit
SESSION_SECRET=...                  # Généré automatiquement
PGHOST=...                         # Fourni par Replit
PGPORT=...                         # Fourni par Replit
PGUSER=...                         # Fourni par Replit
PGPASSWORD=...                     # Fourni par Replit
PGDATABASE=...                     # Fourni par Replit
```

### Déploiement sur VPS

Un script de déploiement est fourni :

```bash
chmod +x deploy_vps.sh
./deploy_vps.sh
```

Le script :
- Configure un environnement virtuel
- Installe les dépendances
- Configure Nginx
- Installe systemd pour Gunicorn
- Configure SSL avec Certbot

## 📝 Structure du Projet

```
mysindic/
├── backend/
│   ├── models/           # 18 modèles SQLAlchemy
│   ├── routes/           # Blueprints API (auth, admin, resident)
│   ├── utils/            # Utilitaires (calculs, notifications)
│   ├── app.py            # Application Flask principale
│   ├── config.py         # Configuration
│   └── init_demo_data.py # Initialisation données démo
├── frontend/
│   ├── static/
│   │   ├── css/          # Styles Tailwind
│   │   ├── js/           # JavaScript
│   │   └── images/       # Assets
│   └── templates/        # Templates Jinja2
│       ├── admin/        # Pages admin
│       ├── resident/     # Pages résident
│       └── auth/         # Pages authentification
├── main.py               # Point d'entrée
├── requirements.txt      # Dépendances Python
└── README.md            # Cette documentation
```

## 🤝 Support

Pour toute question ou problème :
- **Email** : moa@myoneart.com
- **Site** : www.myoneart.com

## 📄 Licence

© 2025 MySindic - Shabaka Syndic par Aisance KALONJI

---

**MySindic** - Gestion Moderne de Copropriété pour le Maroc 🇲🇦
