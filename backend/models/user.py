#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Modèle Utilisateur
Gestion des utilisateurs (Superadmin et Résidents)

Date: 24 octobre 2025
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from backend.models import db


class User(UserMixin, db.Model):
    """
    Modèle utilisateur pour l'authentification et la gestion des rôles
    """
    
    __tablename__ = 'users'
    
    # Identifiant
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations personnelles
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    
    # Rôle : 'superadmin', 'admin' (bureau syndic), 'owner' (propriétaire), 'resident' (résident)
    role = db.Column(db.String(20), nullable=False, default='resident')
    
    # Statut du compte
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relation avec la résidence (pour les résidents)
    residence_id = db.Column(db.Integer, db.ForeignKey('residences.id'), nullable=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relations
    residence = db.relationship('Residence', backref='residents', lazy=True)
    unit = db.relationship('Unit', backref='resident', lazy=True)
    maintenance_requests = db.relationship('MaintenanceRequest', backref='requester', lazy=True)
    poll_votes = db.relationship('PollVote', backref='voter', lazy=True)
    
    def set_password(self, password):
        """
        Hash et stocke le mot de passe
        
        Args:
            password (str): Mot de passe en clair
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Vérifie si le mot de passe est correct
        
        Args:
            password (str): Mot de passe à vérifier
            
        Returns:
            bool: True si le mot de passe est correct
        """
        return check_password_hash(self.password_hash, password)
    
    def is_superadmin(self):
        """Vérifie si l'utilisateur est un superadmin"""
        return self.role == 'superadmin'
    
    def is_admin(self):
        """Vérifie si l'utilisateur est un administrateur (bureau syndic)"""
        return self.role == 'admin'
    
    def is_owner(self):
        """Vérifie si l'utilisateur est un propriétaire"""
        return self.role == 'owner'
    
    def is_resident(self):
        """Vérifie si l'utilisateur est un résident"""
        return self.role == 'resident'
    
    def has_admin_rights(self):
        """Vérifie si l'utilisateur a des droits d'administration (superadmin ou admin)"""
        return self.role in ['superadmin', 'admin']
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        """
        Convertit l'utilisateur en dictionnaire (pour JSON)
        
        Returns:
            dict: Données de l'utilisateur
        """
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'residence_id': self.residence_id,
            'unit_id': self.unit_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
