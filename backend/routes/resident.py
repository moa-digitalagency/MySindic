#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Routes Résidents
Routes pour les fonctionnalités résidents

Date: 24 octobre 2025
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.models import db
from backend.models.maintenance import MaintenanceRequest
from backend.models.news import News

# Créer le blueprint
resident_bp = Blueprint('resident', __name__)


@resident_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Tableau de bord du résident
    """
    try:
        # Récupérer les demandes de maintenance du résident
        maintenance_requests = MaintenanceRequest.query.filter_by(
            requester_id=current_user.id
        ).order_by(MaintenanceRequest.created_at.desc()).limit(5).all()
        
        # Récupérer les actualités de la résidence
        news = []
        if current_user.residence_id:
            news = News.query.filter_by(
                residence_id=current_user.residence_id,
                is_published=True
            ).order_by(News.published_at.desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'maintenance_requests': [m.to_dict() for m in maintenance_requests],
            'news': [n.to_dict() for n in news]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@resident_bp.route('/maintenance', methods=['POST'])
@login_required
def create_maintenance_request():
    """
    Crée une nouvelle demande de maintenance
    
    JSON attendu:
    {
        "title": "Fuite d'eau",
        "description": "Description détaillée...",
        "category": "Plomberie",
        "location": "Appartement A101",
        "priority": "high"
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Le champ {field} est requis'
                }), 400
        
        # Vérifier que l'utilisateur a une résidence
        if not current_user.residence_id:
            return jsonify({
                'success': False,
                'error': 'Vous devez être associé à une résidence'
            }), 400
        
        # Créer la demande
        maintenance_request = MaintenanceRequest(
            residence_id=current_user.residence_id,
            requester_id=current_user.id,
            title=data['title'],
            description=data['description'],
            category=data.get('category'),
            location=data.get('location'),
            priority=data.get('priority', 'normal')
        )
        
        db.session.add(maintenance_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Demande créée avec succès',
            'maintenance_request': maintenance_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@resident_bp.route('/maintenance', methods=['GET'])
@login_required
def get_maintenance_requests():
    """
    Récupère les demandes de maintenance du résident
    """
    try:
        requests = MaintenanceRequest.query.filter_by(
            requester_id=current_user.id
        ).order_by(MaintenanceRequest.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'maintenance_requests': [r.to_dict() for r in requests]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500


@resident_bp.route('/news', methods=['GET'])
@login_required
def get_news():
    """
    Récupère les actualités de la résidence
    """
    try:
        if not current_user.residence_id:
            return jsonify({
                'success': True,
                'news': []
            }), 200
        
        news = News.query.filter_by(
            residence_id=current_user.residence_id,
            is_published=True
        ).order_by(News.is_pinned.desc(), News.published_at.desc()).all()
        
        return jsonify({
            'success': True,
            'news': [n.to_dict() for n in news]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur: {str(e)}'
        }), 500
