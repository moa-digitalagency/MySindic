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


class Payment(db.Model):
    """
    Modèle pour les paiements effectués par les résidents
    """
    
    __tablename__ = 'payments'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Références
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Informations du paiement
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50))  # 'cheque', 'virement', 'especes', 'carte'
    
    # Référence du paiement
    reference = db.Column(db.String(100))  # Numéro de chèque, référence virement, etc.
    
    # Description
    description = db.Column(db.Text)
    
    # Date du paiement
    payment_date = db.Column(db.DateTime, nullable=False)
    
    # Statut
    status = db.Column(db.String(20), default='pending')
    # Statuts: 'pending', 'validated', 'rejected'
    
    # Pièce jointe (justificatif de paiement)
    proof_document = db.Column(db.String(255))  # Chemin vers le fichier (image ou PDF)
    
    # Notes
    admin_notes = db.Column(db.Text)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    user = db.relationship('User', backref='payments', lazy=True)
    
    def to_dict(self):
        """Convertit le paiement en dictionnaire"""
        return {
            'id': self.id,
            'unit_id': self.unit_id,
            'user_id': self.user_id,
            'amount': float(self.amount) if self.amount else 0,
            'payment_method': self.payment_method,
            'reference': self.reference,
            'description': self.description,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'status': self.status,
            'proof_document': self.proof_document,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id}: {self.amount} MAD>'
