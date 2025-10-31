#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from backend.models import db
from backend.models.user import User
from datetime import datetime

# Créer le blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Inscription d'un nouvel utilisateur
    
    JSON attendu:
    {
        "email": "user@example.com",
        "password": "motdepasse",
        "first_name": "Prénom",
        "last_name": "Nom",
        "phone": "+212XXXXXXXXX",
        "role": "resident" (optionnel, par défaut)
    }
    """
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Le champ {field} est requis'
                }), 400
        
        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Cet email est déjà utilisé'
            }), 400
        
        # Créer le nouvel utilisateur
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            role=data.get('role', 'resident')
        )
        user.set_password(data['password'])
        
        # Sauvegarder en base de données
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Compte créé avec succès',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erreur lors de l\'inscription: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Connexion d'un utilisateur
    
    JSON attendu:
    {
        "email": "user@example.com",
        "password": "motdepasse",
        "remember": true (optionnel)
    }
    """
    try:
        data = request.get_json()
        
        # Validation des champs
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Email et mot de passe requis'
            }), 400
        
        # Rechercher l'utilisateur
        user = User.query.filter_by(email=data['email']).first()
        
        # Vérifier les identifiants
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }), 401
        
        # Vérifier si le compte est actif
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Ce compte est désactivé'
            }), 403
        
        # Connecter l'utilisateur
        remember = data.get('remember', False)
        login_user(user, remember=remember)
        
        # Mettre à jour la date de dernière connexion
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Connexion réussie',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la connexion: {str(e)}'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Déconnexion de l'utilisateur
    """
    try:
        logout_user()
        return jsonify({
            'success': True,
            'message': 'Déconnexion réussie'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la déconnexion: {str(e)}'
        }), 500


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Récupère les informations de l'utilisateur connecté
    """
    try:
        return jsonify({
            'success': True,
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """
    Vérifie si l'utilisateur est connecté
    """
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'user': current_user.to_dict() if current_user.is_authenticated else None
    }), 200
