#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Routes Superadmin
Routes pour les fonctionnalités superadmin

Date: 24 octobre 2025
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from backend.models import db
from backend.models.residence import Residence, Unit
from backend.models.user import User

# Créer le blueprint
admin_bp = Blueprint('admin', __name__)


def superadmin_required(f):
    """
    Décorateur pour vérifier que l'utilisateur est un superadmin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'error': 'Authentification requise'
            }), 401
        
        if not current_user.is_superadmin():
            return jsonify({
                'success': False,
                'error': 'Accès réservé aux superadmins'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@superadmin_required
def dashboard():
    """
    Tableau de bord du superadmin
    """
    try:
        # Statistiques générales
        total_residences = Residence.query.count()
        total_users = User.query.count()
        total_units = Unit.query.count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_residences': total_residences,
                'total_users': total_users,
                'total_units': total_units
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@admin_bp.route('/residences', methods=['GET'])
@login_required
@superadmin_required
def get_residences():
    """
    Récupère la liste des résidences
    """
    try:
        residences = Residence.query.all()
        return jsonify({
            'success': True,
            'residences': [r.to_dict() for r in residences]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@admin_bp.route('/residences', methods=['POST'])
@login_required
@superadmin_required
def create_residence():
    """
    Crée une nouvelle résidence
    
    JSON attendu:
    {
        "name": "Résidence Al Andalous",
        "address": "Avenue Mohammed V",
        "city": "Casablanca",
        "postal_code": "20000",
        "total_units": 45,
        "description": "Description...",
        "syndic_name": "Nom du syndic",
        "syndic_email": "syndic@example.com",
        "syndic_phone": "+212..."
    }
    """
    try:
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['name', 'address', 'city', 'total_units']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Le champ {field} est requis'
                }), 400
        
        # Créer la résidence
        residence = Residence(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            postal_code=data.get('postal_code'),
            total_units=data['total_units'],
            description=data.get('description'),
            syndic_name=data.get('syndic_name'),
            syndic_email=data.get('syndic_email'),
            syndic_phone=data.get('syndic_phone')
        )
        
        db.session.add(residence)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Résidence créée avec succès',
            'residence': residence.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@admin_bp.route('/users', methods=['GET'])
@login_required
@superadmin_required
def get_users():
    """
    Récupère la liste des utilisateurs
    """
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [u.to_dict() for u in users]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500
