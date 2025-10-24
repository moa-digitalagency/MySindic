#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Modèles Charges
Gestion des charges et de leur répartition

Date: 24 octobre 2025
"""

from datetime import datetime
from backend.models import db


class Charge(db.Model):
    """
    Modèle pour les charges de la résidence
    """
    
    __tablename__ = 'charges'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Informations de la charge
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Type de charge
    charge_type = db.Column(db.String(50), nullable=False)
    # Types: 'courante', 'exceptionnelle', 'travaux', 'assurance', etc.
    
    # Montant total
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Période concernée
    period_month = db.Column(db.Integer)  # 1-12
    period_year = db.Column(db.Integer, nullable=False)
    
    # Statut
    status = db.Column(db.String(20), default='draft')
    # Statuts: 'draft', 'published', 'closed'
    
    # Dates
    due_date = db.Column(db.DateTime)  # Date limite de paiement
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    distributions = db.relationship('ChargeDistribution', backref='charge', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertit la charge en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'title': self.title,
            'description': self.description,
            'charge_type': self.charge_type,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'period_month': self.period_month,
            'period_year': self.period_year,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Charge {self.title}>'


class ChargeDistribution(db.Model):
    """
    Modèle pour la répartition des charges par lot
    """
    
    __tablename__ = 'charge_distributions'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Références
    charge_id = db.Column(db.Integer, db.ForeignKey('charges.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    
    # Montant calculé pour ce lot
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Statut de paiement
    is_paid = db.Column(db.Boolean, default=False)
    paid_date = db.Column(db.DateTime)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertit la distribution en dictionnaire"""
        return {
            'id': self.id,
            'charge_id': self.charge_id,
            'unit_id': self.unit_id,
            'amount': float(self.amount) if self.amount else 0,
            'is_paid': self.is_paid,
            'paid_date': self.paid_date.isoformat() if self.paid_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ChargeDistribution Charge:{self.charge_id} Unit:{self.unit_id}>'
