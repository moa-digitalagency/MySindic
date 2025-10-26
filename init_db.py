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
        print("🚀 Initialisation manuelle de la base de données MySindic...\n")
        
        from backend.app import app
        from backend.models import db
        from backend.init_demo_data import init_demo_data
        
        # Initialiser avec toutes les données de démonstration
        init_demo_data(app, db)
        
        print("\n✨ Vous pouvez maintenant vous connecter avec les comptes créés!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
