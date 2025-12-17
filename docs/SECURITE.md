# Sécurité - Shabaka Syndic

Ce document décrit les mesures de sécurité implémentées dans Shabaka Syndic et les bonnes pratiques à suivre.

## Vue d'Ensemble

Shabaka Syndic manipule des données sensibles : informations personnelles, données financières, documents officiels. La sécurité est intégrée à tous les niveaux de l'application.

---

## Authentification

### Hashing des Mots de Passe

Les mots de passe ne sont jamais stockés en clair. L'application utilise Werkzeug avec l'algorithme scrypt :

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing
password_hash = generate_password_hash(password)

# Vérification
is_valid = check_password_hash(password_hash, password)
```

Caractéristiques :
- Algorithme scrypt (paramètres : n=32768, r=8, p=1)
- Sel unique pour chaque mot de passe
- Résistance aux attaques par force brute

### Gestion des Sessions

Flask-Login gère les sessions utilisateur :

```python
login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.session_protection = 'strong'

REMEMBER_COOKIE_DURATION = timedelta(days=7)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

Protections :
- Cookie HttpOnly (inaccessible par JavaScript)
- Cookie Secure (HTTPS uniquement en production)
- SameSite Lax (protection CSRF partielle)
- Protection forte des sessions

---

## Autorisation

### Système de Rôles

L'application implémente un contrôle d'accès basé sur les rôles (RBAC) :

| Rôle | Niveau | Accès |
|------|--------|-------|
| Superadmin | 4 | Toutes les résidences, toutes les fonctions |
| Admin | 3 | Résidences assignées, gestion complète |
| Owner | 2 | Sa résidence, fonctions étendues |
| Resident | 1 | Sa résidence, fonctions limitées |

### Décorateurs de Protection

```python
@login_required
# Vérifie que l'utilisateur est connecté

@superadmin_required
# Vérifie que l'utilisateur est superadmin

@admin_or_superadmin_required
# Vérifie que l'utilisateur est admin ou superadmin

@residence_access_required
# Vérifie que l'utilisateur a accès à la résidence

@owner_or_above_required
# Vérifie que l'utilisateur est propriétaire, admin ou superadmin
```

### Vérification de l'Accès aux Résidences

Chaque requête concernant une résidence vérifie que l'utilisateur y a accès :

```python
def check_residence_access(residence_id):
    if current_user.is_superadmin():
        return True
    
    if current_user.is_admin():
        assignments = ResidenceAdmin.query.filter_by(
            user_id=current_user.id
        ).all()
        return residence_id in [a.residence_id for a in assignments]
    
    return current_user.residence_id == residence_id
```

---

## Protection des Données

### Filtrage par Utilisateur

Les requêtes sont toujours filtrées par les données de l'utilisateur connecté :

```python
# Correct : utilise current_user
maintenance = MaintenanceRequest(
    residence_id=current_user.residence_id,
    author_id=current_user.id
)

# Incorrect : vulnérable à la manipulation
maintenance = MaintenanceRequest(
    residence_id=request.json['residence_id'],  # Ne jamais faire
    author_id=request.json['user_id']           # Ne jamais faire
)
```

### Isolation des Données

Les résidents ne voient que :
- Leurs propres demandes de maintenance
- Les actualités de leur résidence
- Leurs propres paiements
- Les documents publics de leur résidence

Les admins ne voient que les données des résidences qui leur sont assignées.

### Types d'Actualités

Deux niveaux de visibilité :
- **Feed (fil d'actualité)** : Visible par tous les résidents
- **Announcement (annonces)** : Visible uniquement par propriétaires et admins

```python
if current_user.role == 'resident' and news_type == 'announcement':
    return jsonify({'error': 'Accès non autorisé'}), 403
```

---

## Protection contre les Attaques

### Injection SQL

L'utilisation de SQLAlchemy ORM prévient les injections SQL :

```python
# SQLAlchemy paramétrise automatiquement les requêtes
user = User.query.filter_by(email=email).first()

# Équivalent SQL sécurisé
# SELECT * FROM users WHERE email = $1
```

### Cross-Site Scripting (XSS)

- Les templates Jinja2 échappent automatiquement les variables
- Les données utilisateur sont assainies avant affichage

```jinja2
{{ user.name }}  <!-- Échappé automatiquement -->
{{ user.bio|safe }}  <!-- Non échappé - à éviter sauf si nécessaire -->
```

### Cross-Site Request Forgery (CSRF)

- Cookies SameSite=Lax
- Vérification de l'origine des requêtes
- Tokens de session liés à l'utilisateur

### Protection des Uploads

Les fichiers uploadés sont sécurisés :

```python
from werkzeug.utils import secure_filename

filename = secure_filename(file.filename)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
safe_filename = f"{timestamp}_{filename}"
```

Mesures :
- Validation du type MIME
- Limite de taille (16 Mo par défaut)
- Renommage avec horodatage
- Stockage hors de la racine web

---

## Configuration Sécurisée

### Variables d'Environnement

Les secrets sont stockés dans des variables d'environnement, jamais dans le code :

```python
SECRET_KEY = os.environ.get('SESSION_SECRET')
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### Mode Production

Différences entre développement et production :

| Paramètre | Développement | Production |
|-----------|---------------|------------|
| DEBUG | True | False |
| SESSION_COOKIE_SECURE | False | True |
| SQLALCHEMY_ECHO | True | False |

### En-têtes de Sécurité

En-têtes HTTP recommandés :

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

---

## Bonnes Pratiques

### Pour les Administrateurs

1. **Mots de passe forts**
   - Minimum 12 caractères
   - Mélange majuscules, minuscules, chiffres, symboles
   - Unique pour chaque compte

2. **Gestion des accès**
   - Créer des comptes individuels
   - Attribuer le rôle minimum nécessaire
   - Désactiver les comptes inutilisés

3. **Surveillance**
   - Consulter régulièrement les journaux
   - Vérifier les connexions inhabituelles
   - Auditer les modifications sensibles

4. **Sauvegardes**
   - Sauvegarder régulièrement la base de données
   - Tester les restaurations
   - Stocker les sauvegardes hors site

### Pour les Développeurs

1. **Ne jamais stocker de secrets dans le code**

```python
# Incorrect
SECRET_KEY = "ma-cle-secrete-en-dur"

# Correct
SECRET_KEY = os.environ.get('SESSION_SECRET')
```

2. **Toujours valider les entrées**

```python
def validate_email(email):
    from email_validator import validate_email, EmailNotValidError
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
```

3. **Utiliser les décorateurs d'autorisation**

```python
@admin_bp.route('/sensible')
@login_required
@superadmin_required
def route_sensible():
    pass
```

4. **Gérer les erreurs proprement**

```python
try:
    # Opération
    db.session.commit()
except Exception as e:
    db.session.rollback()
    # Logger l'erreur sans exposer les détails
    return jsonify({'error': 'Une erreur est survenue'}), 500
```

5. **Ne jamais exposer d'informations sensibles**

```python
# Incorrect - expose la stack trace
return jsonify({'error': str(e)}), 500

# Correct - message générique
logger.error(f'Erreur: {e}')
return jsonify({'error': 'Erreur interne'}), 500
```

### Pour les Utilisateurs

1. **Protéger son compte**
   - Choisir un mot de passe fort
   - Ne pas partager ses identifiants
   - Se déconnecter après utilisation

2. **Signaler les anomalies**
   - Connexions suspectes
   - Données incorrectes
   - Comportements inhabituels

3. **Vérifier les URLs**
   - S'assurer d'être sur le bon site
   - Vérifier la présence du cadenas HTTPS

---

## Conformité

### RGPD / Loi 09-08

L'application respecte les principes de protection des données :

**Minimisation**
- Collecte des données strictement nécessaires
- Pas de tracking tiers intégré par défaut

**Transparence**
- Les utilisateurs voient leurs données
- Historique des modifications conservé

**Sécurité**
- Chiffrement des mots de passe
- Sessions sécurisées
- Contrôle d'accès strict

**Droits des utilisateurs**
- Accès aux données personnelles
- Modification possible
- Possibilité de désactivation du compte

### Logs et Audit

L'application conserve les traces des opérations importantes :
- Connexions et déconnexions
- Modifications de données sensibles
- Opérations financières
- Actions administratives

---

## Incidents de Sécurité

### Procédure en Cas d'Incident

1. **Identification**
   - Détecter l'anomalie
   - Évaluer l'étendue

2. **Containment**
   - Isoler les systèmes affectés
   - Bloquer les accès suspects

3. **Éradication**
   - Corriger la vulnérabilité
   - Supprimer les accès non autorisés

4. **Récupération**
   - Restaurer les services
   - Vérifier l'intégrité des données

5. **Post-mortem**
   - Analyser les causes
   - Documenter l'incident
   - Améliorer les défenses

### Contacts

En cas d'incident de sécurité :
- Email : moa@myoneart.com
- Documenter l'incident avec date, heure et observations

---

## Amélirations Futures

### Prévues

- Rate limiting sur les endpoints d'authentification
- Authentification à deux facteurs (2FA)
- Journalisation centralisée
- Alertes automatiques

### Recommandées

- Audit de sécurité périodique
- Tests de pénétration
- Formation des utilisateurs
- Politique de mots de passe renforcée
