#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Script d'Initialisation avec Données de Démonstration Complètes
Crée les tables et toutes les données de test nécessaires
"""

import os
import sys
from datetime import datetime, timedelta

def init_demo_data(app, db):
    """
    Initialise la base de données avec des données de démonstration complètes
    
    Args:
        app: Instance de l'application Flask
        db: Instance SQLAlchemy
    """
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
    
    with app.app_context():
        print("🚀 Initialisation de la base de données MySindic avec données complètes...\n")
        
        # Créer toutes les tables
        print("📋 Création des tables...")
        db.create_all()
        print("✅ Tables créées avec succès!\n")
        
        # Vérifier si des données existent déjà
        existing_admin = User.query.filter_by(role='superadmin').first()
        if existing_admin:
            print(f"ℹ️  Des données existent déjà dans la base de données.")
            print(f"   Superadmin existant: {existing_admin.email}\n")
            return
        
        # 1. Créer le compte superadmin
        print("👤 Création du compte superadmin...")
        admin = User(
            email="admin@mysindic.ma",
            first_name="Super",
            last_name="Admin",
            phone="+212600000000",
            role="superadmin",
            is_active=True,
            email_verified=True
        )
        admin.set_password("Admin123!")
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Superadmin créé: {admin.email}\n")
        
        # 2. Créer une résidence de test
        print("🏢 Création de la résidence de démonstration...")
        residence = Residence(
            name="Résidence Les Jardins",
            address="123 Avenue Mohammed V",
            city="Casablanca",
            postal_code="20000",
            total_units=20,
            description="Résidence moderne avec espaces verts et piscine",
            syndic_name="MySindic",
            syndic_email="contact@mysindic.ma",
            syndic_phone="+212522000000",
            total_tantiemes=1000
        )
        db.session.add(residence)
        db.session.commit()
        print(f"✅ Résidence créée: {residence.name} (ID: {residence.id})\n")
        
        # 3. Créer des unités
        print("🏠 Création des unités...")
        units_data = [
            {"number": "A101", "floor": 1, "type": "F3", "area": 85.5, "tantiemes": 50, "owner": "Ahmed Alami"},
            {"number": "A102", "floor": 1, "type": "F2", "area": 65.0, "tantiemes": 40, "owner": "Fatima El Amrani"},
            {"number": "A201", "floor": 2, "type": "F4", "area": 110.0, "tantiemes": 65, "owner": "Karim Bennani"},
            {"number": "A202", "floor": 2, "type": "F3", "area": 85.0, "tantiemes": 50, "owner": "Sarah Idrissi"},
            {"number": "B101", "floor": 1, "type": "F2", "area": 60.0, "tantiemes": 35, "owner": "Youssef Lahlou"},
        ]
        
        units = []
        for unit_data in units_data:
            unit = Unit(
                residence_id=residence.id,
                unit_number=unit_data["number"],
                floor=unit_data["floor"],
                unit_type=unit_data["type"],
                surface_area=unit_data["area"],
                tantiemes=unit_data["tantiemes"],
                owner_name=unit_data["owner"],
                owner_email=f"{unit_data['number'].lower()}@mysindic.ma"
            )
            db.session.add(unit)
            units.append(unit)
        
        db.session.commit()
        print(f"✅ {len(units_data)} unités créées\n")
        
        # 4. Créer des utilisateurs résidents
        print("👥 Création des comptes résidents...")
        residents_data = [
            {"email": "resident@mysindic.ma", "first_name": "Ahmed", "last_name": "Alami", "unit_idx": 0},
            {"email": "fatima@mysindic.ma", "first_name": "Fatima", "last_name": "El Amrani", "unit_idx": 1},
            {"email": "karim@mysindic.ma", "first_name": "Karim", "last_name": "Bennani", "unit_idx": 2},
        ]
        
        residents = []
        for idx, resident_data in enumerate(residents_data):
            resident = User(
                email=resident_data["email"],
                first_name=resident_data["first_name"],
                last_name=resident_data["last_name"],
                phone=f"+21260000000{idx+1}",
                role="resident",
                is_active=True,
                email_verified=True,
                residence_id=residence.id,
                unit_id=units[resident_data["unit_idx"]].id
            )
            resident.set_password("Resident123!")
            db.session.add(resident)
            residents.append(resident)
        
        db.session.commit()
        print(f"✅ {len(residents_data)} résidents créés\n")
        
        # 5. Créer des charges (appels de fonds)
        print("💰 Création des charges...")
        charge1 = Charge(
            residence_id=residence.id,
            title="Charges Q1 2025",
            description="Appel de fonds pour le premier trimestre 2025",
            charge_type="regular",
            total_amount=50000.00,
            period_month=3,
            period_year=2025,
            due_date=datetime.now() + timedelta(days=30),
            status="published"
        )
        db.session.add(charge1)
        db.session.commit()
        
        # Créer les distributions de charges
        for unit in units:
            distribution = ChargeDistribution(
                charge_id=charge1.id,
                unit_id=unit.id,
                amount=(charge1.total_amount * unit.tantiemes / residence.total_tantiemes)
            )
            db.session.add(distribution)
        
        db.session.commit()
        print(f"✅ Charges créées avec répartition\n")
        
        # 6. Créer quelques paiements
        print("💳 Création des paiements de démonstration...")
        payment1 = Payment(
            unit_id=units[0].id,
            user_id=residents[0].id,
            amount=2500.00,
            payment_date=datetime.now() - timedelta(days=5),
            payment_method="virement",
            reference="VIR20250101001",
            description="Paiement charges Q1 2025",
            status="validated",
            admin_notes="Paiement validé par l'administrateur"
        )
        
        payment2 = Payment(
            unit_id=units[1].id,
            user_id=residents[1].id,
            amount=2000.00,
            payment_date=datetime.now() - timedelta(days=10),
            payment_method="cheque",
            reference="CHQ123456",
            description="Paiement charges Q1 2025",
            status="validated"
        )
        
        db.session.add_all([payment1, payment2])
        db.session.commit()
        print(f"✅ Paiements créés\n")
        
        # 7. Créer des demandes de maintenance
        print("🔧 Création des demandes de maintenance...")
        maintenance1 = MaintenanceRequest(
            residence_id=residence.id,
            requester_id=residents[0].id,
            title="Fuite d'eau dans la salle de bain",
            description="Il y a une fuite sous le lavabo de la salle de bain principale",
            category="plumbing",
            priority="high",
            status="in_progress"
        )
        
        maintenance2 = MaintenanceRequest(
            residence_id=residence.id,
            requester_id=residents[1].id,
            title="Problème électrique - disjoncteur",
            description="Le disjoncteur saute fréquemment",
            category="electrical",
            priority="urgent",
            status="pending"
        )
        
        db.session.add_all([maintenance1, maintenance2])
        db.session.commit()
        print(f"✅ Demandes de maintenance créées\n")
        
        # 8. Créer des entrées dans le carnet d'entretien
        print("📓 Création d'entrées du carnet d'entretien...")
        log1 = MaintenanceLog(
            residence_id=residence.id,
            title="Entretien annuel de la chaudière",
            description="Maintenance préventive de la chaudière collective",
            intervention_type="maintenance_preventive",
            category="chauffage",
            contractor_name="Société Chauffage Pro",
            contractor_contact="+212522111111",
            intervention_date=datetime.now() - timedelta(days=15),
            next_intervention_date=datetime.now() + timedelta(days=350),
            cost=3500.00,
            invoice_number="INV-2025-001",
            created_by=admin.id
        )
        
        log2 = MaintenanceLog(
            residence_id=residence.id,
            title="Nettoyage des gouttières",
            description="Nettoyage complet du système de gouttières",
            intervention_type="maintenance_preventive",
            category="toiture",
            contractor_name="Entreprise Toiture",
            contractor_contact="+212522222222",
            intervention_date=datetime.now() - timedelta(days=7),
            next_intervention_date=datetime.now() + timedelta(days=180),
            cost=1200.00,
            invoice_number="INV-2025-002",
            created_by=admin.id
        )
        
        db.session.add_all([log1, log2])
        db.session.commit()
        print(f"✅ Carnet d'entretien initialisé\n")
        
        # 9. Créer des actualités
        print("📰 Création des actualités...")
        news1 = News(
            residence_id=residence.id,
            title="Bienvenue sur MySindic!",
            content="Nous sommes ravis de vous présenter votre nouvelle plateforme de gestion de copropriété. Vous pouvez maintenant consulter vos charges, faire des demandes de maintenance et bien plus encore.",
            author_id=admin.id,
            is_published=True
        )
        
        news2 = News(
            residence_id=residence.id,
            title="Travaux de rénovation de la piscine",
            content="Les travaux de rénovation de la piscine commune débuteront le 1er juin 2025. La piscine sera fermée pendant 3 semaines.",
            author_id=admin.id,
            is_published=True
        )
        
        db.session.add_all([news1, news2])
        db.session.commit()
        print(f"✅ Actualités créées\n")
        
        # Note: Sondages, assemblées générales et documents peuvent être ajoutés 
        # manuellement via l'interface d'administration une fois l'application lancée
        
        print("=" * 70)
        print("🎉 Initialisation terminée avec succès!")
        print("=" * 70)
        print("\n📝 Comptes créés:")
        print(f"   Superadmin: admin@mysindic.ma / Admin123!")
        print(f"   Résident 1: resident@mysindic.ma / Resident123!")
        print(f"   Résident 2: fatima@mysindic.ma / Resident123!")
        print(f"   Résident 3: karim@mysindic.ma / Resident123!")
        print(f"\n📊 Données créées:")
        print(f"   • 1 résidence (Les Jardins)")
        print(f"   • 5 unités")
        print(f"   • 4 utilisateurs (1 admin + 3 résidents)")
        print(f"   • 1 appel de fonds avec répartition")
        print(f"   • 2 paiements validés")
        print(f"   • 2 demandes de maintenance")
        print(f"   • 2 entrées du carnet d'entretien")
        print(f"   • 2 actualités")
        print("\n🌐 Accédez à l'application et connectez-vous!")
        print("=" * 70)


if __name__ == "__main__":
    from backend.app import app
    from backend.models import db
    
    try:
        init_demo_data(app, db)
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
