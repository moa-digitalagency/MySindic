#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from datetime import datetime
from backend.models import db


class MaintenanceRequest(db.Model):
    """
    Modèle pour les demandes de maintenance et annonces de travaux
    """
    
    __tablename__ = 'maintenance_requests'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Numéro de suivi unique
    tracking_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Type de demande
    request_type = db.Column(db.String(50), nullable=False, default='resident_request')  # 'resident_request' ou 'admin_announcement'
    
    # Références
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Zone concernée
    zone = db.Column(db.String(100), nullable=False)  # 'appartement', 'escalier', 'ascenseur', 'parking', 'jardin', 'toiture', 'facade', 'autre'
    zone_details = db.Column(db.String(200))  # Ex: "Appartement 12B", "Escalier du 3ème étage"
    
    # Informations de la demande
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Priorité
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'urgent'
    
    # Statut
    status = db.Column(db.String(20), default='pending')
    # Statuts possibles: 'pending', 'in_progress', 'resolved', 'rejected'
    
    # Image
    image_path = db.Column(db.String(500))
    
    # Intervenant assigné
    assigned_to = db.Column(db.String(200))  # Nom du technicien/prestataire externe
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Admin de résidence assigné
    assigned_at = db.Column(db.DateTime)
    
    # Dates
    scheduled_date = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    
    # Notes et commentaires
    admin_notes = db.Column(db.Text)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    author = db.relationship('User', foreign_keys=[author_id], backref='authored_maintenance_requests', lazy=True)
    assigned_user = db.relationship('User', foreign_keys=[assigned_user_id], backref='assigned_maintenance_requests', lazy=True)
    comments = db.relationship('MaintenanceComment', backref='maintenance_request', lazy=True, cascade='all, delete-orphan', order_by='MaintenanceComment.created_at')
    documents = db.relationship('MaintenanceDocument', backref='maintenance_request', lazy=True, cascade='all, delete-orphan', order_by='MaintenanceDocument.created_at.desc()')
    
    @staticmethod
    def generate_tracking_number(residence_id):
        """Génère un numéro de suivi unique pour une demande"""
        import random
        import string
        year = datetime.utcnow().year
        # Format: MNT-YYYY-RESIDXXXX (ex: MNT-2025-RES001234)
        count = MaintenanceRequest.query.filter_by(residence_id=residence_id).count() + 1
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"MNT-{year}-R{residence_id:03d}{random_suffix}"
    
    def to_dict(self, include_relations=False):
        """Convertit la demande en dictionnaire"""
        from backend.models.residence import Residence
        
        result = {
            'id': self.id,
            'tracking_number': self.tracking_number,
            'request_type': self.request_type,
            'residence_id': self.residence_id,
            'author_id': self.author_id,
            'zone': self.zone,
            'zone_details': self.zone_details,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'image_path': self.image_path,
            'assigned_to': self.assigned_to,
            'assigned_user_id': self.assigned_user_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Ajouter les informations de l'auteur
        if self.author:
            result['author_name'] = f"{self.author.first_name} {self.author.last_name}"
            result['author_role'] = self.author.role
            result['author_email'] = self.author.email
        else:
            result['author_name'] = None
            result['author_role'] = None
            result['author_email'] = None
        
        # Ajouter le nom de la résidence
        residence = Residence.query.get(self.residence_id)
        result['residence_name'] = residence.name if residence else None
        
        # Ajouter les informations de l'utilisateur assigné
        if self.assigned_user:
            result['assigned_user_name'] = f"{self.assigned_user.first_name} {self.assigned_user.last_name}"
            result['assigned_user_email'] = self.assigned_user.email
        else:
            result['assigned_user_name'] = None
            result['assigned_user_email'] = None
        
        # Inclure les relations si demandé
        if include_relations:
            result['comments'] = [c.to_dict() for c in self.comments]
            result['documents'] = [d.to_dict() for d in self.documents]
            result['comments_count'] = len(self.comments)
            result['documents_count'] = len(self.documents)
        
        return result
    
    def __repr__(self):
        return f'<MaintenanceRequest {self.title} - {self.status}>'
