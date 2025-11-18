#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Agora.io Integration Service

Service pour gérer l'intégration avec Agora.io pour les réunions en ligne
"""

import os
import time
from agora_token_builder import RtcTokenBuilder, RtmTokenBuilder


class AgoraService:
    """Service pour gérer les tokens et channels Agora.io"""
    
    @staticmethod
    def get_app_id():
        """Récupère l'App ID Agora depuis les variables d'environnement"""
        return os.environ.get('AGORA_APP_ID', '')
    
    @staticmethod
    def get_app_certificate():
        """Récupère l'App Certificate Agora depuis les variables d'environnement"""
        return os.environ.get('AGORA_APP_CERTIFICATE', '')
    
    @staticmethod
    def generate_channel_name(assembly_id):
        """Génère un nom de channel unique pour une assemblée"""
        timestamp = int(time.time())
        return f"assembly_{assembly_id}_{timestamp}"
    
    @staticmethod
    def generate_rtc_token(channel_name, uid, role='publisher', expiration_seconds=3600):
        """
        Génère un token RTC pour Agora.io avec le SDK officiel
        
        Args:
            channel_name: Nom du channel
            uid: User ID (0 pour wildcard)
            role: 'publisher' ou 'subscriber'
            expiration_seconds: Durée de validité en secondes
        
        Returns:
            Token RTC string ou None en cas d'erreur
        """
        app_id = AgoraService.get_app_id()
        app_certificate = AgoraService.get_app_certificate()
        
        if not app_id or not app_certificate:
            print("Warning: AGORA_APP_ID ou AGORA_APP_CERTIFICATE non configuré")
            return None
        
        try:
            # Calculer l'expiration (timestamp Unix)
            privilege_expired_ts = int(time.time()) + expiration_seconds
            
            # Déterminer le rôle Agora
            agora_role = RtcTokenBuilder.Role_Publisher if role == 'publisher' else RtcTokenBuilder.Role_Subscriber
            
            # Générer le token avec le SDK officiel Agora
            token = RtcTokenBuilder.buildTokenWithUid(
                app_id,
                app_certificate,
                channel_name,
                uid,
                agora_role,
                privilege_expired_ts
            )
            
            return token
            
        except Exception as e:
            print(f"Erreur génération token RTC Agora: {e}")
            return None
    
    @staticmethod
    def generate_rtm_token(user_id, expiration_seconds=3600):
        """
        Génère un token RTM (Real-Time Messaging) pour Agora.io avec le SDK officiel
        
        Args:
            user_id: ID de l'utilisateur (string)
            expiration_seconds: Durée de validité en secondes
        
        Returns:
            Token RTM string ou None en cas d'erreur
        """
        app_id = AgoraService.get_app_id()
        app_certificate = AgoraService.get_app_certificate()
        
        if not app_id or not app_certificate:
            print("Warning: AGORA_APP_ID ou AGORA_APP_CERTIFICATE non configuré")
            return None
        
        try:
            # Calculer l'expiration
            privilege_expired_ts = int(time.time()) + expiration_seconds
            
            # Générer le token RTM avec le SDK officiel
            token = RtmTokenBuilder.buildToken(
                app_id,
                app_certificate,
                str(user_id),
                RtmTokenBuilder.Role_Rtm_User,
                privilege_expired_ts
            )
            
            return token
            
        except Exception as e:
            print(f"Erreur génération token RTM Agora: {e}")
            return None
    
    @staticmethod
    def start_cloud_recording(channel_name, uid):
        """
        Démarre l'enregistrement cloud d'un channel
        
        Returns:
            Recording SID ou None
        """
        # En production, appeler l'API Agora Cloud Recording
        # Pour le développement, retourner un SID factice
        timestamp = int(time.time())
        return f"rec_{channel_name}_{timestamp}"
    
    @staticmethod
    def stop_cloud_recording(recording_sid):
        """
        Arrête l'enregistrement cloud
        
        Returns:
            URL de la vidéo enregistrée ou None
        """
        # En production, appeler l'API Agora pour arrêter et récupérer l'URL
        return f"https://recordings.agora.io/{recording_sid}.mp4"
