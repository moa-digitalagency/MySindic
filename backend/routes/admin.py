#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Solution complète et digitale pour les syndics et résidents au Maroc.

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
from backend.utils.charge_calculator import ChargeCalculator
from backend.utils.notification_service import NotificationService

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
@superadmin_required
def get_all_maintenance():
    """Récupère toutes les demandes de maintenance"""
    try:
        requests = MaintenanceRequest.query.order_by(MaintenanceRequest.created_at.desc()).all()
        return jsonify({'success': True, 'maintenance_requests': [r.to_dict() for r in requests]}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/maintenance/<int:request_id>', methods=['PUT'])
@login_required
@superadmin_required
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
            if data['status'] == 'completed':
                maintenance_request.completed_at = datetime.utcnow()
        
        if 'assigned_to' in data:
            maintenance_request.assigned_to = data['assigned_to']
            maintenance_request.assigned_at = datetime.utcnow()
        
        if 'scheduled_date' in data:
            maintenance_request.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        
        if 'admin_notes' in data:
            maintenance_request.admin_notes = data['admin_notes']
        
        if 'resolution_notes' in data:
            maintenance_request.resolution_notes = data['resolution_notes']
        
        db.session.commit()
        
        # Notifier le résident
        NotificationService.notify_maintenance_status_update(maintenance_request)
        
        return jsonify({'success': True, 'message': 'Demande mise à jour'}), 200
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
        
        assembly = GeneralAssembly(
            residence_id=data['residence_id'],
            title=data['title'],
            description=data.get('description'),
            assembly_type=data['assembly_type'],
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


@admin_bp.route('/assemblies/<int:assembly_id>/resolutions', methods=['POST'])
@login_required
@superadmin_required
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
