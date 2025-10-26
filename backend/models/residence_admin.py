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


class ResidenceAdmin(db.Model):
    """
    Modèle d'association pour les administrateurs assignés aux résidences
    Permet à plusieurs admins de gérer plusieurs résidences
    """
    
    __tablename__ = 'residence_admins'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Relations
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Métadonnées
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Contrainte unique: un admin ne peut être assigné qu'une fois à une résidence
    __table_args__ = (
        db.UniqueConstraint('residence_id', 'user_id', name='unique_residence_admin'),
    )
    
    def to_dict(self):
        """Convertit l'assignation en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'user_id': self.user_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }
    
    def __repr__(self):
        return f'<ResidenceAdmin residence_id={self.residence_id} user_id={self.user_id}>'
