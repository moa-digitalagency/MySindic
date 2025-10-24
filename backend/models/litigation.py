#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Modèle Contentieux
Gestion des litiges et procédures contentieuses

Date: 24 octobre 2025
"""

from datetime import datetime
from backend.models import db


class Litigation(db.Model):
    """
    Modèle pour les contentieux/litiges
    """
    
    __tablename__ = 'litigations'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Partie adverse (résident ou externe)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))  # Si c'est un résident
    party_name = db.Column(db.String(200))  # Nom de la partie adverse
    party_contact = db.Column(db.String(200))
    
    # Informations du litige
    reference_number = db.Column(db.String(100), unique=True)  # Numéro de dossier
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Type de contentieux
    litigation_type = db.Column(db.String(50), nullable=False)
    # Types: 'impaye', 'nuisance', 'travaux', 'autre'
    
    # Montant en jeu (si applicable)
    amount = db.Column(db.Numeric(10, 2))
    
    # Statut
    status = db.Column(db.String(20), default='open')
    # Statuts: 'open', 'in_progress', 'settled', 'closed', 'won', 'lost'
    
    # Dates importantes
    start_date = db.Column(db.DateTime, nullable=False)
    hearing_date = db.Column(db.DateTime)
    resolution_date = db.Column(db.DateTime)
    
    # Avocat/Représentant
    lawyer_name = db.Column(db.String(200))
    lawyer_contact = db.Column(db.String(200))
    
    # Notes et résultat
    notes = db.Column(db.Text)
    resolution_notes = db.Column(db.Text)
    
    # Métadonnées
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    residence = db.relationship('Residence', backref='litigations')
    unit = db.relationship('Unit', backref='litigations')
    creator = db.relationship('User', backref='created_litigations')
    
    def to_dict(self):
        """Convertit le contentieux en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'unit_id': self.unit_id,
            'party_name': self.party_name,
            'party_contact': self.party_contact,
            'reference_number': self.reference_number,
            'title': self.title,
            'description': self.description,
            'litigation_type': self.litigation_type,
            'amount': float(self.amount) if self.amount else None,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'hearing_date': self.hearing_date.isoformat() if self.hearing_date else None,
            'resolution_date': self.resolution_date.isoformat() if self.resolution_date else None,
            'lawyer_name': self.lawyer_name,
            'lawyer_contact': self.lawyer_contact,
            'notes': self.notes,
            'resolution_notes': self.resolution_notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Litigation {self.reference_number}: {self.title}>'
