#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Modèle Permission
Gestion des permissions par rôle

Date: 26 octobre 2025
"""

from backend.models import db
from datetime import datetime


class RolePermission(db.Model):
    """
    Modèle pour stocker les permissions par rôle
    
    Chaque enregistrement représente une permission accordée à un rôle spécifique
    pour accéder à une ressource ou effectuer une action.
    """
    __tablename__ = 'role_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Rôle concerné
    role = db.Column(db.String(20), nullable=False, index=True)
    
    # Ressource/fonctionnalité concernée
    resource = db.Column(db.String(50), nullable=False)
    
    # Action autorisée (read, write, delete, manage, etc.)
    action = db.Column(db.String(20), nullable=False)
    
    # Permission accordée ou non
    is_allowed = db.Column(db.Boolean, default=True, nullable=False)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Index composite pour éviter les doublons
    __table_args__ = (
        db.UniqueConstraint('role', 'resource', 'action', name='unique_role_resource_action'),
    )
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'role': self.role,
            'resource': self.resource,
            'action': self.action,
            'is_allowed': self.is_allowed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_role_permissions(role):
        """Récupère toutes les permissions pour un rôle"""
        return RolePermission.query.filter_by(role=role, is_allowed=True).all()
    
    @staticmethod
    def has_permission(role, resource, action='read'):
        """Vérifie si un rôle a une permission spécifique"""
        permission = RolePermission.query.filter_by(
            role=role,
            resource=resource,
            action=action,
            is_allowed=True
        ).first()
        
        return permission is not None
    
    @staticmethod
    def set_permission(role, resource, action, is_allowed=True, user_id=None):
        """Définit une permission pour un rôle"""
        permission = RolePermission.query.filter_by(
            role=role,
            resource=resource,
            action=action
        ).first()
        
        if permission:
            permission.is_allowed = is_allowed
            permission.updated_at = datetime.utcnow()
        else:
            permission = RolePermission(
                role=role,
                resource=resource,
                action=action,
                is_allowed=is_allowed,
                created_by=user_id
            )
            db.session.add(permission)
        
        return permission
    
    def __repr__(self):
        return f'<RolePermission {self.role}:{self.resource}:{self.action}={self.is_allowed}>'
