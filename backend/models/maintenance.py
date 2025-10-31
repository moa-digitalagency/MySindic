#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Solution complète et digitale pour les syndics et résidents au Maroc.

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
    assigned_to = db.Column(db.String(200))  # Nom du technicien/prestataire
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
    author = db.relationship('User', backref='maintenance_requests', lazy=True)
    
    def to_dict(self):
        """Convertit la demande en dictionnaire"""
        from backend.models.residence import Residence
        
        result = {
            'id': self.id,
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
        
        return result
    
    def __repr__(self):
        return f'<MaintenanceRequest {self.title} - {self.status}>'
