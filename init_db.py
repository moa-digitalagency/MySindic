#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Script d'Initialisation de la Base de Données
Crée les tables et un compte superadmin par défaut

Date: 24 octobre 2025
"""

import os
import sys
from backend.app import app
from backend.models import db
from backend.models.user import User
from backend.models.residence import Residence, Unit
from backend.models.charge import Charge, ChargeDistribution
from backend.models.payment import Payment
from backend.models.maintenance import MaintenanceRequest
from backend.models.maintenance_log import MaintenanceLog
from backend.models.news import News
from backend.models.poll import Poll, PollOption, PollVote
from backend.models.document import Document
from backend.models.general_assembly import GeneralAssembly, Resolution, Vote, Attendance
from backend.models.litigation import Litigation


def init_database():
    """Initialise la base de données avec les tables et données de test"""
    print("🚀 Initialisation de la base de données MySindic...\n")
    
    with app.app_context():
        # Créer toutes les tables
        print("📋 Création des tables...")
        db.create_all()
        print("✅ Tables créées avec succès!\n")
        
        # Vérifier si un superadmin existe déjà
        existing_admin = User.query.filter_by(role='superadmin').first()
        if existing_admin:
            print(f"ℹ️  Un compte superadmin existe déjà: {existing_admin.email}\n")
            return
        
        # Créer un compte superadmin par défaut
        print("👤 Création du compte superadmin...")
        admin = User(
            email="admin@mysindic.ma",
            first_name="Super",
            last_name="Admin",
            phone="+212600000000",
            role="superadmin",
            is_active=True
        )
        admin.set_password("Admin123!")
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Compte superadmin créé avec succès!")
        print(f"   Email: {admin.email}")
        print(f"   Mot de passe: Admin123!")
        print(f"   ID: {admin.id}\n")
        
        # Créer une résidence de test
        print("🏢 Création d'une résidence de test...")
        residence = Residence(
            name="Résidence Les Jardins",
            address="123 Avenue Mohammed V",
            city="Casablanca",
            postal_code="20000",
            total_units=20,
            description="Résidence moderne avec espaces verts",
            syndic_name="MySindic",
            syndic_email="contact@mysindic.ma",
            syndic_phone="+212522000000",
            total_tantiemes=1000
        )
        
        db.session.add(residence)
        db.session.commit()
        
        print(f"✅ Résidence créée: {residence.name} (ID: {residence.id})\n")
        
        # Créer quelques unités de test
        print("🏠 Création d'unités de test...")
        units_data = [
            {"number": "A101", "floor": 1, "type": "F3", "area": 85.5, "tantiemes": 50},
            {"number": "A102", "floor": 1, "type": "F2", "area": 65.0, "tantiemes": 40},
            {"number": "A201", "floor": 2, "type": "F4", "area": 110.0, "tantiemes": 65},
        ]
        
        for unit_data in units_data:
            unit = Unit(
                residence_id=residence.id,
                unit_number=unit_data["number"],
                floor=unit_data["floor"],
                unit_type=unit_data["type"],
                surface_area=unit_data["area"],
                tantiemes=unit_data["tantiemes"],
                owner_name=f"Propriétaire {unit_data['number']}",
                owner_email=f"owner{unit_data['number'].lower()}@mysindic.ma"
            )
            db.session.add(unit)
        
        db.session.commit()
        print(f"✅ {len(units_data)} unités créées\n")
        
        # Créer un utilisateur résident de test
        print("👤 Création d'un compte résident de test...")
        resident = User(
            email="resident@mysindic.ma",
            first_name="Ahmed",
            last_name="Alami",
            phone="+212600000001",
            role="resident",
            is_active=True,
            residence_id=residence.id,
            unit_id=1
        )
        resident.set_password("Resident123!")
        
        db.session.add(resident)
        db.session.commit()
        
        print("✅ Compte résident créé avec succès!")
        print(f"   Email: {resident.email}")
        print(f"   Mot de passe: Resident123!")
        print(f"   Résidence: {residence.name}")
        print(f"   Unité: A101\n")
        
        print("=" * 60)
        print("🎉 Initialisation terminée avec succès!")
        print("=" * 60)
        print("\n📝 Comptes créés:")
        print(f"   Superadmin: admin@mysindic.ma / Admin123!")
        print(f"   Résident:   resident@mysindic.ma / Resident123!")
        print("\n🌐 Accédez à l'application et connectez-vous!")


if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
