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


class Poll(db.Model):
    """
    Modèle pour les sondages
    """
    
    __tablename__ = 'polls'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Contenu du sondage
    question = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    
    # Paramètres
    allow_multiple = db.Column(db.Boolean, default=False)  # Vote multiple autorisé
    is_anonymous = db.Column(db.Boolean, default=False)
    
    # Dates
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime)
    
    # Statut
    status = db.Column(db.String(20), default='active')
    # Statuts: 'draft', 'active', 'closed'
    
    # Auteur
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    options = db.relationship('PollOption', backref='poll', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('PollVote', backref='poll', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('User', backref='created_polls', lazy=True)
    
    def get_results(self):
        """Calcule les résultats du sondage"""
        results = []
        total_votes = len(self.votes)
        
        for option in self.options:
            vote_count = len(option.votes)
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            
            results.append({
                'option_id': option.id,
                'option_text': option.option_text,
                'votes': vote_count,
                'percentage': round(percentage, 2)
            })
        
        return {
            'poll_id': self.id,
            'question': self.question,
            'total_votes': total_votes,
            'options': results
        }
    
    def to_dict(self):
        """Convertit le sondage en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'question': self.question,
            'description': self.description,
            'allow_multiple': self.allow_multiple,
            'is_anonymous': self.is_anonymous,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Poll {self.question}>'


class PollOption(db.Model):
    """
    Modèle pour les options d'un sondage
    """
    
    __tablename__ = 'poll_options'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence au sondage
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    
    # Texte de l'option
    option_text = db.Column(db.String(200), nullable=False)
    
    # Ordre d'affichage
    order = db.Column(db.Integer, default=0)
    
    # Relations
    votes = db.relationship('PollVote', backref='option', lazy=True)
    
    def to_dict(self):
        """Convertit l'option en dictionnaire"""
        return {
            'id': self.id,
            'poll_id': self.poll_id,
            'option_text': self.option_text,
            'order': self.order,
            'vote_count': len(self.votes)
        }
    
    def __repr__(self):
        return f'<PollOption {self.option_text}>'


class PollVote(db.Model):
    """
    Modèle pour les votes des résidents
    """
    
    __tablename__ = 'poll_votes'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Références
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_options.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Métadonnées
    voted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Contrainte d'unicité: un utilisateur ne peut voter qu'une fois (sauf vote multiple)
    __table_args__ = (
        db.UniqueConstraint('poll_id', 'user_id', 'option_id', name='unique_vote'),
    )
    
    def to_dict(self):
        """Convertit le vote en dictionnaire"""
        return {
            'id': self.id,
            'poll_id': self.poll_id,
            'option_id': self.option_id,
            'user_id': self.user_id,
            'voted_at': self.voted_at.isoformat() if self.voted_at else None
        }
    
    def __repr__(self):
        return f'<PollVote Poll:{self.poll_id} User:{self.user_id}>'
