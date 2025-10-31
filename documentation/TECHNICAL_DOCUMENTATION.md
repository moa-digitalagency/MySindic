# Shabaka Syndic - Documentation Technique

## Architecture Globale

Shabaka Syndic est une application web monolithique basée sur Flask avec une architecture en couches :

```
┌─────────────────────────────────────────┐
│         Frontend (Templates)            │
│    HTML + TailwindCSS + Vanilla JS      │
└────────────────┬────────────────────────┘
                 │ HTTP/AJAX
┌────────────────▼────────────────────────┐
│         Flask Application               │
│   ┌─────────────────────────────────┐   │
│   │  Routes/Blueprints (API)        │   │
│   │  - auth_bp                      │   │
│   │  - admin_bp (32 endpoints)      │   │
│   │  - resident_bp (24 endpoints)   │   │
│   └────────────┬────────────────────┘   │
│                │                         │
│   ┌────────────▼────────────────────┐   │
│   │  Business Logic                 │   │
│   │  - ChargeCalculator             │   │
│   │  - NotificationService          │   │
│   └────────────┬────────────────────┘   │
│                │                         │
│   ┌────────────▼────────────────────┐   │
│   │  Models (SQLAlchemy ORM)        │   │
│   │  18 modèles interconnectés      │   │
│   └────────────┬────────────────────┘   │
└────────────────┼────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      PostgreSQL Database (Neon)         │
│         18 tables relationnelles        │
└─────────────────────────────────────────┘
```

## Stack Technique Détaillé

### Backend

#### Flask (3.0.0)
- **Application Factory Pattern** : `create_app()` dans `backend/app.py`
- **Blueprints** : Modularisation des routes
- **Context Processors** : Injection de variables globales (custom_head_code)
- **Error Handlers** : 404, 500
- **Middleware** : ProxyFix pour HTTPS, CORS

#### SQLAlchemy (2.0.23) + Flask-SQLAlchemy (3.1.1)
- **ORM Déclaratif** : `DeclarativeBase`
- **Relations** : ForeignKey, relationships avec lazy loading
- **Pool de connexions** : `pool_recycle=300`, `pool_pre_ping=True`
- **Transactions** : Commit/Rollback automatique avec context managers

#### Flask-Migrate (4.0.5)
- **Alembic** : Migrations de schéma
- **Commandes** :
  ```bash
  flask db init        # Initialiser migrations
  flask db migrate -m "Description"  # Créer migration
  flask db upgrade     # Appliquer migrations
  ```

#### Flask-Login (0.6.3)
- **User Loader** : Chargement automatique de l'utilisateur
- **LoginManager** : Configuration dans `app.py`
- **Décorateurs** : `@login_required`, `@superadmin_required`
- **Sessions** : Stockage côté serveur

#### Sécurité
- **Werkzeug** : Password hashing avec scrypt (32768:8:1)
- **PyJWT** : Tokens JWT pour authentification externe (si nécessaire)
- **Cryptography** : Chiffrement avancé
- **Validation** : email-validator

### Frontend

#### Templates Jinja2
```jinja2
{% extends "base.html" %}
{% block content %}
  <!-- Contenu spécifique -->
{% endblock %}
```

**Hiérarchie** :
- `base.html` : Layout principal
- `admin/admin_base.html` : Layout admin
- Pages spécifiques : `dashboard.html`, `finances.html`, etc.

#### Tailwind CSS (v3.x)
```html
<!-- CDN pour développement -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Configuration personnalisée -->
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

**Note Production** : Utiliser PostCSS pour optimisation

#### JavaScript (Vanilla ES6+)
```javascript
// Pattern Module
const App = {
  init() {
    this.setupEventListeners();
    this.loadData();
  },
  
  async fetchAPI(endpoint, options = {}) {
    const response = await fetch(endpoint, {
      headers: {
        'Content-Type': 'application/json'
      },
      ...options
    });
    return response.json();
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
```

#### Feather Icons
```html
<i data-feather="home"></i>
<script>feather.replace()</script>
```

### Base de Données

#### Schéma PostgreSQL

##### Relations Principales

```sql
-- User ←→ Residence (Many-to-One)
-- User ←→ Unit (Many-to-One)

-- Residence ←→ Unit (One-to-Many)
-- Residence ←→ Charge (One-to-Many)
-- Residence ←→ News (One-to-Many)
-- Residence ←→ GeneralAssembly (One-to-Many)

-- Charge ←→ ChargeDistribution (One-to-Many)
-- Unit ←→ ChargeDistribution (One-to-Many)
-- Unit ←→ Payment (One-to-Many)

-- Poll ←→ PollOption (One-to-Many)
-- Poll ←→ PollVote (One-to-Many)

-- GeneralAssembly ←→ Resolution (One-to-Many)
-- Resolution ←→ Vote (One-to-Many)
```

##### Modèle Détaillé : User

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='resident')
    # superadmin, admin, resident
    
    # Relations
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Méthodes
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_superadmin(self):
        return self.role == 'superadmin'
```

##### Index et Performances

```sql
-- Index automatiques
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_residence ON users(residence_id);
CREATE INDEX idx_users_unit ON users(unit_id);

-- Index composites recommandés
CREATE INDEX idx_charges_residence_status ON charges(residence_id, status);
CREATE INDEX idx_news_residence_published ON news(residence_id, is_published);
```

## Flux de Données

### Flux d'Authentification

```
1. User POST /api/auth/login
   ↓
2. Flask reçoit email + password
   ↓
3. Query User.query.filter_by(email=...)
   ↓
4. check_password(password) avec Werkzeug
   ↓
5. login_user(user, remember=True)
   ↓
6. Session stockée côté serveur
   ↓
7. Cookie de session renvoyé au client
   ↓
8. Requêtes futures incluent le cookie
   ↓
9. @login_required valide la session
```

### Flux de Création de Charge

```
1. Admin POST /api/admin/charges
   {
     residence_id, title, total_amount, 
     period_year, charge_type
   }
   ↓
2. Création de Charge (status='draft')
   ↓
3. Admin POST /api/admin/charges/:id/publish
   ↓
4. ChargeCalculator.calculate_distribution()
   ├─ Query tous les Units de la résidence
   ├─ Calcul par tantièmes ou surface
   ├─ Création de ChargeDistribution par unit
   └─ Update Charge.status = 'published'
   ↓
5. NotificationService.notify_charge_published()
   ├─ Query tous les résidents de la résidence
   └─ Envoi notifications/emails
```

### Flux de Vote sur Résolution

```
1. Resident GET /api/resident/assemblies/:id
   ↓
2. Vérification residence_id == current_user.residence_id
   ↓
3. Retour assembly + resolutions
   ↓
4. Resident POST /api/resident/resolutions/:id/vote
   { vote_value: 'for' | 'against' | 'abstain' }
   ↓
5. Vérification Resolution.assembly.residence_id
   ↓
6. Vérification si déjà voté (Vote.query.filter_by)
   ↓
7. Création ou Update de Vote
   ↓
8. Update compteurs Resolution
   (votes_for, votes_against, votes_abstain)
```

## Patterns et Principes

### 1. Sécurité par Design

**Principe** : Ne jamais faire confiance aux données client

```python
# ❌ MAUVAIS : Utilise residence_id de la requête
@admin_bp.route('/charges', methods=['POST'])
def create_charge():
    data = request.get_json()
    charge = Charge(residence_id=data['residence_id'])  # VULNÉRABLE

# ✅ BON : Utilise current_user
@resident_bp.route('/maintenance', methods=['POST'])
def create_maintenance():
    data = request.get_json()
    maintenance = MaintenanceRequest(
        residence_id=current_user.residence_id,  # SÉCURISÉ
        author_id=current_user.id              # SÉCURISÉ
    )
```

### 2. Repository Pattern (implicite via ORM)

```python
# Couche d'abstraction via SQLAlchemy
class Residence(db.Model):
    @classmethod
    def get_by_id(cls, residence_id):
        return cls.query.get(residence_id)
    
    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(is_active=True).all()
```

### 3. Service Layer

```python
# backend/utils/charge_calculator.py
class ChargeCalculator:
    @staticmethod
    def calculate_distribution(charge_id):
        """
        Calcule la répartition d'une charge
        selon les tantièmes ou surface
        """
        charge = Charge.query.get(charge_id)
        units = Unit.query.filter_by(residence_id=charge.residence_id).all()
        
        # Logique métier centralisée
        distributions = []
        for unit in units:
            amount = ChargeCalculator._calculate_unit_amount(charge, unit)
            dist = ChargeDistribution(
                charge_id=charge.id,
                unit_id=unit.id,
                amount=amount
            )
            distributions.append(dist)
        
        db.session.bulk_save_objects(distributions)
        db.session.commit()
        return distributions
```

### 4. Decorator Pattern

```python
def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Auth required'}), 401
        if not current_user.is_superadmin():
            return jsonify({'error': 'Admin required'}), 403
        return f(*args, **kwargs)
    return decorated_function
```

## Configuration

### Environnements

```python
# backend/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SESSION_SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # SSL requis
```

### Variables d'Environnement

| Variable | Description | Requis |
|----------|-------------|--------|
| DATABASE_URL | PostgreSQL connection string | Oui |
| SESSION_SECRET | Flask secret key | Oui |
| FLASK_ENV | development/production | Non |
| PORT | Port serveur (défaut: 5000) | Non |

## Tests

### Structure (à implémenter)

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_calculators.py
│   └── test_validators.py
├── integration/
│   ├── test_auth_flow.py
│   ├── test_charge_flow.py
│   └── test_assembly_flow.py
└── e2e/
    └── test_resident_journey.py
```

### Exemple de Test

```python
# tests/unit/test_models.py
import unittest
from backend.models.user import User

class TestUserModel(unittest.TestCase):
    def test_password_hashing(self):
        user = User(email='test@example.com')
        user.set_password('SecurePass123!')
        
        self.assertTrue(user.check_password('SecurePass123!'))
        self.assertFalse(user.check_password('WrongPass'))
    
    def test_is_superadmin(self):
        user = User(email='admin@example.com', role='superadmin')
        self.assertTrue(user.is_superadmin())
        
        user.role = 'resident'
        self.assertFalse(user.is_superadmin())
```

## Performance et Optimisation

### 1. Requêtes N+1 Prevention

```python
# ❌ MAUVAIS : N+1 queries
charges = Charge.query.all()
for charge in charges:
    print(charge.residence.name)  # Query pour chaque charge

# ✅ BON : Eager loading
charges = Charge.query.options(
    db.joinedload(Charge.residence)
).all()
```

### 2. Pagination

```python
# Pour grandes listes
@admin_bp.route('/payments', methods=['GET'])
def get_payments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Payment.query.order_by(
        Payment.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'payments': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })
```

### 3. Caching (à implémenter)

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL')
})

@cache.cached(timeout=300, key_prefix='residence_stats')
def get_residence_stats(residence_id):
    # Calculs coûteux mis en cache 5 minutes
    return compute_stats(residence_id)
```

### 4. Index Database

```sql
-- Créer des index pour les requêtes fréquentes
CREATE INDEX idx_maintenance_residence_status 
ON maintenance_requests(residence_id, status);

CREATE INDEX idx_payments_unit_status 
ON payments(unit_id, status);

CREATE INDEX idx_charge_dist_unit_paid 
ON charge_distributions(unit_id, is_paid);
```

## Sécurité Avancée

### 1. Protection CSRF

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Exemption pour API externe si nécessaire
@csrf.exempt
@app.route('/api/webhook', methods=['POST'])
def webhook():
    pass
```

### 2. Rate Limiting (à implémenter)

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: current_user.id if current_user.is_authenticated else request.remote_addr
)

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass
```

### 3. Headers de Sécurité

```python
@app.after_request
def set_secure_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### 4. Validation des Entrées

```python
from email_validator import validate_email, EmailNotValidError

def validate_user_input(data):
    # Email
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        raise ValueError('Email invalide')
    
    # Password strength
    if len(data['password']) < 8:
        raise ValueError('Mot de passe trop court')
    
    # Sanitize strings
    data['first_name'] = bleach.clean(data['first_name'])
    data['last_name'] = bleach.clean(data['last_name'])
```

## Monitoring et Logging

### 1. Application Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    logger.info(f'{request.method} {request.path} - {current_user.email if current_user.is_authenticated else "Anonymous"}')

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Server Error: {error}', exc_info=True)
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
```

### 2. Performance Monitoring

```python
import time

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        if elapsed > 1.0:  # Log slow requests
            logger.warning(f'Slow request: {request.path} took {elapsed:.2f}s')
    return response
```

## Déploiement Avancé

### 1. Gunicorn Configuration

```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4  # 2-4 x CPU cores
worker_class = "sync"
worker_connections = 1000
keepalive = 5
timeout = 30
```

### 2. Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name mysindic.ma;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /var/www/shabaka-syndic/frontend/static;
        expires 30d;
    }
}
```

### 3. Systemd Service

```ini
[Unit]
Description=Shabaka Syndic Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/shabaka-syndic
Environment="PATH=/var/www/shabaka-syndic/venv/bin"
ExecStart=/var/www/shabaka-syndic/venv/bin/gunicorn --config gunicorn.conf.py main:app

[Install]
WantedBy=multi-user.target
```

### 4. Database Backup

```bash
#!/bin/bash
# backup.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > backups/mysindic_$TIMESTAMP.sql
```

## Troubleshooting

### Problèmes Courants

#### 1. "relation does not exist"
```bash
# Réinitialiser la base de données
python reset_db.py
python init_db.py
```

#### 2. "session is not JSON serializable"
```python
# S'assurer que to_dict() retourne des types sérialisables
def to_dict(self):
    return {
        'id': self.id,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }
```

#### 3. "CORS errors"
```python
# Vérifier Flask-CORS
CORS(app, origins=['https://your-domain.com'])
```

## Best Practices

### 1. Code Style
- PEP 8 pour Python
- Docstrings pour toutes les fonctions publiques
- Type hints où approprié

### 2. Git Workflow
```bash
git checkout -b feature/new-feature
# Développement
git commit -m "feat: add new feature"
git push origin feature/new-feature
# Pull Request → Review → Merge
```

### 3. Database Migrations
```bash
# Toujours créer une migration pour les changements de schéma
flask db migrate -m "Add column X to table Y"
flask db upgrade
```

### 4. Error Handling
```python
# Toujours gérer les exceptions
try:
    # Operations
    db.session.commit()
except SQLAlchemyError as e:
    db.session.rollback()
    logger.error(f'Database error: {e}')
    return jsonify({'error': 'Database error'}), 500
except Exception as e:
    logger.error(f'Unexpected error: {e}')
    return jsonify({'error': 'Internal error'}), 500
```

---

© 2025 Shabaka Syndic - Documentation Technique
