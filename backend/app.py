#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com

Application principale Flask avec configuration des routes et middlewares.
"""

import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, redirect, url_for, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user
from functools import wraps
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
    # Chemins relatifs vers le dossier frontend
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    
    app = Flask(__name__, 
                static_folder=os.path.join(frontend_dir, 'static'),
                template_folder=os.path.join(frontend_dir, 'templates'))
    
    # Charger la configuration
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Configuration CORS pour permettre les requêtes frontend
    CORS(app)
    
    # Initialiser la base de données
    init_db(app)
    
    # Initialiser Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'login_page'  # type: ignore
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Charge un utilisateur par son ID"""
        from backend.models.user import User
        return User.query.get(int(user_id))
    
    @app.context_processor
    def inject_custom_head():
        """Injecte le code <head> personnalisé dans tous les templates"""
        from backend.models.app_settings import AppSettings
        custom_head_code = AppSettings.get_value('custom_head_code', '')
        return dict(custom_head_code=custom_head_code)
    
    # Enregistrer les blueprints (routes)
    register_blueprints(app)
    
    # Décorateur pour vérifier que l'utilisateur est superadmin
    def superadmin_required(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_superadmin():
                return redirect(url_for('resident_dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    
    # Routes de base
    @app.route('/')
    def index():
        """Page d'accueil"""
        if current_user.is_authenticated:
            if current_user.is_superadmin():
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('resident_dashboard'))
        return render_template('index.html')
    
    @app.route('/login')
    def login_page():
        """Page de connexion"""
        if current_user.is_authenticated:
            if current_user.is_superadmin():
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('resident_dashboard'))
        return render_template('auth/login.html')
    
    @app.route('/register')
    def register_page():
        """Page d'inscription"""
        if current_user.is_authenticated:
            if current_user.is_superadmin():
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('resident_dashboard'))
        return render_template('auth/register.html')
    
    # Routes Admin (pages HTML)
    @app.route('/admin/dashboard')
    @superadmin_required
    def admin_dashboard():
        """Dashboard administrateur"""
        return render_template('admin/dashboard.html')
    
    @app.route('/admin/residences')
    @superadmin_required
    def admin_residences():
        """Gestion des résidences"""
        return render_template('admin/residences.html')
    
    @app.route('/admin/residences/new')
    @superadmin_required
    def admin_residence_wizard():
        """Assistant de création de résidence"""
        response = make_response(render_template('admin/residence_wizard.html'))
        # Désactiver le cache pour forcer le rechargement
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    @app.route('/admin/finances')
    @superadmin_required
    def admin_finances():
        """Gestion financière"""
        return render_template('admin/finances.html')
    
    @app.route('/admin/maintenance')
    @superadmin_required
    def admin_maintenance():
        """Gestion de la maintenance"""
        return render_template('admin/maintenance.html')
    
    @app.route('/admin/users')
    @superadmin_required
    def admin_users():
        """Gestion des utilisateurs"""
        return render_template('admin/users.html')
    
    @app.route('/admin/maintenance-log')
    @superadmin_required
    def admin_maintenance_log():
        """Carnet d'entretien"""
        return render_template('admin/maintenance_log.html')
    
    @app.route('/admin/assemblies')
    @superadmin_required
    def admin_assemblies():
        """Gestion des assemblées générales"""
        return render_template('admin/assemblies.html')
    
    @app.route('/admin/documents')
    @superadmin_required
    def admin_documents():
        """Gestion des documents"""
        return render_template('admin/documents.html')
    
    @app.route('/admin/news')
    @superadmin_required
    def admin_news():
        """Gestion des actualités"""
        return render_template('admin/news.html')
    
    @app.route('/admin/settings')
    @superadmin_required
    def admin_settings():
        """Paramètres de l'application"""
        return render_template('admin/settings.html')
    
    @app.route('/admin/settings/roles')
    @superadmin_required
    def admin_settings_roles():
        """Gestion des rôles et permissions"""
        return render_template('admin/settings_roles.html')
    
    @app.route('/admin/settings/notifications')
    @superadmin_required
    def admin_settings_notifications():
        """Paramètres de notifications"""
        return render_template('admin/settings_notifications.html')
    
    @app.route('/admin/settings/appearance')
    @superadmin_required
    def admin_settings_appearance():
        """Paramètres d'apparence"""
        return render_template('admin/settings_appearance.html')
    
    @app.route('/admin/settings/security')
    @superadmin_required
    def admin_settings_security():
        """Paramètres de sécurité"""
        return render_template('admin/settings_security.html')
    
    @app.route('/admin/settings/custom-code')
    @superadmin_required
    def admin_settings_custom_code():
        """Paramètres de code personnalisé"""
        return render_template('admin/settings_custom_code.html')
    
    # Routes Résidents (pages HTML)
    @app.route('/resident/dashboard')
    @login_required
    def resident_dashboard():
        """Dashboard résident"""
        if current_user.is_superadmin():
            return redirect(url_for('admin_dashboard'))
        return render_template('resident/dashboard.html')
    
    @app.route('/resident/maintenance')
    @login_required
    def resident_maintenance():
        """Demandes de maintenance"""
        return render_template('resident/maintenance.html')
    
    @app.route('/resident/finances')
    @login_required
    def resident_finances():
        """Mes finances"""
        return render_template('resident/finances.html')
    
    @app.route('/resident/news')
    @login_required
    def resident_news():
        """Actualités"""
        return render_template('resident/news.html')
    
    @app.route('/resident/assemblies')
    @login_required
    def resident_assemblies():
        """Consultation des assemblées générales"""
        return render_template('resident/assemblies.html')
    
    @app.route('/resident/documents')
    @login_required
    def resident_documents():
        """Accès aux documents"""
        return render_template('resident/documents.html')
    
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


def auto_init_database():
    """
    Initialise automatiquement la base de données au démarrage si nécessaire
    """
    with app.app_context():
        try:
            # Vérifier si la base de données est déjà initialisée
            from backend.models.user import User
            existing_admin = User.query.filter_by(role='superadmin').first()
            
            if not existing_admin:
                print("📦 Base de données vide détectée. Initialisation automatique...")
                from backend.init_demo_data import init_demo_data
                init_demo_data(app, db)
            else:
                print(f"✅ Base de données déjà initialisée (Admin: {existing_admin.email})")
        except Exception as e:
            # Si les tables n'existent pas, les créer et initialiser
            print(f"⚠️  Erreur détectée: {str(e)}")
            print("📋 Création des tables et initialisation des données...")
            try:
                from backend.init_demo_data import init_demo_data
                init_demo_data(app, db)
            except Exception as init_error:
                print(f"❌ Erreur lors de l'initialisation: {str(init_error)}")


# Initialiser automatiquement la base de données au démarrage
auto_init_database()


if __name__ == '__main__':
    # Port pour Replit (obligatoire: 5000)
    # Pour VPS, utiliser le script deploy_vps.sh qui démarre sur port 5006
    port = int(os.getenv('PORT', 5000))
    
    # Bind sur 0.0.0.0 pour être accessible depuis l'extérieur
    print(f"🚀 Démarrage de MySindic sur le port {port}...")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
