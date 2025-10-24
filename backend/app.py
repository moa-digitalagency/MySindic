#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Application Flask Principale
Application web de gestion de copropriété

Date: 24 octobre 2025
Version: 0.1.0
"""

import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Imports locaux
from backend.config import get_config
from backend.models import db, migrate, init_db

# Initialiser Flask-Login
login_manager = LoginManager()


def create_app():
    """
    Factory pour créer et configurer l'application Flask
    
    Returns:
        Flask: Instance de l'application configurée
    """
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Charger la configuration
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Configuration CORS pour permettre les requêtes frontend
    CORS(app)
    
    # Initialiser la base de données
    init_db(app)
    
    # Initialiser Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Charge un utilisateur par son ID"""
        from backend.models.user import User
        return User.query.get(int(user_id))
    
    # Enregistrer les blueprints (routes)
    register_blueprints(app)
    
    # Routes de base
    @app.route('/')
    def index():
        """Page d'accueil"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """Endpoint de santé pour vérifier que l'API fonctionne"""
        db_status = 'connected'
        try:
            # Test de connexion à la base de données
            db.session.execute(db.text('SELECT 1'))
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return jsonify({
            'status': 'healthy',
            'application': 'MySindic',
            'version': '0.1.0',
            'database': db_status
        })
    
    @app.route('/api/info')
    def api_info():
        """Informations sur l'API"""
        return jsonify({
            'name': 'MySindic API',
            'version': '0.1.0',
            'description': 'API de gestion de copropriété',
            'endpoints': {
                'health': '/health',
                'info': '/api/info',
                'auth': '/api/auth/*',
                'admin': '/api/admin/*',
                'resident': '/api/resident/*'
            }
        })
    
    # Gestionnaires d'erreurs
    @app.errorhandler(404)
    def not_found(error):
        """Gestion des erreurs 404"""
        return jsonify({
            'error': 'Page non trouvée',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Gestion des erreurs 500"""
        db.session.rollback()
        return jsonify({
            'error': 'Erreur interne du serveur',
            'status': 500
        }), 500
    
    return app


def register_blueprints(app):
    """
    Enregistre tous les blueprints de l'application
    
    Args:
        app: Instance de l'application Flask
    """
    # Import des blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.admin import admin_bp
    from backend.routes.resident import resident_bp
    
    # Enregistrement des blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(resident_bp, url_prefix='/api/resident')


# Créer l'application
app = create_app()

if __name__ == '__main__':
    # Port pour Replit (obligatoire: 5000)
    # Pour VPS, utiliser le script deploy_vps.sh qui démarre sur port 5006
    port = int(os.getenv('PORT', 5000))
    
    # Créer les tables si elles n'existent pas (en développement uniquement)
    with app.app_context():
        if os.getenv('FLASK_ENV') == 'development':
            try:
                db.create_all()
                print("✅ Tables de base de données créées")
            except Exception as e:
                print(f"⚠️ Erreur lors de la création des tables: {e}")
    
    # Bind sur 0.0.0.0 pour être accessible depuis l'extérieur
    print(f"🚀 Démarrage de MySindic sur le port {port}...")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
