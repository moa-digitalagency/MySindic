#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Modèle pour les paramètres de l'application

Stocke les paramètres personnalisés de l'application
incluant le code <head> personnalisé
"""

from backend.models import db
from datetime import datetime


class AppSettings(db.Model):
    """Paramètres de l'application"""
    __tablename__ = 'app_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_value(key, default=None):
        """Récupère la valeur d'un paramètre"""
        setting = AppSettings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set_value(key, value, description=None):
        """Définit la valeur d'un paramètre"""
        setting = AppSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
            if description:
                setting.description = description
        else:
            setting = AppSettings(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting
    
    def __repr__(self):
        return f'<AppSettings {self.key}>'
