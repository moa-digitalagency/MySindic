#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Routes Résidents
Routes pour toutes les fonctionnalités résidents

Date: 24 octobre 2025
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from decimal import Decimal

from backend.models import db
from backend.models.maintenance import MaintenanceRequest
from backend.models.news import News
from backend.models.poll import Poll, PollOption, PollVote
from backend.models.document import Document
from backend.models.charge import ChargeDistribution
from backend.models.payment import Payment
from backend.models.general_assembly import GeneralAssembly, Resolution, Vote, Attendance
from backend.models.maintenance_log import MaintenanceLog
from backend.utils.charge_calculator import ChargeCalculator
from backend.utils.notification_service import NotificationService

# Créer le blueprint
resident_bp = Blueprint('resident', __name__)


# ==================== DASHBOARD ====================

@resident_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Tableau de bord du résident"""
    try:
        # Demandes de maintenance récentes
        maintenance_requests = MaintenanceRequest.query.filter_by(
            requester_id=current_user.id
        ).order_by(MaintenanceRequest.created_at.desc()).limit(5).all()
        
        # Actualités de la résidence
        news = []
        if current_user.residence_id:
            news = News.query.filter_by(
                residence_id=current_user.residence_id,
                is_published=True
            ).order_by(News.published_at.desc()).limit(5).all()
        
        # Solde du compte (si l'utilisateur a un lot)
        balance = None
        if current_user.unit_id:
            balance = ChargeCalculator.get_unit_balance(current_user.unit_id)
        
        # Assemblées générales à venir
        upcoming_assemblies = []
        if current_user.residence_id:
            upcoming_assemblies = GeneralAssembly.query.filter_by(
                residence_id=current_user.residence_id,
                status='planned'
            ).filter(GeneralAssembly.scheduled_date >= datetime.utcnow()).order_by(
                GeneralAssembly.scheduled_date
            ).limit(3).all()
        
        return jsonify({
            'success': True,
            'maintenance_requests': [m.to_dict() for m in maintenance_requests],
            'news': [n.to_dict() for n in news],
            'balance': balance,
            'upcoming_assemblies': [a.to_dict() for a in upcoming_assemblies]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ACTUALITÉS ====================

@resident_bp.route('/news', methods=['GET'])
@login_required
def get_news():
    """Récupère les actualités de la résidence"""
    try:
        if not current_user.residence_id:
            return jsonify({'success': True, 'news': []}), 200
        
        news = News.query.filter_by(
            residence_id=current_user.residence_id,
            is_published=True
        ).order_by(News.is_pinned.desc(), News.published_at.desc()).all()
        
        return jsonify({'success': True, 'news': [n.to_dict() for n in news]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/news/<int:news_id>', methods=['GET'])
@login_required
def get_news_detail(news_id):
    """Récupère le détail d'une actualité"""
    try:
        news = News.query.get(news_id)
        if not news or news.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Actualité non trouvée'}), 404
        
        return jsonify({'success': True, 'news': news.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== MAINTENANCE ====================

@resident_bp.route('/maintenance', methods=['POST'])
@login_required
def create_maintenance_request():
    """Crée une nouvelle demande de maintenance"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # Vérifier que l'utilisateur a une résidence
        if not current_user.residence_id:
            return jsonify({'success': False, 'error': 'Vous devez être associé à une résidence'}), 400
        
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
        
        # Notifier les administrateurs
        NotificationService.notify_new_maintenance_request(maintenance_request)
        
        return jsonify({
            'success': True,
            'message': 'Demande créée avec succès',
            'maintenance_request': maintenance_request.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/maintenance', methods=['GET'])
@login_required
def get_maintenance_requests():
    """Récupère les demandes de maintenance du résident"""
    try:
        requests = MaintenanceRequest.query.filter_by(
            requester_id=current_user.id
        ).order_by(MaintenanceRequest.created_at.desc()).all()
        
        return jsonify({'success': True, 'maintenance_requests': [r.to_dict() for r in requests]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/maintenance/<int:request_id>', methods=['GET'])
@login_required
def get_maintenance_detail(request_id):
    """Récupère le détail d'une demande de maintenance"""
    try:
        maintenance_request = MaintenanceRequest.query.get(request_id)
        
        if not maintenance_request or maintenance_request.requester_id != current_user.id:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        return jsonify({'success': True, 'maintenance_request': maintenance_request.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CHARGES ET PAIEMENTS ====================

@resident_bp.route('/charges', methods=['GET'])
@login_required
def get_my_charges():
    """Récupère les charges du résident"""
    try:
        if not current_user.unit_id:
            return jsonify({'success': True, 'charges': [], 'message': 'Aucun lot associé'}), 200
        
        distributions = ChargeDistribution.query.filter_by(unit_id=current_user.unit_id).all()
        
        charges_data = []
        for dist in distributions:
            charge_dict = dist.charge.to_dict()
            charge_dict['distribution'] = dist.to_dict()
            charges_data.append(charge_dict)
        
        return jsonify({'success': True, 'charges': charges_data}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/charges/unpaid', methods=['GET'])
@login_required
def get_unpaid_charges():
    """Récupère les charges impayées"""
    try:
        if not current_user.unit_id:
            return jsonify({'success': True, 'unpaid_charges': []}), 200
        
        unpaid = ChargeCalculator.get_unpaid_charges(current_user.unit_id)
        
        return jsonify({'success': True, 'unpaid_charges': unpaid}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/balance', methods=['GET'])
@login_required
def get_balance():
    """Récupère le solde du compte"""
    try:
        if not current_user.unit_id:
            return jsonify({'success': False, 'error': 'Aucun lot associé'}), 400
        
        balance = ChargeCalculator.get_unit_balance(current_user.unit_id)
        
        return jsonify({'success': True, 'balance': balance}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/payments', methods=['POST'])
@login_required
def declare_payment():
    """Déclare un paiement"""
    try:
        if not current_user.unit_id:
            return jsonify({'success': False, 'error': 'Aucun lot associé'}), 400
        
        data = request.get_json()
        required_fields = ['amount', 'payment_method', 'payment_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        payment = Payment(
            unit_id=current_user.unit_id,
            user_id=current_user.id,
            amount=Decimal(str(data['amount'])),
            payment_method=data['payment_method'],
            reference=data.get('reference'),
            description=data.get('description'),
            payment_date=datetime.fromisoformat(data['payment_date']),
            status='pending'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Paiement enregistré', 'payment': payment.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/payments', methods=['GET'])
@login_required
def get_my_payments():
    """Récupère l'historique des paiements"""
    try:
        payments = Payment.query.filter_by(user_id=current_user.id).order_by(Payment.payment_date.desc()).all()
        
        return jsonify({'success': True, 'payments': [p.to_dict() for p in payments]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== DOCUMENTS ====================

@resident_bp.route('/documents', methods=['GET'])
@login_required
def get_documents():
    """Récupère les documents accessibles au résident"""
    try:
        if not current_user.residence_id:
            return jsonify({'success': True, 'documents': []}), 200
        
        # Documents publics de la résidence
        documents = Document.query.filter_by(
            residence_id=current_user.residence_id,
            is_public=True
        ).order_by(Document.document_date.desc()).all()
        
        return jsonify({'success': True, 'documents': [d.to_dict() for d in documents]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/documents/<int:document_id>', methods=['GET'])
@login_required
def get_document_detail(document_id):
    """Récupère le détail d'un document"""
    try:
        document = Document.query.get(document_id)
        
        if not document or document.residence_id != current_user.residence_id or not document.is_public:
            return jsonify({'success': False, 'error': 'Document non accessible'}), 404
        
        return jsonify({'success': True, 'document': document.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== SONDAGES ====================

@resident_bp.route('/polls', methods=['GET'])
@login_required
def get_polls():
    """Récupère les sondages de la résidence"""
    try:
        if not current_user.residence_id:
            return jsonify({'success': True, 'polls': []}), 200
        
        polls = Poll.query.filter_by(
            residence_id=current_user.residence_id,
            status='active'
        ).order_by(Poll.created_at.desc()).all()
        
        polls_data = []
        for poll in polls:
            poll_dict = poll.to_dict()
            
            # Vérifier si l'utilisateur a déjà voté
            user_vote = PollVote.query.filter_by(poll_id=poll.id, user_id=current_user.id).first()
            poll_dict['has_voted'] = user_vote is not None
            poll_dict['options'] = [opt.to_dict() for opt in poll.options]
            
            polls_data.append(poll_dict)
        
        return jsonify({'success': True, 'polls': polls_data}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/polls/<int:poll_id>', methods=['GET'])
@login_required
def get_poll_detail(poll_id):
    """Récupère le détail d'un sondage"""
    try:
        poll = Poll.query.get(poll_id)
        
        if not poll or poll.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Sondage non trouvé'}), 404
        
        poll_dict = poll.to_dict()
        poll_dict['options'] = [opt.to_dict() for opt in poll.options]
        
        # Vérifier si l'utilisateur a déjà voté
        user_vote = PollVote.query.filter_by(poll_id=poll.id, user_id=current_user.id).first()
        poll_dict['has_voted'] = user_vote is not None
        
        # Si le sondage est fermé ou l'utilisateur a voté, afficher les résultats
        if poll.status == 'closed' or user_vote:
            poll_dict['results'] = poll.get_results()
        
        return jsonify({'success': True, 'poll': poll_dict}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/polls/<int:poll_id>/vote', methods=['POST'])
@login_required
def vote_poll(poll_id):
    """Vote pour un sondage"""
    try:
        poll = Poll.query.get(poll_id)
        
        if not poll or poll.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Sondage non trouvé'}), 404
        
        if poll.status != 'active':
            return jsonify({'success': False, 'error': 'Ce sondage n\'est plus actif'}), 400
        
        data = request.get_json()
        option_id = data.get('option_id')
        
        if not option_id:
            return jsonify({'success': False, 'error': 'Option requise'}), 400
        
        # Vérifier que l'option appartient à ce sondage
        option = PollOption.query.get(option_id)
        if not option or option.poll_id != poll_id:
            return jsonify({'success': False, 'error': 'Option invalide'}), 400
        
        # Vérifier si l'utilisateur a déjà voté
        existing_vote = PollVote.query.filter_by(poll_id=poll_id, user_id=current_user.id).first()
        if existing_vote and not poll.allow_multiple:
            return jsonify({'success': False, 'error': 'Vous avez déjà voté'}), 400
        
        # Enregistrer le vote
        vote = PollVote(
            poll_id=poll_id,
            option_id=option_id,
            user_id=current_user.id
        )
        
        db.session.add(vote)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Vote enregistré'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ASSEMBLÉES GÉNÉRALES ====================

@resident_bp.route('/assemblies', methods=['GET'])
@login_required
def get_assemblies():
    """Récupère les assemblées générales"""
    try:
        if not current_user.residence_id:
            return jsonify({'success': True, 'assemblies': []}), 200
        
        assemblies = GeneralAssembly.query.filter_by(
            residence_id=current_user.residence_id
        ).order_by(GeneralAssembly.scheduled_date.desc()).all()
        
        return jsonify({'success': True, 'assemblies': [a.to_dict() for a in assemblies]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/assemblies/<int:assembly_id>', methods=['GET'])
@login_required
def get_assembly_detail(assembly_id):
    """Récupère le détail d'une assemblée"""
    try:
        assembly = GeneralAssembly.query.get(assembly_id)
        
        if not assembly or assembly.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        assembly_dict = assembly.to_dict()
        
        # Ajouter les résolutions
        resolutions = Resolution.query.filter_by(assembly_id=assembly_id).order_by(Resolution.order).all()
        assembly_dict['resolutions'] = [r.to_dict() for r in resolutions]
        
        # Vérifier la présence de l'utilisateur
        attendance = Attendance.query.filter_by(assembly_id=assembly_id, user_id=current_user.id).first()
        assembly_dict['is_attending'] = attendance.is_present if attendance else False
        
        return jsonify({'success': True, 'assembly': assembly_dict}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/assemblies/<int:assembly_id>/attend', methods=['POST'])
@login_required
def register_attendance(assembly_id):
    """Enregistre la présence à une AG"""
    try:
        assembly = GeneralAssembly.query.get(assembly_id)
        
        if not assembly or assembly.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        # Vérifier si déjà enregistré
        attendance = Attendance.query.filter_by(assembly_id=assembly_id, user_id=current_user.id).first()
        
        if attendance:
            attendance.is_present = True
        else:
            attendance = Attendance(
                assembly_id=assembly_id,
                user_id=current_user.id,
                is_present=True
            )
            db.session.add(attendance)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Présence enregistrée'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/resolutions/<int:resolution_id>/vote', methods=['POST'])
@login_required
def vote_resolution(resolution_id):
    """Vote sur une résolution"""
    try:
        resolution = Resolution.query.get(resolution_id)
        
        if not resolution:
            return jsonify({'success': False, 'error': 'Résolution non trouvée'}), 404
        
        # Vérifier que l'utilisateur appartient à la résidence de l'AG
        assembly = resolution.assembly
        if assembly.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        data = request.get_json()
        vote_value = data.get('vote_value')
        
        if vote_value not in ['for', 'against', 'abstain']:
            return jsonify({'success': False, 'error': 'Vote invalide'}), 400
        
        # Vérifier si l'utilisateur a déjà voté
        existing_vote = Vote.query.filter_by(resolution_id=resolution_id, user_id=current_user.id).first()
        
        if existing_vote:
            # Mettre à jour le vote
            existing_vote.vote_value = vote_value
        else:
            # Créer un nouveau vote
            vote = Vote(
                resolution_id=resolution_id,
                user_id=current_user.id,
                vote_value=vote_value
            )
            db.session.add(vote)
        
        db.session.commit()
        
        # Mettre à jour les compteurs de la résolution
        votes = Vote.query.filter_by(resolution_id=resolution_id).all()
        resolution.votes_for = sum(1 for v in votes if v.vote_value == 'for')
        resolution.votes_against = sum(1 for v in votes if v.vote_value == 'against')
        resolution.votes_abstain = sum(1 for v in votes if v.vote_value == 'abstain')
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Vote enregistré'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== CARNET D'ENTRETIEN (Consultation) ====================

@resident_bp.route('/maintenance-logs', methods=['GET'])
@login_required
def get_maintenance_logs():
    """Récupère l'historique des interventions"""
    try:
        if not current_user.residence_id:
            return jsonify({'success': True, 'logs': []}), 200
        
        logs = MaintenanceLog.query.filter_by(
            residence_id=current_user.residence_id
        ).order_by(MaintenanceLog.intervention_date.desc()).limit(50).all()
        
        return jsonify({'success': True, 'logs': [l.to_dict() for l in logs]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
