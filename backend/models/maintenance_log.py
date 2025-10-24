#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Modèle Carnet d'Entretien
Historique complet de toutes les interventions

Date: 24 octobre 2025
"""

from datetime import datetime
from backend.models import db


class MaintenanceLog(db.Model):
    """
    Modèle pour le carnet d'entretien (historique des interventions)
    """
    
    __tablename__ = 'maintenance_logs'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Lien avec une demande de maintenance (si applicable)
    maintenance_request_id = db.Column(db.Integer, db.ForeignKey('maintenance_requests.id'))
    
    # Informations de l'intervention
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Type d'intervention
    intervention_type = db.Column(db.String(50), nullable=False)
    # Types: 'maintenance_preventive', 'maintenance_corrective', 'reparation', 'controle', 'autre'
    
    # Catégorie
    category = db.Column(db.String(50))
    # Categories: 'plomberie', 'electricite', 'chauffage', 'ascenseur', 'toiture', 'facade', 'autre'
    
    # Lieu de l'intervention
    location = db.Column(db.String(200))
    
    # Intervenant
    contractor_name = db.Column(db.String(200), nullable=False)
    contractor_contact = db.Column(db.String(200))
    
    # Dates
    intervention_date = db.Column(db.DateTime, nullable=False)
    next_intervention_date = db.Column(db.DateTime)  # Pour la maintenance préventive
    
    # Coûts
    cost = db.Column(db.Numeric(10, 2))
    invoice_number = db.Column(db.String(100))
    
    # Documents associés
    documents = db.Column(db.Text)  # JSON avec les IDs des documents
    photos = db.Column(db.Text)  # JSON avec les chemins des photos
    
    # Garantie
    warranty_end_date = db.Column(db.DateTime)
    
    # Notes
    notes = db.Column(db.Text)
    
    # Métadonnées
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    residence = db.relationship('Residence', backref='maintenance_logs')
    maintenance_request = db.relationship('MaintenanceRequest', backref='logs')
    creator = db.relationship('User', backref='created_logs')
    
    def to_dict(self):
        """Convertit l'entrée du carnet en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'maintenance_request_id': self.maintenance_request_id,
            'title': self.title,
            'description': self.description,
            'intervention_type': self.intervention_type,
            'category': self.category,
            'location': self.location,
            'contractor_name': self.contractor_name,
            'contractor_contact': self.contractor_contact,
            'intervention_date': self.intervention_date.isoformat() if self.intervention_date else None,
            'next_intervention_date': self.next_intervention_date.isoformat() if self.next_intervention_date else None,
            'cost': float(self.cost) if self.cost else None,
            'invoice_number': self.invoice_number,
            'warranty_end_date': self.warranty_end_date.isoformat() if self.warranty_end_date else None,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MaintenanceLog {self.title} - {self.intervention_date}>'
