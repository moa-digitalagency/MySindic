#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Décorateurs de sécurité réutilisables

Contient tous les décorateurs pour contrôler l'accès par rôle et résidence.
"""

from functools import wraps
from flask import jsonify, abort
from flask_login import current_user
from backend.models.residence_admin import ResidenceAdmin


def superadmin_required(f):
    """Décorateur pour vérifier que l'utilisateur est un superadmin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentification requise'}), 401
        if not current_user.is_superadmin():
            return jsonify({'success': False, 'error': 'Accès réservé aux superadmins'}), 403
        return f(*args, **kwargs)
    return decorated_function


def admin_or_superadmin_required(f):
    """Décorateur pour vérifier que l'utilisateur est un admin ou un superadmin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentification requise'}), 401
        if not (current_user.is_admin() or current_user.is_superadmin()):
            return jsonify({'success': False, 'error': 'Accès réservé aux administrateurs'}), 403
        return f(*args, **kwargs)
    return decorated_function


def owner_or_above_required(f):
    """
    Décorateur pour vérifier que l'utilisateur est propriétaire, admin ou superadmin
    Bloque les résidents simples (role='resident')
    
    Supporte à la fois les routes HTML et API:
    - Routes API (/api/*): Retourne JSON avec code HTTP
    - Routes HTML: Utilise abort() pour redirection vers page d'erreur
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        
        if not current_user.is_authenticated:
            # Détecter si c'est une route API
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Authentification requise'}), 401
            else:
                abort(401)  # HTML route
        
        if current_user.role not in ['owner', 'admin', 'superadmin']:
            # Détecter si c'est une route API
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'error': 'Accès réservé aux propriétaires et administrateurs'}), 403
            else:
                abort(403)  # HTML route - Accès interdit
        
        return f(*args, **kwargs)
    return decorated_function


def get_user_residence_ids():
    """
    Récupère les IDs des résidences auxquelles l'utilisateur a accès
    
    Returns:
        list: Liste des IDs de résidence ou None si accès à toutes les résidences (superadmin)
    """
    if current_user.is_superadmin():
        return None  # None signifie accès à toutes les résidences
    elif current_user.is_admin():
        # Admin voit seulement les résidences assignées
        assignments = ResidenceAdmin.query.filter_by(user_id=current_user.id).all()
        return [a.residence_id for a in assignments]
    elif current_user.is_owner() or current_user.is_resident():
        # Propriétaire et résident voient seulement leur résidence
        if current_user.residence_id:
            return [current_user.residence_id]
        return []
    return []


def check_residence_access(residence_id):
    """
    Vérifie si l'utilisateur a accès à une résidence spécifique
    
    Args:
        residence_id: ID de la résidence à vérifier
        
    Returns:
        bool: True si l'utilisateur a accès, False sinon
    """
    allowed_residence_ids = get_user_residence_ids()
    
    # Superadmin a accès à tout
    if allowed_residence_ids is None:
        return True
    
    # Vérifier si la résidence est dans la liste autorisée
    return residence_id in allowed_residence_ids


def residence_access_required(f):
    """
    Décorateur pour vérifier l'accès à une résidence spécifique
    Utilise le paramètre residence_id de la route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        residence_id = kwargs.get('residence_id')
        
        if residence_id is None:
            return jsonify({'success': False, 'error': 'ID de résidence manquant'}), 400
        
        if not check_residence_access(residence_id):
            return jsonify({'success': False, 'error': 'Accès non autorisé à cette résidence'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
