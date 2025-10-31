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


class Document(db.Model):
    """
    Modèle pour les documents de la résidence
    """
    
    __tablename__ = 'documents'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Informations du document
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Type de document
    document_type = db.Column(db.String(50), nullable=False)
    # Types: 'quittance', 'pv_ag', 'appel_fonds', 'reglement', 'autre'
    
    # Fichier
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # Taille en bytes
    mime_type = db.Column(db.String(100))
    
    # Visibilité
    is_public = db.Column(db.Boolean, default=False)  # Visible par tous les résidents
    
    # Dates
    document_date = db.Column(db.DateTime)  # Date du document (ex: date de l'AG)
    
    # Métadonnées
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertit le document en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'title': self.title,
            'description': self.description,
            'document_type': self.document_type,
            'filename': self.filename,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'is_public': self.is_public,
            'document_date': self.document_date.isoformat() if self.document_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Document {self.title}>'
