#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instances des extensions
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    """
    Initialise la base de données avec l'application Flask
    
    Args:
        app: Instance de l'application Flask
    """
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importer tous les modèles ici pour que Flask-Migrate les détecte
    from backend.models.user import User
    from backend.models.residence import Residence, Unit
    from backend.models.residence_admin import ResidenceAdmin
    from backend.models.maintenance import MaintenanceRequest
    from backend.models.maintenance_comment import MaintenanceComment
    from backend.models.maintenance_document import MaintenanceDocument
    from backend.models.document import Document
    from backend.models.charge import Charge, ChargeDistribution
    from backend.models.payment import Payment
    from backend.models.news import News
    from backend.models.poll import Poll, PollOption, PollVote
    from backend.models.general_assembly import GeneralAssembly, Resolution, Vote, Attendance
    from backend.models.litigation import Litigation
    from backend.models.maintenance_log import MaintenanceLog
    from backend.models.app_settings import AppSettings
