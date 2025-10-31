#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import os
from datetime import timedelta

class Config:
    """Configuration de base pour tous les environnements"""
    
    # Clé secrète pour les sessions et JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mysindic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Configuration JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configuration Flask-Login
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@mysindic.ma')
    
    # Configuration de l'application
    APP_NAME = 'Shabaka Syndic'
    APP_VERSION = '0.1.0'
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Upload de fichiers
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}


class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement"""
    
    DEBUG = True
    TESTING = False
    
    # Désactiver HTTPS en développement
    SESSION_COOKIE_SECURE = False
    
    # Activer les logs SQL
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configuration pour l'environnement de production"""
    
    DEBUG = False
    TESTING = False
    
    # Note: Les validations sont effectuées dans get_config()
    # pour éviter les erreurs lors de l'import du module


class TestingConfig(Config):
    """Configuration pour les tests"""
    
    DEBUG = False
    TESTING = True
    
    # Base de données de test en mémoire
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Désactiver la protection CSRF pour les tests
    WTF_CSRF_ENABLED = False


# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """
    Récupère la configuration appropriée selon l'environnement
    
    Returns:
        Config: Instance de configuration
    """
    env = os.getenv('FLASK_ENV', 'development')
    
    # Validation pour la production
    if env == 'production':
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY doit être définie en production!")
        if not os.getenv('DATABASE_URL'):
            raise ValueError("DATABASE_URL doit être définie en production!")
    
    return config.get(env, config['default'])
