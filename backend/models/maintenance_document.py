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


class MaintenanceDocument(db.Model):
    """
    Modèle pour les documents joints aux demandes de maintenance
    (changelog, factures, devis, photos supplémentaires, etc.)
    """
    
    __tablename__ = 'maintenance_documents'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la demande de maintenance
    maintenance_request_id = db.Column(db.Integer, db.ForeignKey('maintenance_requests.id'), nullable=False)
    
    # Type de document
    document_type = db.Column(db.String(50), nullable=False)  # 'changelog', 'invoice', 'quote', 'photo', 'report', 'other'
    
    # Informations du document
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Fichier
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # Taille en octets
    mime_type = db.Column(db.String(100))
    
    # Auteur de l'upload
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref='uploaded_maintenance_documents', lazy=True)
    
    def to_dict(self):
        """Convertit le document en dictionnaire"""
        result = {
            'id': self.id,
            'maintenance_request_id': self.maintenance_request_id,
            'document_type': self.document_type,
            'title': self.title,
            'description': self.description,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Ajouter les informations de l'uploader
        if self.uploader:
            result['uploader_name'] = f"{self.uploader.first_name} {self.uploader.last_name}"
            result['uploader_role'] = self.uploader.role
        else:
            result['uploader_name'] = None
            result['uploader_role'] = None
        
        return result
    
    def __repr__(self):
        return f'<MaintenanceDocument {self.title} - {self.document_type}>'
