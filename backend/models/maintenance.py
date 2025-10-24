#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Modèle Demandes de Maintenance
Gestion des demandes d'intervention des résidents

Date: 24 octobre 2025
"""

from datetime import datetime
from backend.models import db


class MaintenanceRequest(db.Model):
    """
    Modèle pour les demandes de maintenance des résidents
    """
    
    __tablename__ = 'maintenance_requests'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Références
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Informations de la demande
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # Ex: "Plomberie", "Électricité", "Ascenseur", etc.
    location = db.Column(db.String(200))  # Localisation précise dans la résidence
    
    # Priorité
    priority = db.Column(db.String(20), default='normal')  # 'low', 'normal', 'high', 'urgent'
    
    # Statut
    status = db.Column(db.String(20), default='pending')
    # Statuts possibles: 'pending', 'in_progress', 'completed', 'cancelled'
    
    # Intervenant assigné
    assigned_to = db.Column(db.String(200))  # Nom du technicien/prestataire
    assigned_at = db.Column(db.DateTime)
    
    # Dates
    scheduled_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Notes et commentaires
    admin_notes = db.Column(db.Text)
    resolution_notes = db.Column(db.Text)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertit la demande en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'requester_id': self.requester_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'location': self.location,
            'priority': self.priority,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'admin_notes': self.admin_notes,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MaintenanceRequest {self.id}: {self.title} ({self.status})>'
