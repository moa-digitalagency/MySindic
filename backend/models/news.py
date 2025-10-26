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


class News(db.Model):
    """
    Modèle pour les actualités et informations de la résidence
    """
    
    __tablename__ = 'news'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Contenu
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Catégorie
    category = db.Column(db.String(50))  # 'info', 'travaux', 'urgent', 'evenement'
    
    # Priorité
    is_important = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)  # Épinglé en haut
    
    # Publication
    is_published = db.Column(db.Boolean, default=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Auteur
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    author = db.relationship('User', backref='news_posts', lazy=True)
    
    def to_dict(self):
        """Convertit l'actualité en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'is_important': self.is_important,
            'is_pinned': self.is_pinned,
            'is_published': self.is_published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'author_id': self.author_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<News {self.title}>'
