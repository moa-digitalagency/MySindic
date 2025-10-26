#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import sys


if __name__ == "__main__":
    try:
        print("⚠️  ATTENTION: Ce script va supprimer TOUTES les données existantes!")
        print("Appuyez sur Ctrl+C pour annuler dans les 3 secondes...\n")
        
        import time
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("\n🗑️  Suppression de toutes les données...\n")
        
        from backend.app import app
        from backend.models import db
        from backend.init_demo_data import init_demo_data
        
        with app.app_context():
            # Supprimer toutes les tables
            print("📋 Suppression des tables existantes...")
            db.drop_all()
            print("✅ Tables supprimées\n")
            
            # Réinitialiser avec toutes les données de démonstration
            init_demo_data(app, db)
        
        print("\n✨ Base de données réinitialisée avec succès!")
        print("Vous pouvez maintenant vous connecter avec les comptes de démonstration.")
        
    except KeyboardInterrupt:
        print("\n\n❌ Réinitialisation annulée par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur lors de la réinitialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
