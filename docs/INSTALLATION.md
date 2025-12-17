# Guide d'Installation - Shabaka Syndic

Ce guide explique comment installer et configurer Shabaka Syndic sur différentes plateformes.

## Prérequis

### Logiciels Requis

| Logiciel | Version Minimum | Rôle |
|----------|-----------------|------|
| Python | 3.11+ | Langage backend |
| PostgreSQL | 12+ | Base de données |
| pip | Dernière | Gestionnaire de paquets Python |

### Ressources Système

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| RAM | 512 Mo | 2 Go |
| Stockage | 1 Go | 5 Go |
| CPU | 1 vCPU | 2 vCPU |

---

## Installation sur Replit

Replit est la plateforme recommandée pour un déploiement rapide.

### Étapes

1. **Créer un Repl**
   - Connectez-vous à Replit
   - Cliquez sur "Create Repl"
   - Choisissez "Import from GitHub" ou "Python"

2. **Importer le Code**
   - Clonez ou uploadez les fichiers du projet

3. **Configuration Automatique**
   - Replit détecte Python et installe les dépendances
   - La base de données PostgreSQL est provisionnée automatiquement

4. **Variables d'Environnement**
   - Allez dans l'onglet "Secrets"
   - Ajoutez `SESSION_SECRET` avec une valeur aléatoire

5. **Lancer l'Application**
   - Cliquez sur "Run"
   - L'application démarre sur le port 5000
   - L'URL publique apparaît dans le Webview

### Variables Automatiques

Sur Replit, ces variables sont définies automatiquement :

- `DATABASE_URL`
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`
- `REPLIT_DOMAINS`, `REPLIT_DEV_DOMAIN`

---

## Installation Locale

### 1. Cloner le Projet

```bash
git clone <url-du-repo>
cd shabaka-syndic
```

### 2. Créer un Environnement Virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer PostgreSQL

Créez une base de données PostgreSQL :

```sql
CREATE DATABASE shabaka_syndic;
CREATE USER shabaka_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE shabaka_syndic TO shabaka_user;
```

### 5. Configurer les Variables d'Environnement

Créez un fichier `.env` à la racine :

```bash
DATABASE_URL=postgresql://shabaka_user:votre_mot_de_passe@localhost:5432/shabaka_syndic
SESSION_SECRET=une-cle-secrete-aleatoire-de-32-caracteres
FLASK_ENV=development
```

Ou exportez directement :

```bash
export DATABASE_URL="postgresql://shabaka_user:votre_mot_de_passe@localhost:5432/shabaka_syndic"
export SESSION_SECRET="une-cle-secrete-aleatoire-de-32-caracteres"
export FLASK_ENV="development"
```

### 6. Initialiser la Base de Données

```bash
python init_db.py
```

Cette commande crée les tables et insère les données de démonstration.

### 7. Lancer l'Application

**Mode Développement :**

```bash
python main.py
```

**Mode Production :**

```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

### 8. Accéder à l'Application

Ouvrez votre navigateur : `http://localhost:5000`

---

## Installation sur VPS (Linux)

### 1. Préparer le Serveur

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer les dépendances
sudo apt install python3.11 python3.11-venv python3-pip postgresql nginx -y
```

### 2. Configurer PostgreSQL

```bash
# Accéder à PostgreSQL
sudo -u postgres psql

# Créer la base et l'utilisateur
CREATE DATABASE shabaka_syndic;
CREATE USER shabaka_user WITH PASSWORD 'mot_de_passe_securise';
GRANT ALL PRIVILEGES ON DATABASE shabaka_syndic TO shabaka_user;
\q
```

### 3. Déployer l'Application

```bash
# Créer un répertoire
sudo mkdir -p /var/www/shabaka-syndic
cd /var/www/shabaka-syndic

# Cloner le projet
sudo git clone <url-repo> .

# Créer l'environnement virtuel
python3.11 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configurer les Variables d'Environnement

Créez `/var/www/shabaka-syndic/.env` :

```bash
DATABASE_URL=postgresql://shabaka_user:mot_de_passe_securise@localhost:5432/shabaka_syndic
SESSION_SECRET=cle-secrete-de-production-longue-et-aleatoire
FLASK_ENV=production
```

### 5. Initialiser la Base

```bash
source venv/bin/activate
python init_db.py
```

### 6. Configurer Systemd

Créez `/etc/systemd/system/shabaka.service` :

```ini
[Unit]
Description=Shabaka Syndic Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/shabaka-syndic
Environment="PATH=/var/www/shabaka-syndic/venv/bin"
EnvironmentFile=/var/www/shabaka-syndic/.env
ExecStart=/var/www/shabaka-syndic/venv/bin/gunicorn --workers 4 --bind unix:shabaka.sock main:app

[Install]
WantedBy=multi-user.target
```

Activez le service :

```bash
sudo systemctl enable shabaka
sudo systemctl start shabaka
```

### 7. Configurer Nginx

Créez `/etc/nginx/sites-available/shabaka` :

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://unix:/var/www/shabaka-syndic/shabaka.sock;
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

Activez le site :

```bash
sudo ln -s /etc/nginx/sites-available/shabaka /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configurer SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d votre-domaine.com
```

---

## Configuration Avancée

### Variables d'Environnement Complètes

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| DATABASE_URL | URL PostgreSQL | Oui |
| SESSION_SECRET | Clé secrète Flask | Oui |
| FLASK_ENV | development / production | Non |
| PORT | Port du serveur (défaut: 5000) | Non |
| AGORA_APP_ID | ID Agora.io pour AG en ligne | Non |
| AGORA_APP_CERTIFICATE | Certificat Agora.io | Non |
| MAIL_SERVER | Serveur SMTP | Non |
| MAIL_PORT | Port SMTP (défaut: 587) | Non |
| MAIL_USE_TLS | Activer TLS (True/False) | Non |
| MAIL_USERNAME | Utilisateur SMTP | Non |
| MAIL_PASSWORD | Mot de passe SMTP | Non |

### Configuration Email

Pour activer les notifications par email :

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-application
MAIL_DEFAULT_SENDER=noreply@votre-domaine.com
```

Pour Gmail, utilisez un "mot de passe d'application" plutôt que votre mot de passe principal.

### Configuration Agora.io (AG en Ligne)

1. Créez un compte sur console.agora.io
2. Créez un projet et récupérez l'App ID
3. Activez le certificat et récupérez l'App Certificate
4. Configurez les variables :

```bash
AGORA_APP_ID=votre-app-id
AGORA_APP_CERTIFICATE=votre-app-certificate
```

---

## Vérification de l'Installation

### Test de Santé

Accédez à `/health` pour vérifier l'état :

```bash
curl http://localhost:5000/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "application": "Shabaka Syndic",
  "version": "0.1.0",
  "database": "connected"
}
```

### Connexion Test

1. Accédez à l'application
2. Connectez-vous avec : `admin@mysindic.ma` / `Admin123!`
3. Vérifiez l'accès au tableau de bord

---

## Mise à Jour

### Sur Replit

1. Faites un `git pull` ou mettez à jour les fichiers
2. Redémarrez le Repl

### Sur VPS

```bash
cd /var/www/shabaka-syndic
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
sudo systemctl restart shabaka
```

---

## Sauvegarde

### Base de Données

```bash
pg_dump -U shabaka_user -h localhost shabaka_syndic > backup_$(date +%Y%m%d).sql
```

### Restauration

```bash
psql -U shabaka_user -h localhost shabaka_syndic < backup_20250101.sql
```

---

## Résolution de Problèmes

### Erreur "relation does not exist"

La base de données n'est pas initialisée :

```bash
python init_db.py
```

### Erreur de connexion à la base de données

Vérifiez :
1. PostgreSQL est démarré
2. L'URL DATABASE_URL est correcte
3. L'utilisateur a les droits sur la base

### Erreur 500 Internal Server Error

Consultez les logs :

```bash
# Sur VPS
sudo journalctl -u shabaka -f

# En local
# Les erreurs s'affichent dans la console
```

### Page blanche ou erreur CORS

Vérifiez que Flask-CORS est installé et configuré :

```python
CORS(app)
```

### Mot de passe oublié

Réinitialisez via la base de données :

```python
from werkzeug.security import generate_password_hash

# Dans la console Python
hash = generate_password_hash('NouveauMotDePasse')
# Mettez à jour en SQL
UPDATE users SET password_hash = 'hash_obtenu' WHERE email = 'email@exemple.com';
```
