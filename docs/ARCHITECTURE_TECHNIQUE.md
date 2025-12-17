# Architecture Technique - Shabaka Syndic

Ce document décrit l'architecture logicielle de Shabaka Syndic, les choix techniques et l'organisation du code.

## Vue d'Ensemble

Shabaka Syndic est une application web monolithique utilisant le framework Flask. L'architecture suit un modèle en couches avec séparation des responsabilités.

```
┌─────────────────────────────────────────────────────┐
│                    Client Web                        │
│           (Navigateur - HTML/CSS/JS)                 │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/HTTPS
┌──────────────────────▼──────────────────────────────┐
│                   Gunicorn                           │
│              (Serveur WSGI)                          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│               Flask Application                      │
│  ┌─────────────────────────────────────────────┐    │
│  │            Routes (Blueprints)              │    │
│  │   auth_bp  │  admin_bp  │  resident_bp      │    │
│  └─────────────────────┬───────────────────────┘    │
│                        │                             │
│  ┌─────────────────────▼───────────────────────┐    │
│  │           Services (Logique Métier)         │    │
│  │  ChargeCalculator │ NotificationService     │    │
│  │  AgoraService                               │    │
│  └─────────────────────┬───────────────────────┘    │
│                        │                             │
│  ┌─────────────────────▼───────────────────────┐    │
│  │            Models (SQLAlchemy ORM)          │    │
│  │         20 modèles interconnectés           │    │
│  └─────────────────────┬───────────────────────┘    │
└────────────────────────┼────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│                   PostgreSQL                         │
│              (Base de données)                       │
└─────────────────────────────────────────────────────┘
```

## Stack Technique

### Backend

| Composant | Version | Rôle |
|-----------|---------|------|
| Python | 3.11 | Langage principal |
| Flask | 3.0.0 | Framework web |
| SQLAlchemy | 2.0.23 | ORM pour base de données |
| Flask-SQLAlchemy | 3.1.1 | Intégration Flask/SQLAlchemy |
| Flask-Migrate | 4.0.5 | Migrations de schéma |
| Flask-Login | 0.6.3 | Gestion des sessions utilisateur |
| Flask-CORS | 4.0.0 | Gestion des requêtes cross-origin |
| Flask-Mail | 0.9.1 | Envoi d'emails |
| Werkzeug | 3.0.1 | Utilitaires WSGI, hashing |
| PyJWT | 2.8.0 | Tokens JWT |
| Gunicorn | 21.2.0 | Serveur WSGI production |

### Frontend

| Composant | Rôle |
|-----------|------|
| Jinja2 | Moteur de templates |
| Tailwind CSS | Framework CSS (via CDN) |
| Feather Icons | Icônes |
| JavaScript ES6+ | Interactivité côté client |

### Base de Données

PostgreSQL hébergé via Replit Database ou tout serveur PostgreSQL compatible.

---

## Structure du Projet

```
shabaka-syndic/
├── backend/
│   ├── models/
│   │   ├── __init__.py         # Initialisation SQLAlchemy
│   │   ├── user.py             # Modèle utilisateur
│   │   ├── residence.py        # Résidences et lots
│   │   ├── residence_admin.py  # Association admin-résidence
│   │   ├── maintenance.py      # Demandes de maintenance
│   │   ├── maintenance_comment.py
│   │   ├── maintenance_document.py
│   │   ├── maintenance_log.py  # Carnet d'entretien
│   │   ├── charge.py           # Appels de fonds
│   │   ├── payment.py          # Paiements
│   │   ├── news.py             # Actualités
│   │   ├── poll.py             # Sondages
│   │   ├── general_assembly.py # Assemblées générales
│   │   ├── document.py         # Documents
│   │   ├── litigation.py       # Contentieux
│   │   └── app_settings.py     # Paramètres
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentification
│   │   ├── admin.py            # API administrateur
│   │   └── resident.py         # API résident
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── charge_calculator.py
│   │   ├── notification_service.py
│   │   └── agora_service.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── decorators.py       # Décorateurs d'autorisation
│   │
│   ├── app.py                  # Factory Flask
│   ├── config.py               # Configuration
│   └── init_demo_data.py       # Données de démonstration
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   └── main.js
│   │   ├── images/
│   │   ├── favicon/
│   │   ├── manifest.json       # PWA
│   │   └── sw.js               # Service Worker
│   │
│   └── templates/
│       ├── base.html           # Template de base
│       ├── index.html          # Page d'accueil
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── admin/
│       │   ├── admin_base.html
│       │   ├── dashboard.html
│       │   ├── residences.html
│       │   ├── finances.html
│       │   ├── maintenance.html
│       │   ├── users.html
│       │   ├── assemblies.html
│       │   └── ...
│       └── resident/
│           ├── resident_base.html
│           ├── dashboard.html
│           ├── maintenance.html
│           ├── finances.html
│           └── ...
│
├── docs/                       # Documentation
├── main.py                     # Point d'entrée
├── requirements.txt            # Dépendances
└── replit.md                   # Configuration Replit
```

---

## Modèles de Données

### Diagramme des Relations

```
User ──────────────┐
  │                │
  │ N:1            │ N:1
  ▼                ▼
Residence ◄────── Unit
  │                │
  │ 1:N            │ 1:N
  ├──► MaintenanceRequest
  ├──► Charge ──────► ChargeDistribution
  ├──► News
  ├──► Poll
  ├──► GeneralAssembly
  ├──► Document
  └──► Litigation

GeneralAssembly ──► Resolution ──► Vote
                ──► Attendance

Poll ──► PollOption ──► PollVote

MaintenanceRequest ──► MaintenanceComment
                   ──► MaintenanceDocument
                   ──► MaintenanceLog
```

### Modèle User

Gère l'authentification et les rôles.

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='resident')
    # Rôles : superadmin, admin, owner, resident
    
    is_active = db.Column(db.Boolean, default=True)
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
```

### Modèle Residence

Représente une copropriété.

```python
class Residence(db.Model):
    __tablename__ = 'residences'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20))
    total_units = db.Column(db.Integer, nullable=False)
    syndic_name = db.Column(db.String(200))
    syndic_email = db.Column(db.String(120))
    syndic_phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    units = db.relationship('Unit', backref='residence')
    maintenance_requests = db.relationship('MaintenanceRequest')
    charges = db.relationship('Charge')
    news = db.relationship('News')
```

### Modèle Unit (Lot)

Représente un appartement ou local.

```python
class Unit(db.Model):
    __tablename__ = 'units'
    
    id = db.Column(db.Integer, primary_key=True)
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'))
    unit_number = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.Integer)
    building = db.Column(db.String(50))
    unit_type = db.Column(db.String(50))
    surface_area = db.Column(db.Float)
    owner_name = db.Column(db.String(200))
    owner_email = db.Column(db.String(120))
    is_occupied = db.Column(db.Boolean, default=True)
```

### Modèle Charge et ChargeDistribution

Gestion des appels de fonds.

```python
class Charge(db.Model):
    __tablename__ = 'charges'
    
    id = db.Column(db.Integer, primary_key=True)
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'))
    title = db.Column(db.String(200), nullable=False)
    charge_type = db.Column(db.String(50))  # courante, exceptionnelle, travaux
    total_amount = db.Column(db.Numeric(10, 2))
    period_month = db.Column(db.Integer)
    period_year = db.Column(db.Integer)
    status = db.Column(db.String(20), default='draft')  # draft, published, closed
    due_date = db.Column(db.DateTime)

class ChargeDistribution(db.Model):
    __tablename__ = 'charge_distributions'
    
    id = db.Column(db.Integer, primary_key=True)
    charge_id = db.Column(db.Integer, db.ForeignKey('charges.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    amount = db.Column(db.Numeric(10, 2))
    is_paid = db.Column(db.Boolean, default=False)
```

---

## Routes et API

### Organisation en Blueprints

L'application utilise trois blueprints Flask :

1. **auth_bp** (`/api/auth`) - Authentification
2. **admin_bp** (`/api/admin`) - Fonctions administrateur
3. **resident_bp** (`/api/resident`) - Fonctions résident

### Décorateurs d'Autorisation

```python
# Dans backend/utils/decorators.py

@login_required  # Flask-Login standard
def route():
    pass

@superadmin_required  # Vérifie role == 'superadmin'
def admin_only_route():
    pass

@admin_or_superadmin_required  # Vérifie role in ['admin', 'superadmin']
def syndic_route():
    pass

@residence_access_required  # Vérifie accès à la résidence
def residence_route(residence_id):
    pass

@owner_or_above_required  # Vérifie role in ['owner', 'admin', 'superadmin']
def owner_route():
    pass
```

### Pattern de Route Typique

```python
@admin_bp.route('/charges', methods=['GET'])
@login_required
@admin_or_superadmin_required
def get_charges():
    try:
        residence_ids = get_user_residence_ids()
        
        if residence_ids is None:
            # Superadmin : accès à tout
            charges = Charge.query.all()
        else:
            # Admin : filtrer par résidences assignées
            charges = Charge.query.filter(
                Charge.residence_id.in_(residence_ids)
            ).all()
        
        return jsonify({
            'success': True,
            'charges': [c.to_dict() for c in charges]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

---

## Services Métier

### ChargeCalculator

Calcul et répartition des charges.

```python
class ChargeCalculator:
    @staticmethod
    def calculate_distribution(charge_id):
        """Répartit une charge entre tous les lots"""
        charge = Charge.query.get(charge_id)
        units = Unit.query.filter_by(residence_id=charge.residence_id).all()
        
        # Répartition égale
        amount_per_unit = charge.total_amount / len(units)
        
        for unit in units:
            distribution = ChargeDistribution(
                charge_id=charge_id,
                unit_id=unit.id,
                amount=amount_per_unit
            )
            db.session.add(distribution)
        
        db.session.commit()
    
    @staticmethod
    def get_unit_balance(unit_id):
        """Calcule le solde d'un lot"""
        # Total des charges
        distributions = ChargeDistribution.query.filter_by(unit_id=unit_id).all()
        total_charges = sum(float(d.amount) for d in distributions)
        
        # Total des paiements validés
        payments = Payment.query.filter_by(
            unit_id=unit_id, 
            status='validated'
        ).all()
        total_payments = sum(float(p.amount) for p in payments)
        
        balance = total_payments - total_charges
        
        return {
            'total_charges': total_charges,
            'total_payments': total_payments,
            'balance': balance,
            'status': 'credit' if balance > 0 else 'debit' if balance < 0 else 'balanced'
        }
```

### AgoraService

Intégration vidéoconférence pour les AG en ligne.

```python
class AgoraService:
    @staticmethod
    def generate_rtc_token(channel_name, uid, role='publisher'):
        """Génère un token RTC pour Agora.io"""
        app_id = os.environ.get('AGORA_APP_ID')
        app_certificate = os.environ.get('AGORA_APP_CERTIFICATE')
        
        if not app_id or not app_certificate:
            return None
        
        expiration = int(time.time()) + 3600
        agora_role = RtcTokenBuilder.Role_Publisher
        
        token = RtcTokenBuilder.buildTokenWithUid(
            app_id,
            app_certificate,
            channel_name,
            uid,
            agora_role,
            expiration
        )
        
        return token
```

---

## Frontend

### Templates Jinja2

Hiérarchie des templates :

```
base.html
├── admin/admin_base.html
│   ├── dashboard.html
│   ├── residences.html
│   └── ...
└── resident/resident_base.html
    ├── dashboard.html
    └── ...
```

### Configuration Tailwind

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: '#6366f1',
          secondary: '#8b5cf6'
        }
      }
    }
  }
</script>
```

### JavaScript Côté Client

Pattern utilisé pour les appels API :

```javascript
async function fetchAPI(endpoint, options = {}) {
    const response = await fetch(endpoint, {
        headers: {
            'Content-Type': 'application/json'
        },
        ...options
    });
    return response.json();
}

// Exemple d'utilisation
async function loadCharges() {
    const data = await fetchAPI('/api/admin/charges');
    if (data.success) {
        renderCharges(data.charges);
    } else {
        showError(data.error);
    }
}
```

---

## Configuration

### Variables d'Environnement

| Variable | Description | Requis |
|----------|-------------|--------|
| DATABASE_URL | URL de connexion PostgreSQL | Oui |
| SESSION_SECRET | Clé secrète Flask | Oui |
| FLASK_ENV | development / production | Non |
| AGORA_APP_ID | ID application Agora.io | Non |
| AGORA_APP_CERTIFICATE | Certificat Agora.io | Non |
| MAIL_SERVER | Serveur SMTP | Non |
| MAIL_PORT | Port SMTP | Non |
| MAIL_USERNAME | Utilisateur SMTP | Non |
| MAIL_PASSWORD | Mot de passe SMTP | Non |

### Configuration Flask

```python
class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
```

---

## Patterns et Bonnes Pratiques

### Sécurité par Design

Toujours filtrer par les données de l'utilisateur connecté :

```python
# Correct : utilise current_user
maintenance = MaintenanceRequest(
    residence_id=current_user.residence_id,
    author_id=current_user.id
)

# Incorrect : utilise les données de la requête
maintenance = MaintenanceRequest(
    residence_id=data['residence_id'],  # Vulnérable
    author_id=data['user_id']           # Vulnérable
)
```

### Gestion des Erreurs

```python
@admin_bp.route('/charges', methods=['POST'])
def create_charge():
    try:
        # Logique
        db.session.commit()
        return jsonify({'success': True}), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
```

### Sérialisation

Chaque modèle implémente `to_dict()` :

```python
def to_dict(self):
    return {
        'id': self.id,
        'title': self.title,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }
```

---

## Déploiement

### Commande de Production

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Configuration Gunicorn

```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 5
```

### Replit

Le fichier `.replit` configure automatiquement le déploiement sur Replit avec la commande gunicorn appropriée.

---

## Évolutions Futures

- Cache Redis pour les requêtes fréquentes
- Tests automatisés (pytest)
- Application mobile (React Native ou Flutter)
- Intégration paiement en ligne
- Module comptabilité avancé
- API GraphQL optionnelle
