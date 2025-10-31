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
from backend.services.charge_calculator import ChargeCalculator
from backend.services.notification_service import NotificationService

# Créer le blueprint
resident_bp = Blueprint('resident', __name__)


# ==================== DASHBOARD ====================

@resident_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Tableau de bord du résident"""
    try:
        # Demandes de maintenance récentes (filtrées par residence_id et author_id)
        maintenance_requests = MaintenanceRequest.query.filter_by(
            author_id=current_user.id
        ).order_by(MaintenanceRequest.created_at.desc()).limit(5).all()
        
        # Actualités de la résidence (filtrées par residence_id)
        news = []
        if current_user.residence_id:
            news = News.query.filter_by(
                residence_id=current_user.residence_id,
                is_published=True
            ).order_by(News.published_at.desc()).limit(5).all()
        
        # Solde du compte (vérifié unit_id ownership)
        balance = None
        if current_user.unit_id:
            balance = ChargeCalculator.get_unit_balance(current_user.unit_id)
        
        # Assemblées générales à venir (filtrées par residence_id)
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
        
        # SÉCURISÉ: Filtre par residence_id
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
        
        # SÉCURITÉ: Vérifier que l'actualité appartient à la résidence de l'utilisateur
        if not news:
            return jsonify({'success': False, 'error': 'Actualité non trouvée'}), 404
        
        if news.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        return jsonify({'success': True, 'news': news.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== MAINTENANCE ====================

@resident_bp.route('/maintenance', methods=['POST'])
@login_required
def create_maintenance_request():
    """Crée une nouvelle demande de maintenance"""
    import os
    from werkzeug.utils import secure_filename
    
    try:
        # Gérer les données multipart/form-data pour l'upload d'images
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = request.form.to_dict()
            image_file = request.files.get('image')
        else:
            data = request.get_json()
            image_file = None
        
        # Validation
        required_fields = ['title', 'description', 'zone']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # SÉCURITÉ: Vérifier que l'utilisateur a une résidence
        if not current_user.residence_id:
            return jsonify({'success': False, 'error': 'Vous devez être associé à une résidence'}), 400
        
        # Gérer l'upload d'image
        image_path = None
        if image_file and image_file.filename:
            # Créer le dossier uploads si nécessaire
            upload_folder = os.path.join('frontend', 'static', 'uploads', 'maintenance')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Sécuriser le nom de fichier
            filename = secure_filename(image_file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Sauvegarder le fichier
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)
            image_path = f"/static/uploads/maintenance/{filename}"
        
        # Générer un numéro de suivi unique
        tracking_number = MaintenanceRequest.generate_tracking_number(current_user.residence_id)
        
        # SÉCURITÉ: Utiliser residence_id et author_id de current_user (pas de la requête)
        maintenance_request = MaintenanceRequest(
            tracking_number=tracking_number,
            request_type='resident_request',
            residence_id=current_user.residence_id,
            author_id=current_user.id,
            zone=data['zone'],
            zone_details=data.get('zone_details'),
            title=data['title'],
            description=data['description'],
            priority=data.get('priority', 'medium'),
            image_path=image_path
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
        # SÉCURISÉ: Filtre par author_id
        requests = MaintenanceRequest.query.filter_by(
            author_id=current_user.id
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
        
        # SÉCURITÉ: Vérifier ownership
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        if maintenance_request.author_id != current_user.id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        return jsonify({'success': True, 'maintenance_request': maintenance_request.to_dict(include_relations=True)}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== COMMENTAIRES MAINTENANCE (RÉSIDENT) ====================

@resident_bp.route('/maintenance/<int:request_id>/comments', methods=['GET'])
@login_required
def get_resident_maintenance_comments(request_id):
    """Récupère les commentaires d'une demande de maintenance (non-internes uniquement)"""
    try:
        from backend.models.maintenance_comment import MaintenanceComment
        
        # Vérifier que la demande existe et appartient à l'utilisateur
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        if maintenance_request.author_id != current_user.id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        # Récupérer les commentaires non-internes
        comments = MaintenanceComment.query.filter_by(
            maintenance_request_id=request_id,
            is_internal=False
        ).order_by(MaintenanceComment.created_at).all()
        
        return jsonify({
            'success': True,
            'comments': [c.to_dict() for c in comments]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/maintenance/<int:request_id>/comments', methods=['POST'])
@login_required
def add_resident_maintenance_comment(request_id):
    """Ajoute un commentaire à une demande de maintenance"""
    try:
        from backend.models.maintenance_comment import MaintenanceComment
        
        # Vérifier que la demande existe et appartient à l'utilisateur
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        if maintenance_request.author_id != current_user.id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        data = request.get_json()
        
        if 'comment_text' not in data or not data['comment_text'].strip():
            return jsonify({'success': False, 'error': 'Le commentaire ne peut pas être vide'}), 400
        
        # Créer le commentaire (toujours non-interne pour les résidents)
        comment = MaintenanceComment(
            maintenance_request_id=request_id,
            author_id=current_user.id,
            comment_text=data['comment_text'],
            comment_type='comment',
            is_internal=False
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Notifier les admins
        NotificationService.notify_new_maintenance_comment(comment)
        
        return jsonify({
            'success': True,
            'message': 'Commentaire ajouté',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== DOCUMENTS MAINTENANCE (RÉSIDENT) ====================

@resident_bp.route('/maintenance/<int:request_id>/documents', methods=['GET'])
@login_required
def get_resident_maintenance_documents(request_id):
    """Récupère les documents d'une demande de maintenance"""
    try:
        from backend.models.maintenance_document import MaintenanceDocument
        
        # Vérifier que la demande existe et appartient à l'utilisateur
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'error': 'Demande non trouvée'}), 404
        
        if maintenance_request.author_id != current_user.id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
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


# ==================== CHARGES ET PAIEMENTS ====================

@resident_bp.route('/charges', methods=['GET'])
@login_required
def get_my_charges():
    """Récupère les charges du résident"""
    try:
        # SÉCURITÉ: Vérifier unit_id
        if not current_user.unit_id:
            return jsonify({'success': True, 'charges': [], 'message': 'Aucun lot associé'}), 200
        
        # SÉCURISÉ: Filtre par unit_id de l'utilisateur
        distributions = ChargeDistribution.query.filter_by(unit_id=current_user.unit_id).all()
        
        charges_data = []
        for dist in distributions:
            # SÉCURITÉ: Vérifier que la charge appartient à la même résidence
            if dist.charge.residence_id == current_user.residence_id:
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
        # SÉCURITÉ: Vérifier unit_id
        if not current_user.unit_id:
            return jsonify({'success': True, 'unpaid_charges': []}), 200
        
        # SÉCURISÉ: ChargeCalculator utilise unit_id
        unpaid = ChargeCalculator.get_unpaid_charges(current_user.unit_id)
        
        return jsonify({'success': True, 'unpaid_charges': unpaid}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/balance', methods=['GET'])
@login_required
def get_balance():
    """Récupère le solde du compte"""
    try:
        # SÉCURITÉ: Vérifier unit_id
        if not current_user.unit_id:
            return jsonify({'success': False, 'error': 'Aucun lot associé'}), 400
        
        # SÉCURISÉ: ChargeCalculator utilise unit_id
        balance = ChargeCalculator.get_unit_balance(current_user.unit_id)
        
        return jsonify({'success': True, 'balance': balance}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@resident_bp.route('/payments', methods=['POST'])
@login_required
def declare_payment():
    """Déclare un paiement"""
    try:
        # SÉCURITÉ: Vérifier unit_id
        if not current_user.unit_id:
            return jsonify({'success': False, 'error': 'Aucun lot associé'}), 400
        
        data = request.get_json()
        required_fields = ['amount', 'payment_method', 'payment_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Le champ {field} est requis'}), 400
        
        # SÉCURITÉ: Utiliser unit_id et user_id de current_user (pas de la requête)
        payment = Payment(
            unit_id=current_user.unit_id,  # Dérivé de l'utilisateur authentifié
            user_id=current_user.id,  # Dérivé de l'utilisateur authentifié
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
        # SÉCURISÉ: Filtre par user_id
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
        
        # SÉCURISÉ: Filtre par residence_id et is_public
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
        
        # SÉCURITÉ: Vérifier residence_id et is_public
        if not document:
            return jsonify({'success': False, 'error': 'Document non trouvé'}), 404
        
        if document.residence_id != current_user.residence_id or not document.is_public:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
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
        
        # SÉCURISÉ: Filtre par residence_id
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
        
        # SÉCURITÉ: Vérifier residence_id
        if not poll:
            return jsonify({'success': False, 'error': 'Sondage non trouvé'}), 404
        
        if poll.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
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
        
        # SÉCURITÉ: Vérifier residence_id
        if not poll:
            return jsonify({'success': False, 'error': 'Sondage non trouvé'}), 404
        
        if poll.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        if poll.status != 'active':
            return jsonify({'success': False, 'error': 'Ce sondage n\'est plus actif'}), 400
        
        data = request.get_json()
        option_id = data.get('option_id')
        
        if not option_id:
            return jsonify({'success': False, 'error': 'Option requise'}), 400
        
        # SÉCURITÉ: Vérifier que l'option appartient à ce sondage
        option = PollOption.query.get(option_id)
        if not option or option.poll_id != poll_id:
            return jsonify({'success': False, 'error': 'Option invalide'}), 400
        
        # Vérifier si l'utilisateur a déjà voté
        existing_vote = PollVote.query.filter_by(poll_id=poll_id, user_id=current_user.id).first()
        if existing_vote and not poll.allow_multiple:
            return jsonify({'success': False, 'error': 'Vous avez déjà voté'}), 400
        
        # SÉCURITÉ: Enregistrer le vote avec user_id de current_user
        vote = PollVote(
            poll_id=poll_id,
            option_id=option_id,
            user_id=current_user.id  # Dérivé de l'utilisateur authentifié
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
        
        # SÉCURISÉ: Filtre par residence_id
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
        
        # SÉCURITÉ: Vérifier residence_id
        if not assembly:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        if assembly.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
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
        
        # SÉCURITÉ: Vérifier residence_id
        if not assembly:
            return jsonify({'success': False, 'error': 'AG non trouvée'}), 404
        
        if assembly.residence_id != current_user.residence_id:
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        # Vérifier si déjà enregistré
        attendance = Attendance.query.filter_by(assembly_id=assembly_id, user_id=current_user.id).first()
        
        if attendance:
            attendance.is_present = True
        else:
            # SÉCURITÉ: Utiliser user_id de current_user
            attendance = Attendance(
                assembly_id=assembly_id,
                user_id=current_user.id,  # Dérivé de l'utilisateur authentifié
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
        
        # SÉCURITÉ: Vérifier que l'utilisateur appartient à la résidence de l'AG
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
            # SÉCURITÉ: Créer un nouveau vote avec user_id de current_user
            vote = Vote(
                resolution_id=resolution_id,
                user_id=current_user.id,  # Dérivé de l'utilisateur authentifié
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
        
        # SÉCURISÉ: Filtre par residence_id
        logs = MaintenanceLog.query.filter_by(
            residence_id=current_user.residence_id
        ).order_by(MaintenanceLog.intervention_date.desc()).limit(50).all()
        
        return jsonify({'success': True, 'logs': [l.to_dict() for l in logs]}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
