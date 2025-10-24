#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Application Flask Principale
Application web de gestion de copropriété

Date: 24 octobre 2025
Version: 0.1.0
"""

import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def create_app():
    """
    Factory pour créer et configurer l'application Flask
    
    Returns:
        Flask: Instance de l'application configurée
    """
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
    
    # Configuration CORS pour permettre les requêtes frontend
    CORS(app)
    
    # Routes de base
    @app.route('/')
    def index():
        """Page d'accueil"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """Endpoint de santé pour vérifier que l'API fonctionne"""
        return jsonify({
            'status': 'healthy',
            'application': 'MySindic',
            'version': '0.1.0'
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
                'residences': '/api/residences/*',
                'maintenance': '/api/maintenance/*'
            }
        })
    
    # Gestionnaire d'erreurs 404
    @app.errorhandler(404)
    def not_found(error):
        """Gestion des erreurs 404"""
        return jsonify({
            'error': 'Page non trouvée',
            'status': 404
        }), 404
    
    # Gestionnaire d'erreurs 500
    @app.errorhandler(500)
    def internal_error(error):
        """Gestion des erreurs 500"""
        return jsonify({
            'error': 'Erreur interne du serveur',
            'status': 500
        }), 500
    
    return app

# Créer l'application
app = create_app()

if __name__ == '__main__':
    # Port pour Replit (obligatoire: 5000)
    # Pour VPS, utiliser le script deploy_vps.sh qui démarre sur port 5006
    port = int(os.getenv('PORT', 5000))
    
    # Bind sur 0.0.0.0 pour être accessible depuis l'extérieur
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
