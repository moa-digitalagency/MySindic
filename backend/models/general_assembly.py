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


class GeneralAssembly(db.Model):
    """
    Modèle pour les assemblées générales (AG)
    """
    
    __tablename__ = 'general_assemblies'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à la résidence
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=False)
    
    # Informations de l'AG
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Type d'AG
    assembly_type = db.Column(db.String(50), nullable=False)
    # Types: 'ordinaire', 'extraordinaire'
    
    # Dates
    scheduled_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    
    # Lieu
    location = db.Column(db.String(200))
    
    # Statut
    status = db.Column(db.String(20), default='planned')
    # Statuts: 'planned', 'in_progress', 'completed', 'cancelled'
    
    # Documents
    convocation_sent = db.Column(db.Boolean, default=False)
    convocation_sent_date = db.Column(db.DateTime)
    
    # Procès-verbal
    minutes_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
    
    # Quorum
    quorum_required = db.Column(db.Integer, default=50)  # Pourcentage
    quorum_reached = db.Column(db.Boolean, default=False)
    
    # Métadonnées
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    resolutions = db.relationship('Resolution', backref='assembly', lazy=True, cascade='all, delete-orphan')
    attendances = db.relationship('Attendance', backref='assembly', lazy=True, cascade='all, delete-orphan')
    residence = db.relationship('Residence', backref='assemblies')
    creator = db.relationship('User', backref='created_assemblies')
    
    def to_dict(self):
        """Convertit l'AG en dictionnaire"""
        return {
            'id': self.id,
            'residence_id': self.residence_id,
            'title': self.title,
            'description': self.description,
            'assembly_type': self.assembly_type,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'status': self.status,
            'convocation_sent': self.convocation_sent,
            'convocation_sent_date': self.convocation_sent_date.isoformat() if self.convocation_sent_date else None,
            'quorum_required': self.quorum_required,
            'quorum_reached': self.quorum_reached,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<GeneralAssembly {self.title}>'


class Resolution(db.Model):
    """
    Modèle pour les résolutions/votes d'une AG
    """
    
    __tablename__ = 'resolutions'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Référence à l'AG
    assembly_id = db.Column(db.Integer, db.ForeignKey('general_assemblies.id'), nullable=False)
    
    # Informations de la résolution
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Ordre dans l'ordre du jour
    order = db.Column(db.Integer, default=0)
    
    # Type de vote
    vote_type = db.Column(db.String(50), default='simple')
    # Types: 'simple', 'double_majorite', 'unanimite'
    
    # Résultats
    votes_for = db.Column(db.Integer, default=0)
    votes_against = db.Column(db.Integer, default=0)
    votes_abstain = db.Column(db.Integer, default=0)
    
    # Statut
    status = db.Column(db.String(20), default='pending')
    # Statuts: 'pending', 'voting', 'approved', 'rejected'
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    votes = db.relationship('Vote', backref='resolution', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertit la résolution en dictionnaire"""
        return {
            'id': self.id,
            'assembly_id': self.assembly_id,
            'title': self.title,
            'description': self.description,
            'order': self.order,
            'vote_type': self.vote_type,
            'votes_for': self.votes_for,
            'votes_against': self.votes_against,
            'votes_abstain': self.votes_abstain,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Resolution {self.title}>'


class Vote(db.Model):
    """
    Modèle pour les votes sur les résolutions
    """
    
    __tablename__ = 'votes'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Références
    resolution_id = db.Column(db.Integer, db.ForeignKey('resolutions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Vote
    vote_value = db.Column(db.String(20), nullable=False)
    # Valeurs: 'for', 'against', 'abstain'
    
    # Métadonnées
    voted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Contrainte d'unicité
    __table_args__ = (
        db.UniqueConstraint('resolution_id', 'user_id', name='unique_resolution_vote'),
    )
    
    def to_dict(self):
        """Convertit le vote en dictionnaire"""
        return {
            'id': self.id,
            'resolution_id': self.resolution_id,
            'user_id': self.user_id,
            'vote_value': self.vote_value,
            'voted_at': self.voted_at.isoformat() if self.voted_at else None
        }
    
    def __repr__(self):
        return f'<Vote Resolution:{self.resolution_id} User:{self.user_id}>'


class Attendance(db.Model):
    """
    Modèle pour les présences/absences aux AG
    """
    
    __tablename__ = 'attendances'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Références
    assembly_id = db.Column(db.Integer, db.ForeignKey('general_assemblies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Présence
    is_present = db.Column(db.Boolean, default=False)
    represented_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Représentant
    
    # Métadonnées
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convertit la présence en dictionnaire"""
        return {
            'id': self.id,
            'assembly_id': self.assembly_id,
            'user_id': self.user_id,
            'is_present': self.is_present,
            'represented_by': self.represented_by,
            'registered_at': self.registered_at.isoformat() if self.registered_at else None
        }
    
    def __repr__(self):
        return f'<Attendance Assembly:{self.assembly_id} User:{self.user_id}>'
