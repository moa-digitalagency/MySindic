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


class Residence(db.Model):
    """
    Modèle pour les résidences/copropriétés
    """
    
    __tablename__ = 'residences'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations de la résidence
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='Maroc')
    
    # Détails
    description = db.Column(db.Text)
    total_units = db.Column(db.Integer, nullable=False)
    
    # Contact syndic
    syndic_name = db.Column(db.String(200))
    syndic_email = db.Column(db.String(120))
    syndic_phone = db.Column(db.String(20))
    
    
    # Statut
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    units = db.relationship('Unit', backref='residence', lazy=True, cascade='all, delete-orphan')
    maintenance_requests = db.relationship('MaintenanceRequest', backref='residence', lazy=True)
    documents = db.relationship('Document', backref='residence', lazy=True)
    news = db.relationship('News', backref='residence', lazy=True)
    polls = db.relationship('Poll', backref='residence', lazy=True)
    charges = db.relationship('Charge', backref='residence', lazy=True)
    
    def to_dict(self):
        """Convertit la résidence en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country,
            'description': self.description,
            'total_units': self.total_units,
            'syndic_name': self.syndic_name,
            'syndic_email': self.syndic_email,
            'syndic_phone': self.syndic_phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Residence {self.name}>'


class Unit(db.Model):
    """
    Modèle pour les lots/appartements d'une résidence
    """
    
    __tablename__ = 'units'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Informations du lot
    unit_number = db.Column(db.String(50), nullable=False)  # Ex: "A101", "B205"
    floor = db.Column(db.Integer)
    building = db.Column(db.String(50))  # Ex: "Bâtiment A"
    
    # Type de lot
    unit_type = db.Column(db.String(50))  # Ex: "Appartement", "Commerce", "Parking"
    
    # Superficie
    surface_area = db.Column(db.Float)  # en m²
    
    # Propriétaire
    owner_name = db.Column(db.String(200))
    owner_email = db.Column(db.String(120))
    owner_phone = db.Column(db.String(20))
    
    # Statut
    is_occupied = db.Column(db.Boolean, default=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    charge_distributions = db.relationship('ChargeDistribution', backref='unit', lazy=True)
    payments = db.relationship('Payment', backref='unit', lazy=True)
    
    def to_dict(self):
        """Convertit le lot en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'unit_number': self.unit_number,
            'floor': self.floor,
            'building': self.building,
            'unit_type': self.unit_type,
            'surface_area': self.surface_area,
            'owner_name': self.owner_name,
            'owner_email': self.owner_email,
            'owner_phone': self.owner_phone,
            'is_occupied': self.is_occupied,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Unit {self.unit_number}>'
