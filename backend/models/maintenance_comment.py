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


class MaintenanceComment(db.Model):
    """
    Modèle pour les commentaires sur les demandes de maintenance
    Permet la communication entre résidents et administrateurs
    """
    
    __tablename__ = 'maintenance_comments'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la demande de maintenance
    maintenance_request_id = db.Column(db.Integer, db.ForeignKey('maintenance_requests.id'), nullable=False)
    
    # Auteur du commentaire
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Contenu du commentaire
    comment_text = db.Column(db.Text, nullable=False)
    
    # Type de commentaire
    comment_type = db.Column(db.String(50), default='comment')  # 'comment', 'status_update', 'mention'
    
    # Utilisateur mentionné (optionnel pour tagging)
    mentioned_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Visibilité
    is_internal = db.Column(db.Boolean, default=False)  # True = visible seulement pour admins
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    author = db.relationship('User', foreign_keys=[author_id], backref='maintenance_comments', lazy=True)
    mentioned_user = db.relationship('User', foreign_keys=[mentioned_user_id], backref='mentioned_in_comments', lazy=True)
    
    def to_dict(self):
        """Convertit le commentaire en dictionnaire"""
        result = {
            'id': self.id,
            'maintenance_request_id': self.maintenance_request_id,
            'author_id': self.author_id,
            'comment_text': self.comment_text,
            'comment_type': self.comment_type,
            'mentioned_user_id': self.mentioned_user_id,
            'is_internal': self.is_internal,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Ajouter les informations de l'auteur
        if self.author:
            result['author_name'] = f"{self.author.first_name} {self.author.last_name}"
            result['author_role'] = self.author.role
        else:
            result['author_name'] = None
            result['author_role'] = None
        
        # Ajouter les informations de l'utilisateur mentionné
        if self.mentioned_user:
            result['mentioned_user_name'] = f"{self.mentioned_user.first_name} {self.mentioned_user.last_name}"
        else:
            result['mentioned_user_name'] = None
        
        return result
    
    def __repr__(self):
        return f'<MaintenanceComment {self.id} by User {self.author_id}>'
