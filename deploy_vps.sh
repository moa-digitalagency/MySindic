#!/bin/bash

###############################################################################
# MySindic - Script de Déploiement VPS Automatisé
# Version: 1.0
# Date: 24 octobre 2025
#
# Ce script automatise le déploiement de MySindic sur un VPS
###############################################################################

set -e  # Arrêt en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="$HOME/MySindic"
VENV_DIR="$APP_DIR/venv"
ENV_FILE="$APP_DIR/.env"
PORT=5006
APP_NAME="mysindic"

# Fonction d'affichage des messages
print_step() {
    echo -e "${BLUE}==>${NC} ${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCÈS]${NC} $1"
}

###############################################################################
# ÉTAPE 1: Pull du code depuis Git
###############################################################################
print_step "Étape 1/7: Mise à jour du code depuis Git"

if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
    print_step "Répertoire trouvé, pull des dernières modifications..."
    git pull origin main || {
        print_error "Échec du git pull"
        exit 1
    }
else
    print_error "Le répertoire $APP_DIR n'existe pas"
    print_warning "Veuillez cloner le repository d'abord avec:"
    echo "    git clone <repository-url> $APP_DIR"
    exit 1
fi

print_success "Code mis à jour avec succès"

###############################################################################
# ÉTAPE 2: Vérification/Création de l'environnement virtuel
###############################################################################
print_step "Étape 2/7: Gestion de l'environnement virtuel Python"

if [ -d "$VENV_DIR" ]; then
    print_step "Environnement virtuel existant trouvé"
else
    print_step "Création d'un nouvel environnement virtuel..."
    python3 -m venv "$VENV_DIR" || {
        print_error "Échec de la création de l'environnement virtuel"
        exit 1
    }
    print_success "Environnement virtuel créé"
fi

###############################################################################
# ÉTAPE 3: Activation de l'environnement virtuel
###############################################################################
print_step "Étape 3/7: Activation de l'environnement virtuel"

source "$VENV_DIR/bin/activate" || {
    print_error "Échec de l'activation de l'environnement virtuel"
    exit 1
}

print_success "Environnement virtuel activé"

###############################################################################
# ÉTAPE 4: Gestion du fichier .env
###############################################################################
print_step "Étape 4/7: Vérification du fichier .env"

if [ ! -f "$ENV_FILE" ]; then
    print_warning "Fichier .env non trouvé"
    
    # Créer un fichier .env de base
    print_step "Création d'un fichier .env par défaut..."
    cat > "$ENV_FILE" << 'EOF'
# Configuration Flask
FLASK_APP=backend/app.py
FLASK_ENV=production
SECRET_KEY=changez_cette_cle_secrete_en_production

# Base de données PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/mysindic

# Configuration Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_password

# Configuration VPS
VPS_PORT=5006

# Mode Debug (mettre à False en production)
DEBUG=False
EOF
    
    print_success "Fichier .env créé"
    print_warning "ATTENTION: Veuillez éditer $ENV_FILE et configurer vos valeurs réelles"
    print_warning "Notamment: SECRET_KEY, DATABASE_URL, et les paramètres email"
else
    print_success "Fichier .env trouvé"
fi

###############################################################################
# ÉTAPE 5: Installation des dépendances
###############################################################################
print_step "Étape 5/7: Installation des dépendances Python"

if [ -f "$APP_DIR/backend/requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r "$APP_DIR/backend/requirements.txt" || {
        print_error "Échec de l'installation des dépendances"
        exit 1
    }
    print_success "Dépendances installées avec succès"
else
    print_error "Fichier requirements.txt non trouvé dans backend/"
    exit 1
fi

###############################################################################
# ÉTAPE 6: Migrations de la base de données
###############################################################################
print_step "Étape 6/7: Migrations de la base de données"

cd "$APP_DIR"

# Vérifier si les migrations existent
if [ -d "$APP_DIR/migrations" ]; then
    print_step "Application des migrations..."
    flask db upgrade || {
        print_warning "Échec des migrations (peut-être la première fois?)"
    }
else
    print_step "Initialisation des migrations..."
    flask db init || print_warning "Migrations déjà initialisées ou erreur"
    flask db migrate -m "Initial migration" || print_warning "Erreur de migration"
    flask db upgrade || print_warning "Erreur d'upgrade"
fi

print_success "Migrations terminées"

###############################################################################
# ÉTAPE 7: Démarrage de l'application
###############################################################################
print_step "Étape 7/7: Démarrage de l'application MySindic"

# Arrêter l'ancienne instance si elle existe
print_step "Recherche d'instances existantes..."
pkill -f "python.*app.py" || print_step "Aucune instance en cours"

# Créer le répertoire de logs s'il n'existe pas
mkdir -p "$APP_DIR/logs"

# Démarrer l'application en arrière-plan
print_step "Démarrage de MySindic sur le port $PORT..."

cd "$APP_DIR"
nohup python backend/app.py > logs/app.log 2>&1 &

# Attendre que l'application démarre
sleep 3

# Vérifier si l'application est en cours d'exécution
if pgrep -f "python.*app.py" > /dev/null; then
    print_success "MySindic démarré avec succès!"
    print_success "Application accessible sur le port $PORT"
    print_step "Logs disponibles dans: $APP_DIR/logs/app.log"
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  MySindic est maintenant en ligne!              ║${NC}"
    echo -e "${GREEN}║  Port: $PORT                                      ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    print_step "Pour voir les logs en temps réel:"
    echo "    tail -f $APP_DIR/logs/app.log"
    echo ""
    print_step "Pour arrêter l'application:"
    echo "    pkill -f 'python.*app.py'"
else
    print_error "Échec du démarrage de l'application"
    print_step "Consultez les logs pour plus d'informations:"
    echo "    tail -50 $APP_DIR/logs/app.log"
    exit 1
fi

###############################################################################
# FIN DU SCRIPT
###############################################################################
