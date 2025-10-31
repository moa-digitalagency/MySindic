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
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service centralisé de notifications
    """
    
    @staticmethod
    def send_email(to_email, subject, body, html_body=None):
        """
        Envoie un email
        
        Args:
            to_email: Email du destinataire
            subject: Sujet de l'email
            body: Corps du message (texte)
            html_body: Corps du message (HTML)
        """
        # TODO: Implémenter l'envoi réel avec Flask-Mail
        logger.info(f"Email envoyé à {to_email}: {subject}")
        return True
    
    @staticmethod
    def notify_new_maintenance_request(maintenance_request):
        """
        Notifie les administrateurs d'une nouvelle demande de maintenance
        """
        from backend.models.user import User
        
        admins = User.query.filter_by(role='superadmin').all()
        
        for admin in admins:
            NotificationService.send_email(
                to_email=admin.email,
                subject=f"Nouvelle demande de maintenance: {maintenance_request.title}",
                body=f"""
                Une nouvelle demande de maintenance a été créée.
                
                Titre: {maintenance_request.title}
                Zone: {maintenance_request.zone}
                Priorité: {maintenance_request.priority}
                Description: {maintenance_request.description}
                """
            )
    
    @staticmethod
    def notify_maintenance_status_update(maintenance_request):
        """
        Notifie le résident d'un changement de statut de sa demande
        """
        NotificationService.send_email(
            to_email=maintenance_request.author.email,
            subject=f"Mise à jour: {maintenance_request.title}",
            body=f"""
            Votre demande de maintenance a été mise à jour.
            
            Nouveau statut: {maintenance_request.status}
            """
        )
    
    @staticmethod
    def notify_charge_published(charge):
        """
        Notifie les résidents qu'une nouvelle charge a été publiée
        """
        from backend.models.user import User
        from backend.models.residence import Residence
        
        residence = Residence.query.get(charge.residence_id)
        residents = User.query.filter_by(residence_id=residence.id, role='resident').all()
        
        for resident in residents:
            NotificationService.send_email(
                to_email=resident.email,
                subject=f"Nouvel appel de fonds: {charge.title}",
                body=f"""
                Un nouvel appel de fonds a été publié pour votre résidence.
                
                Titre: {charge.title}
                Montant total: {charge.total_amount} MAD
                Date limite: {charge.due_date.strftime('%d/%m/%Y') if charge.due_date else 'Non définie'}
                """
            )
    
    @staticmethod
    def notify_assembly_convocation(assembly):
        """
        Envoie les convocations pour une assemblée générale
        """
        from backend.models.user import User
        from backend.models.residence import Residence
        
        residence = Residence.query.get(assembly.residence_id)
        residents = User.query.filter_by(residence_id=residence.id, role='resident').all()
        
        for resident in residents:
            NotificationService.send_email(
                to_email=resident.email,
                subject=f"Convocation: {assembly.title}",
                body=f"""
                Vous êtes convoqué(e) à l'assemblée générale suivante:
                
                Type: {assembly.assembly_type}
                Date: {assembly.scheduled_date.strftime('%d/%m/%Y à %H:%M')}
                Lieu: {assembly.location}
                
                Description:
                {assembly.description}
                """
            )
