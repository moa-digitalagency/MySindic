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
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from decimal import Decimal

from backend.models import db
from backend.models.residence import Residence, Unit
from backend.models.residence_admin import ResidenceAdmin
from backend.models.user import User
from backend.models.charge import Charge, ChargeDistribution
from backend.models.payment import Payment
from backend.models.maintenance import MaintenanceRequest
from backend.models.news import News
from backend.models.poll import Poll, PollOption, PollVote
from backend.models.document import Document
from backend.models.general_assembly import GeneralAssembly, Resolution, Vote, Attendance
from backend.models.litigation import Litigation
from backend.models.maintenance_log import MaintenanceLog
from backend.models.app_settings import AppSettings
from backend.services.charge_calculator import ChargeCalculator
from backend.services.notification_service import NotificationService
from backend.services.agora_service import AgoraService

# Créer le blueprint
admin_bp = Blueprint('admin', __name__)


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


# ==================== DASHBOARD ====================

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@superadmin_required
def dashboard():
    """Tableau de bord du superadmin avec statistiques complètes"""
    try:
        total_residences = Residence.query.count()
        total_users = User.query.count()
        total_units = Unit.query.count()
        total_charges = Charge.query.filter_by(status='published').count()
        total_maintenance = MaintenanceRequest.query.count()
        pending_maintenance = MaintenanceRequest.query.filter_by(status='pending').count()
        
        # Statistiques financières
        unpaid_distributions = ChargeDistribution.query.filter_by(is_paid=False).all()
        total_unpaid = sum(float(d.amount) for d in unpaid_distributions)
        
        return jsonify({
            'success': True,
            'stats': {
                'total_residences': total_residences,
                'total_users': total_users,
                'total_units': total_units,
                'total_charges': total_charges,
                'total_maintenance': total_maintenance,
                'pending_maintenance': pending_maintenance,
                'total_unpaid': total_unpaid
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== RÉSIDENCES ====================

@admin_bp.route('/residences', methods=['GET'])
@login_required
@superadmin_required
def get_residences():
    """Récupère la liste des résidences"""
    try:
        residences = Residence.query.all()
        return jsonify({'success': True, 'residences': [r.to_dict() for r in residences]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/residences', methods=['POST'])
@login_required
@superadmin_required
def create_residence():
    """Crée une nouvelle résidence avec ses unités (format wizard ou simple)"""
    try:
        data = request.get_json()
        
        # Support pour 2 formats: wizard complet ou création simple
        if 'residence' in data and 'units' in data:
            # Format wizard: { residence: {...}, units: [...], divisions: [...], admins: [...] }
            residence_data = data['residence']
            units_data = data.get('units', [])
            
            # Validation
            required_fields = ['name', 'address', 'city']
            for field in required_fields:
                if field not in residence_data:
                    return jsonify({'success': False, 'message': f'Le champ {field} est requis'}), 400
            
            # Créer la résidence
            residence = Residence(
                name=residence_data['name'],
                address=residence_data['address'],
                city=residence_data['city'],
                postal_code=residence_data.get('postal_code'),
                total_units=len(units_data),
                description=residence_data.get('description'),
                syndic_name=residence_data.get('syndic_name'),
                syndic_email=residence_data.get('syndic_email'),
                syndic_phone=residence_data.get('syndic_phone')
            )
            
            db.session.add(residence)
            db.session.flush()  # Pour obtenir l'ID de la résidence
            
            # Créer les unités
            created_units = []
            for unit_data in units_data:
                unit = Unit(
                    residence_id=residence.id,
                    unit_number=unit_data['unit_number'],
                    floor=unit_data.get('floor'),
                    building=unit_data.get('division'),  # Stocker la division/bâtiment
                    unit_type=unit_data.get('unit_type', 'appartement')
                )
                db.session.add(unit)
                created_units.append(unit)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Résidence créée avec succès avec {len(created_units)} unité(s)',
                'residence': residence.to_dict()
            }), 201
            
        else:
            # Format simple: création directe
            required_fields = ['name', 'address', 'city', 'total_units']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
            
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
            
            return jsonify({'success': True, 'message': 'Résidence créée avec succès', 'residence': residence.to_dict()}), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/residences/<int:residence_id>', methods=['PUT'])
@login_required
@superadmin_required
def update_residence(residence_id):
    """Met à jour une résidence"""
    try:
        residence = Residence.query.get(residence_id)
        if not residence:
            return jsonify({'success': False, 'error': 'Résidence non trouvée'}), 404
        
        data = request.get_json()
        for field in ['name', 'address', 'city', 'postal_code', 'description', 'syndic_name', 'syndic_email', 'syndic_phone']:
            if field in data:
                setattr(residence, field, data[field])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Résidence mise à jour', 'residence': residence.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== UNITÉS/LOTS ====================

@admin_bp.route('/residences/<int:residence_id>/units', methods=['GET'])
@login_required
@superadmin_required
def get_units(residence_id):
    """Récupère les lots d'une résidence"""
    try:
        units = Unit.query.filter_by(residence_id=residence_id).all()
        return jsonify({'success': True, 'units': [u.to_dict() for u in units]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/residences/<int:residence_id>/units', methods=['POST'])
@login_required
@superadmin_required
def create_unit(residence_id):
    """Crée un nouveau lot"""
    try:
        data = request.get_json()
        required_fields = ['unit_number']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        unit = Unit(
            residence_id=residence_id,
            unit_number=data['unit_number'],
            floor=data.get('floor'),
            building=data.get('building'),
            unit_type=data.get('unit_type'),
            surface_area=data.get('surface_area'),
            owner_name=data.get('owner_name'),
            owner_email=data.get('owner_email'),
            owner_phone=data.get('owner_phone'),
            is_occupied=data.get('is_occupied', True)
        )
        
        db.session.add(unit)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lot créé avec succès', 'unit': unit.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/units', methods=['POST'])
@login_required
@superadmin_required
def create_unit_simple():
    """Crée un nouveau lot (endpoint simplifié)"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'unit_number']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        unit = Unit(
            residence_id=data['residence_id'],
            unit_number=data['unit_number'],
            floor=data.get('floor'),
            building=data.get('building'),
            unit_type=data.get('unit_type'),
            surface_area=data.get('surface_area'),
            owner_name=data.get('owner_name'),
            owner_email=data.get('owner_email'),
            owner_phone=data.get('owner_phone'),
            is_occupied=data.get('is_occupied', True)
        )
        
        db.session.add(unit)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Lot créé avec succès', 'unit': unit.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CHARGES ====================

@admin_bp.route('/charges', methods=['GET'])
@login_required
@superadmin_required
def get_charges():
    """Récupère toutes les charges"""
    try:
        residence_id = request.args.get('residence_id')
        query = Charge.query
        if residence_id:
            query = query.filter_by(residence_id=int(residence_id))
        charges = query.order_by(Charge.created_at.desc()).all()
        return jsonify({'success': True, 'charges': [c.to_dict() for c in charges]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/charges', methods=['POST'])
@login_required
@superadmin_required
def create_charge():
    """Crée un nouvel appel de fonds"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'title', 'charge_type', 'total_amount', 'period_year']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        charge = Charge(
            residence_id=data['residence_id'],
            title=data['title'],
            description=data.get('description'),
            charge_type=data['charge_type'],
            total_amount=Decimal(str(data['total_amount'])),
            period_month=data.get('period_month'),
            period_year=data['period_year'],
            status='draft',
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        )
        
        db.session.add(charge)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Charge créée', 'charge': charge.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/charges/<int:charge_id>/publish', methods=['POST'])
@login_required
@superadmin_required
def publish_charge(charge_id):
    """Publie une charge et calcule la répartition"""
    try:
        charge = Charge.query.get(charge_id)
        if not charge:
            return jsonify({'success': False, 'error': 'Charge non trouvée'}), 404
        
        # Calculer la répartition
        distributions = ChargeCalculator.calculate_distribution(charge_id)
        
        # Publier la charge
        charge.status = 'published'
        db.session.commit()
        
        # Notifier les résidents
        NotificationService.notify_charge_published(charge)
        
        return jsonify({
            'success': True,
            'message': 'Charge publiée et répartie',
            'distributions_created': len(distributions)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/charges/<int:charge_id>/distributions', methods=['GET'])
@login_required
@superadmin_required
def get_charge_distributions(charge_id):
    """Récupère les distributions d'une charge"""
    try:
        distributions = ChargeDistribution.query.filter_by(charge_id=charge_id).all()
        return jsonify({'success': True, 'distributions': [d.to_dict() for d in distributions]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== PAIEMENTS ====================

@admin_bp.route('/payments', methods=['GET'])
@login_required
@superadmin_required
def get_payments():
    """Récupère tous les paiements"""
    try:
        payments = Payment.query.order_by(Payment.created_at.desc()).all()
        return jsonify({'success': True, 'payments': [p.to_dict() for p in payments]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/payments/<int:payment_id>/validate', methods=['POST'])
@login_required
@superadmin_required
def validate_payment(payment_id):
    """Valide un paiement"""
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            return jsonify({'success': False, 'error': 'Paiement non trouvé'}), 404
        
        payment.status = 'validated'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Paiement validé'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/units/<int:unit_id>/balance', methods=['GET'])
@login_required
@superadmin_required
def get_unit_balance(unit_id):
    """Récupère le solde d'un lot"""
    try:
        balance = ChargeCalculator.get_unit_balance(unit_id)
        unpaid = ChargeCalculator.get_unpaid_charges(unit_id)
        return jsonify({'success': True, 'balance': balance, 'unpaid_charges': unpaid}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ACTUALITÉS ====================

@admin_bp.route('/news', methods=['GET'])
@login_required
@superadmin_required
def get_all_news():
    """Récupère toutes les actualités"""
    try:
        news = News.query.order_by(News.is_pinned.desc(), News.published_at.desc()).all()
        return jsonify({
            'success': True,
            'news': [n.to_dict() for n in news]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/news', methods=['POST'])
@login_required
@superadmin_required
def create_news():
    """Crée une nouvelle actualité"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'title', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        news = News(
            residence_id=data['residence_id'],
            title=data['title'],
            content=data['content'],
            category=data.get('category', 'info'),
            is_important=data.get('is_important', False),
            is_pinned=data.get('is_pinned', False),
            is_published=data.get('is_published', True),
            author_id=current_user.id
        )
        
        db.session.add(news)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Actualité créée', 'news': news.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/news/<int:news_id>', methods=['PUT'])
@login_required
@superadmin_required
def update_news(news_id):
    """Met à jour une actualité"""
    try:
        news = News.query.get(news_id)
        if not news:
            return jsonify({'success': False, 'error': 'Actualité non trouvée'}), 404
        
        data = request.get_json()
        for field in ['title', 'content', 'category', 'is_important', 'is_pinned', 'is_published']:
            if field in data:
                setattr(news, field, data[field])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Actualité mise à jour'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/news/<int:news_id>', methods=['DELETE'])
@login_required
@superadmin_required
def delete_news(news_id):
    """Supprime une actualité"""
    try:
        news = News.query.get(news_id)
        if not news:
            return jsonify({'success': False, 'error': 'Actualité non trouvée'}), 404
        
        db.session.delete(news)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Actualité supprimée'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== MAINTENANCE ====================

@admin_bp.route('/maintenance', methods=['GET'])
@login_required
@admin_or_superadmin_required
def get_all_maintenance():
    """Récupère toutes les demandes de maintenance"""
    try:
        requests = MaintenanceRequest.query.order_by(MaintenanceRequest.created_at.desc()).all()
        return jsonify({'success': True, 'maintenance_requests': [r.to_dict() for r in requests]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance/<int:request_id>', methods=['PUT'])
@login_required
@admin_or_superadmin_required
def update_maintenance(request_id):
    """Met à jour une demande de maintenance"""
    try:
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        data = request.get_json()
        
        # Mettre à jour les champs
        if 'status' in data:
            maintenance_request.status = data['status']
            if data['status'] == 'resolved':
                maintenance_request.resolved_at = datetime.utcnow()
        
        if 'priority' in data:
            maintenance_request.priority = data['priority']
        
        if 'assigned_to' in data:
            maintenance_request.assigned_to = data['assigned_to']
            if not maintenance_request.assigned_at:
                maintenance_request.assigned_at = datetime.utcnow()
        
        if 'assigned_user_id' in data:
            maintenance_request.assigned_user_id = data['assigned_user_id']
            if not maintenance_request.assigned_at:
                maintenance_request.assigned_at = datetime.utcnow()
        
        if 'scheduled_date' in data:
            if data['scheduled_date']:
                maintenance_request.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
            else:
                maintenance_request.scheduled_date = None
        
        if 'admin_notes' in data:
            maintenance_request.admin_notes = data['admin_notes']
        
        db.session.commit()
        
        # Notifier le résident
        NotificationService.notify_maintenance_status_update(maintenance_request)
        
        return jsonify({'success': True, 'message': 'Demande mise à jour', 'maintenance_request': maintenance_request.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance/announcement', methods=['POST'])
@login_required
@admin_or_superadmin_required
def create_maintenance_announcement():
    """Crée une annonce de maintenance planifiée"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['residence_id', 'title', 'description', 'zone']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # Générer un numéro de suivi unique
        tracking_number = MaintenanceRequest.generate_tracking_number(data['residence_id'])
        
        # Créer l'annonce
        announcement = MaintenanceRequest(
            tracking_number=tracking_number,
            request_type='admin_announcement',
            residence_id=data['residence_id'],
            author_id=current_user.id,
            zone=data['zone'],
            zone_details=data.get('zone_details'),
            title=data['title'],
            description=data['description'],
            priority=data.get('priority', 'medium'),
            scheduled_date=datetime.fromisoformat(data['scheduled_date']) if data.get('scheduled_date') else None,
            assigned_to=data.get('assigned_to'),
            assigned_user_id=data.get('assigned_user_id'),
            status='in_progress'
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        # Notifier les résidents
        NotificationService.notify_maintenance_announcement(announcement)
        
        return jsonify({
            'success': True,
            'message': 'Annonce créée avec succès',
            'announcement': announcement.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== COMMENTAIRES MAINTENANCE ====================

@admin_bp.route('/maintenance/<int:request_id>/comments', methods=['GET'])
@login_required
@admin_or_superadmin_required
def get_maintenance_comments(request_id):
    """Récupère les commentaires d'une demande de maintenance"""
    try:
        from backend.models.maintenance_comment import MaintenanceComment
        
        # Vérifier que la demande existe
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        # Récupérer tous les commentaires (incluant les internes)
        comments = MaintenanceComment.query.filter_by(
            maintenance_request_id=request_id
        ).order_by(MaintenanceComment.created_at).all()
        
        return jsonify({
            'success': True,
            'comments': [c.to_dict() for c in comments]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance/<int:request_id>/comments', methods=['POST'])
@login_required
@admin_or_superadmin_required
def add_maintenance_comment(request_id):
    """Ajoute un commentaire à une demande de maintenance"""
    try:
        from backend.models.maintenance_comment import MaintenanceComment
        
        # Vérifier que la demande existe
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        data = request.get_json()
        
        if 'comment_text' not in data or not data['comment_text'].strip():
            return jsonify({'success': False, 'error': 'Le commentaire ne peut pas être vide'}), 400
        
        # Créer le commentaire
        comment = MaintenanceComment(
            maintenance_request_id=request_id,
            author_id=current_user.id,
            comment_text=data['comment_text'],
            comment_type=data.get('comment_type', 'comment'),
            mentioned_user_id=data.get('mentioned_user_id'),
            is_internal=data.get('is_internal', False)
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Notifier si un utilisateur est mentionné
        if comment.mentioned_user_id:
            NotificationService.notify_user_mentioned(comment)
        
        return jsonify({
            'success': True,
            'message': 'Commentaire ajouté',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== DOCUMENTS MAINTENANCE ====================

@admin_bp.route('/maintenance/<int:request_id>/documents', methods=['GET'])
@login_required
@superadmin_required
def get_maintenance_documents(request_id):
    """Récupère les documents d'une demande de maintenance"""
    try:
        from backend.models.maintenance_document import MaintenanceDocument
        
        # Vérifier que la demande existe
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        # Récupérer tous les documents
        documents = MaintenanceDocument.query.filter_by(
            maintenance_request_id=request_id
        ).order_by(MaintenanceDocument.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'documents': [d.to_dict() for d in documents]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance/<int:request_id>/documents', methods=['POST'])
@login_required
@superadmin_required
def upload_maintenance_document(request_id):
    """Upload un document pour une demande de maintenance"""
    import os
    from werkzeug.utils import secure_filename
    from backend.models.maintenance_document import MaintenanceDocument
    
    try:
        # Vérifier que la demande existe
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        # Gérer l'upload de fichier
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nom de fichier invalide'}), 400
        
        # Récupérer les métadonnées depuis le formulaire
        document_type = request.form.get('document_type', 'other')
        title = request.form.get('title', file.filename)
        description = request.form.get('description', '')
        
        # Créer le dossier uploads si nécessaire
        upload_folder = os.path.join('frontend', 'static', 'uploads', 'maintenance', 'documents')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Sécuriser le nom de fichier
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Sauvegarder le fichier
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Obtenir la taille et le type MIME
        file_size = os.path.getsize(file_path)
        mime_type = file.content_type
        
        # Créer l'entrée dans la base de données
        document = MaintenanceDocument(
            maintenance_request_id=request_id,
            document_type=document_type,
            title=title,
            description=description,
            filename=filename,
            file_path=f"/static/uploads/maintenance/documents/{filename}",
            file_size=file_size,
            mime_type=mime_type,
            uploaded_by=current_user.id
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Document uploadé',
            'document': document.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance/documents/<int:document_id>', methods=['DELETE'])
@login_required
@superadmin_required
def delete_maintenance_document(document_id):
    """Supprime un document de maintenance"""
    import os
    from backend.models.maintenance_document import MaintenanceDocument
    
    try:
        document = MaintenanceDocument.query.get(document_id)
        if not document:
            return jsonify({'success': False, 'error': 'Document non trouvé'}), 404
        
        # Supprimer le fichier physique
        try:
            file_path = os.path.join('frontend', document.file_path.lstrip('/'))
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier: {e}")
        
        # Supprimer l'entrée de la base de données
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Document supprimé'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CARNET D'ENTRETIEN ====================

@admin_bp.route('/maintenance-logs', methods=['GET'])
@login_required
@superadmin_required
def get_maintenance_logs():
    """Récupère le carnet d'entretien"""
    try:
        residence_id = request.args.get('residence_id')
        query = MaintenanceLog.query
        if residence_id:
            query = query.filter_by(residence_id=int(residence_id))
        logs = query.order_by(MaintenanceLog.intervention_date.desc()).all()
        return jsonify({'success': True, 'logs': [l.to_dict() for l in logs]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance-logs', methods=['POST'])
@login_required
@superadmin_required
def create_maintenance_log():
    """Crée une entrée dans le carnet d'entretien"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'title', 'description', 'intervention_type', 'contractor_name', 'intervention_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        log = MaintenanceLog(
            residence_id=data['residence_id'],
            maintenance_request_id=data.get('maintenance_request_id'),
            title=data['title'],
            description=data['description'],
            intervention_type=data['intervention_type'],
            category=data.get('category'),
            location=data.get('location'),
            contractor_name=data['contractor_name'],
            contractor_contact=data.get('contractor_contact'),
            intervention_date=datetime.fromisoformat(data['intervention_date']),
            next_intervention_date=datetime.fromisoformat(data['next_intervention_date']) if data.get('next_intervention_date') else None,
            cost=Decimal(str(data['cost'])) if data.get('cost') else None,
            invoice_number=data.get('invoice_number'),
            warranty_end_date=datetime.fromisoformat(data['warranty_end_date']) if data.get('warranty_end_date') else None,
            notes=data.get('notes'),
            created_by=current_user.id
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Intervention enregistrée', 'log': log.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ASSEMBLÉES GÉNÉRALES ====================

@admin_bp.route('/assemblies', methods=['GET'])
@login_required
@superadmin_required
def get_assemblies():
    """Récupère les assemblées générales"""
    try:
        residence_id = request.args.get('residence_id')
        query = GeneralAssembly.query
        if residence_id:
            query = query.filter_by(residence_id=int(residence_id))
        assemblies = query.order_by(GeneralAssembly.scheduled_date.desc()).all()
        return jsonify({'success': True, 'assemblies': [a.to_dict() for a in assemblies]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies', methods=['POST'])
@login_required
@superadmin_required
def create_assembly():
    """Crée une nouvelle assemblée générale"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'title', 'assembly_type', 'scheduled_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # Générer le nom du channel Agora si le mode est online ou both
        meeting_mode = data.get('meeting_mode', 'physical')
        agora_channel_name = None
        if meeting_mode in ['online', 'both']:
            agora_channel_name = AgoraService.generate_channel_name(0)
        
        assembly = GeneralAssembly(
            residence_id=data['residence_id'],
            title=data['title'],
            description=data.get('description'),
            assembly_type=data['assembly_type'],
            meeting_mode=meeting_mode,
            agora_channel_name=agora_channel_name,
            scheduled_date=datetime.fromisoformat(data['scheduled_date']),
            location=data.get('location'),
            quorum_required=data.get('quorum_required', 50),
            created_by=current_user.id
        )
        
        db.session.add(assembly)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'AG créée', 'assembly': assembly.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/send-convocations', methods=['POST'])
@login_required
@superadmin_required
def send_convocations(assembly_id):
    """Envoie les convocations pour une AG"""
    try:
        assembly = GeneralAssembly.query.get(assembly_id)
        if not assembly:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        # Envoyer les convocations
        NotificationService.notify_assembly_convocation(assembly)
        
        assembly.convocation_sent = True
        assembly.convocation_sent_date = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Convocations envoyées'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/start', methods=['POST'])
@login_required
@admin_or_superadmin_required
def start_assembly(assembly_id):
    """Démarre une assemblée générale"""
    try:
        assembly = GeneralAssembly.query.get(assembly_id)
        if not assembly:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        if assembly.status != 'planned':
            return jsonify({'success': False, 'error': 'AG déjà démarrée ou terminée'}), 400
        
        assembly.status = 'in_progress'
        assembly.agora_started_at = datetime.utcnow()
        
        # Démarrer l'enregistrement Agora si mode online/both
        if assembly.meeting_mode in ['online', 'both'] and assembly.agora_channel_name:
            recording_sid = AgoraService.start_cloud_recording(assembly.agora_channel_name, 0)
            assembly.agora_recording_sid = recording_sid
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'AG démarrée', 'assembly': assembly.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/end', methods=['POST'])
@login_required
@admin_or_superadmin_required
def end_assembly(assembly_id):
    """Termine une assemblée générale"""
    try:
        assembly = GeneralAssembly.query.get(assembly_id)
        if not assembly:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        assembly.status = 'completed'
        assembly.end_date = datetime.utcnow()
        
        # Arrêter l'enregistrement Agora
        if assembly.agora_recording_sid:
            AgoraService.stop_cloud_recording(assembly.agora_recording_sid)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'AG terminée', 'assembly': assembly.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/agora-token', methods=['GET'])
@login_required
def get_agora_token(assembly_id):
    """Génère un token Agora pour rejoindre une AG en ligne"""
    try:
        assembly = GeneralAssembly.query.get(assembly_id)
        if not assembly:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        if not assembly.agora_channel_name:
            return jsonify({'success': False, 'error': 'Cette AG ne supporte pas le mode en ligne'}), 400
        
        # Générer le token RTC
        uid = current_user.id
        rtc_token = AgoraService.generate_rtc_token(
            assembly.agora_channel_name,
            uid,
            role='publisher',
            expiration_seconds=7200  # 2 heures
        )
        
        if not rtc_token:
            return jsonify({
                'success': False,
                'error': 'Impossible de générer le token Agora. Vérifiez la configuration AGORA_APP_ID et AGORA_APP_CERTIFICATE.'
            }), 500
        
        return jsonify({
            'success': True,
            'app_id': AgoraService.get_app_id(),
            'channel_name': assembly.agora_channel_name,
            'token': rtc_token,
            'uid': uid
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/attendance', methods=['GET'])
@login_required
@admin_or_superadmin_required
def get_attendance(assembly_id):
    """Récupère la liste des présences pour une AG"""
    try:
        attendances = Attendance.query.filter_by(assembly_id=assembly_id).all()
        users_data = []
        
        for attendance in attendances:
            user = User.query.get(attendance.user_id)
            if user:
                users_data.append({
                    'attendance_id': attendance.id,
                    'user_id': user.id,
                    'user_name': f"{user.first_name} {user.last_name}",
                    'email': user.email,
                    'is_present': attendance.is_present,
                    'attendance_mode': attendance.attendance_mode,
                    'presence_marked_at': attendance.presence_marked_at.isoformat() if attendance.presence_marked_at else None
                })
        
        return jsonify({'success': True, 'attendances': users_data}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/attendance/mark', methods=['POST'])
@login_required
@admin_or_superadmin_required
def mark_attendance(assembly_id):
    """Marque la présence d'un ou plusieurs utilisateurs (syndic uniquement)"""
    try:
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        attendance_mode = data.get('attendance_mode', 'physical')
        
        if not user_ids:
            return jsonify({'success': False, 'error': 'Aucun utilisateur spécifié'}), 400
        
        marked_count = 0
        for user_id in user_ids:
            # Chercher ou créer l'attendance
            attendance = Attendance.query.filter_by(
                assembly_id=assembly_id,
                user_id=user_id
            ).first()
            
            if not attendance:
                attendance = Attendance(
                    assembly_id=assembly_id,
                    user_id=user_id
                )
                db.session.add(attendance)
            
            attendance.is_present = True
            attendance.attendance_mode = attendance_mode
            attendance.presence_marked_at = datetime.utcnow()
            attendance.marked_by = current_user.id
            marked_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{marked_count} présence(s) marquée(s)',
            'count': marked_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/attendance/join-online', methods=['POST'])
@login_required
def join_online(assembly_id):
    """Auto-marque la présence en ligne lorsqu'un utilisateur rejoint"""
    try:
        # Chercher ou créer l'attendance
        attendance = Attendance.query.filter_by(
            assembly_id=assembly_id,
            user_id=current_user.id
        ).first()
        
        if not attendance:
            attendance = Attendance(
                assembly_id=assembly_id,
                user_id=current_user.id
            )
            db.session.add(attendance)
        
        attendance.is_present = True
        attendance.attendance_mode = 'online'
        attendance.presence_marked_at = datetime.utcnow()
        attendance.marked_by = current_user.id  # Auto-marqué
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Présence en ligne enregistrée',
            'attendance': attendance.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/resolutions', methods=['GET'])
@login_required
def get_resolutions(assembly_id):
    """Récupère les résolutions d'une AG"""
    try:
        resolutions = Resolution.query.filter_by(assembly_id=assembly_id).order_by(Resolution.order).all()
        return jsonify({'success': True, 'resolutions': [r.to_dict() for r in resolutions]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/assemblies/<int:assembly_id>/resolutions', methods=['POST'])
@login_required
@admin_or_superadmin_required
def create_resolution(assembly_id):
    """Crée une résolution pour une AG"""
    try:
        data = request.get_json()
        required_fields = ['title']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        resolution = Resolution(
            assembly_id=assembly_id,
            title=data['title'],
            description=data.get('description'),
            order=data.get('order', 0),
            vote_type=data.get('vote_type', 'simple')
        )
        
        db.session.add(resolution)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Résolution créée', 'resolution': resolution.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/resolutions/<int:resolution_id>/vote', methods=['POST'])
@login_required
def submit_vote(resolution_id):
    """Soumet un vote pour une résolution"""
    try:
        resolution = Resolution.query.get(resolution_id)
        if not resolution:
            return jsonify({'success': False, 'error': 'Résolution non trouvée'}), 404
        
        # Vérifier que l'utilisateur est présent à l'AG
        attendance = Attendance.query.filter_by(
            assembly_id=resolution.assembly_id,
            user_id=current_user.id,
            is_present=True
        ).first()
        
        if not attendance:
            return jsonify({'success': False, 'error': 'Vous devez être marqué présent pour voter'}), 403
        
        data = request.get_json()
        vote_value = data.get('vote_value')  # 'for', 'against', 'abstain'
        
        if vote_value not in ['for', 'against', 'abstain']:
            return jsonify({'success': False, 'error': 'Valeur de vote invalide'}), 400
        
        # Chercher ou créer le vote
        vote = Vote.query.filter_by(
            resolution_id=resolution_id,
            user_id=current_user.id
        ).first()
        
        if vote:
            # Mettre à jour le vote existant
            old_value = vote.vote_value
            vote.vote_value = vote_value
            vote.voted_at = datetime.utcnow()
            
            # Ajuster les compteurs
            if old_value == 'for':
                resolution.votes_for -= 1
            elif old_value == 'against':
                resolution.votes_against -= 1
            elif old_value == 'abstain':
                resolution.votes_abstain -= 1
        else:
            # Créer un nouveau vote
            vote = Vote(
                resolution_id=resolution_id,
                user_id=current_user.id,
                vote_value=vote_value
            )
            db.session.add(vote)
        
        # Incrémenter les compteurs
        if vote_value == 'for':
            resolution.votes_for += 1
        elif vote_value == 'against':
            resolution.votes_against += 1
        elif vote_value == 'abstain':
            resolution.votes_abstain += 1
        
        # Mettre à jour le statut si nécessaire
        if resolution.status == 'pending':
            resolution.status = 'voting'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Vote enregistré',
            'vote': vote.to_dict(),
            'resolution': resolution.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/resolutions/<int:resolution_id>/close', methods=['POST'])
@login_required
@admin_or_superadmin_required
def close_resolution(resolution_id):
    """Clôture une résolution et détermine le résultat"""
    try:
        resolution = Resolution.query.get(resolution_id)
        if not resolution:
            return jsonify({'success': False, 'error': 'Résolution non trouvée'}), 404
        
        total_votes = resolution.votes_for + resolution.votes_against + resolution.votes_abstain
        
        if total_votes == 0:
            resolution.status = 'rejected'
        elif resolution.votes_for > resolution.votes_against:
            resolution.status = 'approved'
        else:
            resolution.status = 'rejected'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Résolution clôturée',
            'resolution': resolution.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CONTENTIEUX ====================

@admin_bp.route('/litigations', methods=['GET'])
@login_required
@superadmin_required
def get_litigations():
    """Récupère les contentieux"""
    try:
        residence_id = request.args.get('residence_id')
        query = Litigation.query
        if residence_id:
            query = query.filter_by(residence_id=int(residence_id))
        litigations = query.order_by(Litigation.start_date.desc()).all()
        return jsonify({'success': True, 'litigations': [l.to_dict() for l in litigations]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/litigations', methods=['POST'])
@login_required
@superadmin_required
def create_litigation():
    """Crée un nouveau contentieux"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'title', 'description', 'litigation_type', 'start_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # Générer un numéro de référence
        import uuid
        reference = f"LIT-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
        
        litigation = Litigation(
            residence_id=data['residence_id'],
            unit_id=data.get('unit_id'),
            party_name=data.get('party_name'),
            party_contact=data.get('party_contact'),
            reference_number=reference,
            title=data['title'],
            description=data['description'],
            litigation_type=data['litigation_type'],
            amount=Decimal(str(data['amount'])) if data.get('amount') else None,
            start_date=datetime.fromisoformat(data['start_date']),
            hearing_date=datetime.fromisoformat(data['hearing_date']) if data.get('hearing_date') else None,
            lawyer_name=data.get('lawyer_name'),
            lawyer_contact=data.get('lawyer_contact'),
            notes=data.get('notes'),
            created_by=current_user.id
        )
        
        db.session.add(litigation)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Contentieux créé', 'litigation': litigation.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/litigations/<int:litigation_id>', methods=['PUT'])
@login_required
@superadmin_required
def update_litigation(litigation_id):
    """Met à jour un contentieux"""
    try:
        litigation = Litigation.query.get(litigation_id)
        if not litigation:
            return jsonify({'success': False, 'error': 'Contentieux non trouvé'}), 404
        
        data = request.get_json()
        
        for field in ['status', 'notes', 'resolution_notes', 'lawyer_name', 'lawyer_contact']:
            if field in data:
                setattr(litigation, field, data[field])
        
        if 'resolution_date' in data:
            litigation.resolution_date = datetime.fromisoformat(data['resolution_date'])
        
        if 'hearing_date' in data:
            litigation.hearing_date = datetime.fromisoformat(data['hearing_date'])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Contentieux mis à jour'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== SONDAGES ====================

@admin_bp.route('/polls', methods=['POST'])
@login_required
@superadmin_required
def create_poll():
    """Crée un nouveau sondage"""
    try:
        data = request.get_json()
        required_fields = ['residence_id', 'question', 'options']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        poll = Poll(
            residence_id=data['residence_id'],
            question=data['question'],
            description=data.get('description'),
            allow_multiple=data.get('allow_multiple', False),
            is_anonymous=data.get('is_anonymous', False),
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
            created_by=current_user.id
        )
        
        db.session.add(poll)
        db.session.flush()
        
        # Ajouter les options
        for idx, option_text in enumerate(data['options']):
            option = PollOption(
                poll_id=poll.id,
                option_text=option_text,
                order=idx
            )
            db.session.add(option)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Sondage créé', 'poll': poll.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/polls/<int:poll_id>/close', methods=['POST'])
@login_required
@superadmin_required
def close_poll(poll_id):
    """Ferme un sondage"""
    try:
        poll = Poll.query.get(poll_id)
        if not poll:
            return jsonify({'success': False, 'error': 'Sondage non trouvé'}), 404
        
        poll.status = 'closed'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Sondage fermé', 'results': poll.get_results()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== UTILISATEURS ====================

@admin_bp.route('/users', methods=['GET'])
@login_required
@superadmin_required
def get_users():
    """Récupère la liste des utilisateurs"""
    try:
        users = User.query.all()
        return jsonify({'success': True, 'users': [u.to_dict() for u in users]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
@superadmin_required
def update_user(user_id):
    """Met à jour un utilisateur"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        for field in ['first_name', 'last_name', 'phone', 'role', 'is_active', 'residence_id', 'unit_id']:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Utilisateur mis à jour'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@login_required
@superadmin_required
def update_user_role(user_id):
    """Met à jour le rôle d'un utilisateur (réservé au superadmin)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        new_role = data.get('role')
        
        # Validation du rôle
        valid_roles = ['superadmin', 'admin', 'owner', 'resident']
        if new_role not in valid_roles:
            return jsonify({
                'success': False, 
                'error': f'Rôle invalide. Rôles autorisés: {", ".join(valid_roles)}'
            }), 400
        
        # Empêcher de modifier son propre rôle
        if user.id == current_user.id:
            return jsonify({
                'success': False, 
                'error': 'Vous ne pouvez pas modifier votre propre rôle'
            }), 403
        
        old_role = user.role
        user.role = new_role
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Rôle mis à jour de {old_role} vers {new_role}',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/users/stats', methods=['GET'])
@login_required
@superadmin_required
def get_user_stats():
    """Récupère les statistiques des utilisateurs par rôle"""
    try:
        stats = {
            'superadmin': User.query.filter_by(role='superadmin').count(),
            'admin': User.query.filter_by(role='admin').count(),
            'owner': User.query.filter_by(role='owner').count(),
            'resident': User.query.filter_by(role='resident').count()
        }
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== SETTINGS & PERMISSIONS ====================

@admin_bp.route('/settings/permissions', methods=['POST'])
@login_required
@superadmin_required
def save_permissions():
    """Sauvegarde les permissions des rôles
    
    Note: Cette fonctionnalité est en cours de développement.
    Pour une implémentation complète, les permissions devraient être:
    - Stockées dans une table dédiée ou un fichier de configuration
    - Chargées au démarrage de l'application
    - Utilisées pour contrôler l'accès aux fonctionnalités
    
    Actuellement, les permissions sont définies de manière statique dans le code.
    """
    try:
        data = request.get_json()
        
        # Validation des données
        if not isinstance(data, dict):
            return jsonify({
                'success': False,
                'error': 'Format de données invalide'
            }), 400
        
        # Validation que seuls les rôles autorisés sont modifiés
        valid_roles = ['admin', 'owner', 'resident']
        for role in data.keys():
            if role not in valid_roles:
                return jsonify({
                    'success': False,
                    'error': f'Rôle invalide: {role}. Seuls {", ".join(valid_roles)} peuvent être modifiés.'
                }), 400
        
        # TODO: Implémenter la persistance des permissions
        # Options possibles:
        # 1. Table Permission(role, resource, action, allowed)
        # 2. Fichier JSON de configuration
        # 3. Variables d'environnement
        
        # Pour l'instant, on log les changements
        print(f"[PERMISSIONS] Superadmin {current_user.email} a modifié les permissions:")
        for role, permissions in data.items():
            print(f"  - {role}: {len(permissions)} permissions activées")
        
        return jsonify({
            'success': True,
            'message': 'Configuration des permissions enregistrée (fonctionnalité en développement)',
            'note': 'Les permissions seront pleinement fonctionnelles dans une prochaine version',
            'permissions': data
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ASSIGNATION ADMINS AUX RÉSIDENCES ====================

@admin_bp.route('/residences/<int:residence_id>/admins', methods=['POST'])
@login_required
@superadmin_required
def assign_admin_to_residence(residence_id):
    """Assigne un ou plusieurs admins à une résidence"""
    try:
        residence = Residence.query.get(residence_id)
        if not residence:
            return jsonify({'success': False, 'error': 'Résidence non trouvée'}), 404
        
        data = request.get_json()
        admin_ids = data.get('admin_ids', [])
        
        if not admin_ids:
            return jsonify({'success': False, 'error': 'Aucun administrateur spécifié'}), 400
        
        assigned_count = 0
        for admin_id in admin_ids:
            admin = User.query.get(admin_id)
            if not admin or admin.role not in ['admin', 'superadmin']:
                continue
            
            # Vérifier si déjà assigné
            existing = ResidenceAdmin.query.filter_by(
                residence_id=residence_id,
                user_id=admin_id
            ).first()
            
            if not existing:
                assignment = ResidenceAdmin(
                    residence_id=residence_id,
                    user_id=admin_id,
                    assigned_by=current_user.id
                )
                db.session.add(assignment)
                assigned_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{assigned_count} administrateur(s) assigné(s)'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/residences/<int:residence_id>/admins', methods=['GET'])
@login_required
@superadmin_required
def get_residence_admins(residence_id):
    """Récupère les admins assignés à une résidence"""
    try:
        assignments = ResidenceAdmin.query.filter_by(residence_id=residence_id).all()
        admin_ids = [a.user_id for a in assignments]
        admins = User.query.filter(User.id.in_(admin_ids)).all() if admin_ids else []
        
        return jsonify({
            'success': True,
            'admins': [admin.to_dict() for admin in admins]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/residences/<int:residence_id>/admins/<int:admin_id>', methods=['DELETE'])
@login_required
@superadmin_required
def remove_admin_from_residence(residence_id, admin_id):
    """Retire un admin d'une résidence"""
    try:
        assignment = ResidenceAdmin.query.filter_by(
            residence_id=residence_id,
            user_id=admin_id
        ).first()
        
        if not assignment:
            return jsonify({'success': False, 'error': 'Assignation non trouvée'}), 404
        
        db.session.delete(assignment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Admin retiré de la résidence'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CRÉATION DE RÉSIDENCE AVEC WIZARD ====================

@admin_bp.route('/residences/wizard', methods=['POST'])
@login_required
@superadmin_required
def create_residence_wizard():
    """Crée une résidence complète avec structure et admins (wizard)"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'address', 'city']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # Créer la résidence
        residence = Residence(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            postal_code=data.get('postal_code'),
            description=data.get('description'),
            total_units=data.get('total_units', 0),
            syndic_name=data.get('syndic_name'),
            syndic_email=data.get('syndic_email'),
            syndic_phone=data.get('syndic_phone')
        )
        
        db.session.add(residence)
        db.session.flush()  # Pour obtenir l'ID
        
        # Créer les unités si fournies
        units_data = data.get('units', [])
        created_units = 0
        
        for unit_data in units_data:
            unit = Unit(
                residence_id=residence.id,
                unit_number=unit_data.get('unit_number'),
                floor=unit_data.get('floor'),
                building=unit_data.get('building') or unit_data.get('division'),
                unit_type=unit_data.get('unit_type'),
                surface_area=unit_data.get('surface_area'),
                owner_name=unit_data.get('owner_name'),
                owner_email=unit_data.get('owner_email'),
                owner_phone=unit_data.get('owner_phone'),
                is_occupied=unit_data.get('is_occupied', True)
            )
            db.session.add(unit)
            created_units += 1
        
        # Mettre à jour le nombre total d'unités
        if created_units > 0:
            residence.total_units = created_units
        
        # Assigner les admins
        admin_ids = data.get('admin_ids', [])
        assigned_admins = 0
        
        for admin_id in admin_ids:
            admin = User.query.get(admin_id)
            if admin and admin.role in ['admin', 'superadmin']:
                assignment = ResidenceAdmin(
                    residence_id=residence.id,
                    user_id=admin_id,
                    assigned_by=current_user.id
                )
                db.session.add(assignment)
                assigned_admins += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Résidence créée avec succès',
            'residence': residence.to_dict(),
            'stats': {
                'units_created': created_units,
                'admins_assigned': assigned_admins
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== PARAMÈTRES DE L'APPLICATION ====================

@admin_bp.route('/settings', methods=['GET'])
@login_required
@superadmin_required
def get_settings():
    """Récupère tous les paramètres de l'application"""
    try:
        settings = AppSettings.query.all()
        return jsonify({
            'success': True,
            'settings': {s.key: s.to_dict() for s in settings}
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/settings/<key>', methods=['GET'])
@login_required
@superadmin_required
def get_setting(key):
    """Récupère un paramètre spécifique"""
    try:
        value = AppSettings.get_value(key)
        return jsonify({
            'success': True,
            'key': key,
            'value': value
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/settings', methods=['POST'])
@login_required
@superadmin_required
def set_setting():
    """Définit ou met à jour un paramètre"""
    try:
        data = request.get_json(silent=True)
        
        if not data or not isinstance(data, dict):
            return jsonify({
                'success': False,
                'error': 'Données JSON invalides ou manquantes'
            }), 400
        
        if 'key' not in data or 'value' not in data:
            return jsonify({
                'success': False,
                'error': 'Les champs key et value sont requis'
            }), 400
        
        setting = AppSettings.set_value(
            key=data['key'],
            value=data['value'],
            description=data.get('description')
        )
        
        return jsonify({
            'success': True,
            'message': 'Paramètre sauvegardé avec succès',
            'setting': setting.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/settings/custom-head', methods=['GET'])
@login_required
@superadmin_required
def get_custom_head():
    """Récupère le code <head> personnalisé"""
    try:
        code = AppSettings.get_value('custom_head_code', '')
        return jsonify({
            'success': True,
            'code': code
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/settings/custom-head', methods=['POST'])
@login_required
@superadmin_required
def set_custom_head():
    """Définit le code <head> personnalisé"""
    try:
        data = request.get_json(silent=True)
        
        if not data or not isinstance(data, dict):
            return jsonify({
                'success': False,
                'error': 'Données JSON invalides ou manquantes'
            }), 400
        
        code = data.get('code', '')
        
        setting = AppSettings.set_value(
            key='custom_head_code',
            value=code,
            description='Code personnalisé à injecter dans l\'élément <head>'
        )
        
        return jsonify({
            'success': True,
            'message': 'Code <head> personnalisé sauvegardé avec succès',
            'setting': setting.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
