#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shabaka Syndic - Solution complète et digitale pour les syndics et résidents au Maroc.

Shabaka Syndic
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
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
    from backend.models.residence_admin import ResidenceAdmin
    from backend.models.charge import Charge, ChargeDistribution
    from backend.models.payment import Payment
    from backend.models.maintenance import MaintenanceRequest
    from backend.models.maintenance_comment import MaintenanceComment
    from backend.models.maintenance_log import MaintenanceLog
    from backend.models.news import News
    from backend.models.poll import Poll, PollOption, PollVote
    from backend.models.document import Document
    from backend.models.general_assembly import GeneralAssembly, Resolution, Vote, Attendance
    
    with app.app_context():
        print("🚀 Initialisation de la base de données Shabaka Syndic avec données complètes...\n")
        
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
            syndic_name="Shabaka Syndic",
            syndic_email="contact@mysindic.ma",
            syndic_phone="+212522000000"
        )
        db.session.add(residence)
        db.session.commit()
        print(f"✅ Résidence créée: {residence.name} (ID: {residence.id})\n")
        
        # 3. Créer des unités
        print("🏠 Création des unités...")
        units_data = [
            {"number": "A101", "floor": 1, "type": "F3", "area": 85.5, "owner": "Ahmed Alami"},
            {"number": "A102", "floor": 1, "type": "F2", "area": 65.0, "owner": "Fatima El Amrani"},
            {"number": "A201", "floor": 2, "type": "F4", "area": 110.0, "owner": "Karim Bennani"},
            {"number": "A202", "floor": 2, "type": "F3", "area": 85.0, "owner": "Sarah Idrissi"},
            {"number": "B101", "floor": 1, "type": "F2", "area": 60.0, "owner": "Youssef Lahlou"},
        ]
        
        units = []
        for unit_data in units_data:
            unit = Unit(
                residence_id=residence.id,
                unit_number=unit_data["number"],
                floor=unit_data["floor"],
                unit_type=unit_data["type"],
                surface_area=unit_data["area"],
                owner_name=unit_data["owner"],
                owner_email=f"{unit_data['number'].lower()}@mysindic.ma"
            )
            db.session.add(unit)
            units.append(unit)
        
        db.session.commit()
        print(f"✅ {len(units_data)} unités créées\n")
        
        # 4. Créer des utilisateurs avec différents rôles
        print("👥 Création des comptes utilisateurs...")
        
        # Administrateur 1 (Bureau Syndic - Responsable principal)
        admin_user1 = User(
            email="admin.syndic@mysindic.ma",
            first_name="Hassan",
            last_name="Tazi",
            phone="+212600000001",
            role="admin",
            is_active=True,
            email_verified=True,
            residence_id=residence.id
        )
        admin_user1.set_password("Admin123!")
        db.session.add(admin_user1)
        
        # Administrateur 2 (Bureau Syndic - Comptable)
        admin_user2 = User(
            email="bureau.syndic@mysindic.ma",
            first_name="Leila",
            last_name="Mansouri",
            phone="+212600000010",
            role="admin",
            is_active=True,
            email_verified=True,
            residence_id=residence.id
        )
        admin_user2.set_password("Admin123!")
        db.session.add(admin_user2)
        
        # Propriétaire
        owner = User(
            email="owner@mysindic.ma",
            first_name="Ahmed",
            last_name="Alami",
            phone="+212600000002",
            role="owner",
            is_active=True,
            email_verified=True,
            residence_id=residence.id,
            unit_id=units[0].id
        )
        owner.set_password("Owner123!")
        db.session.add(owner)
        
        # Résidents
        residents_data = [
            {"email": "resident@mysindic.ma", "first_name": "Fatima", "last_name": "El Amrani", "unit_idx": 1},
            {"email": "karim@mysindic.ma", "first_name": "Karim", "last_name": "Bennani", "unit_idx": 2},
        ]
        
        residents = []
        for idx, resident_data in enumerate(residents_data):
            resident = User(
                email=resident_data["email"],
                first_name=resident_data["first_name"],
                last_name=resident_data["last_name"],
                phone=f"+21260000000{idx+3}",
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
        print(f"✅ 2 admins syndic (bureau), 1 propriétaire et {len(residents_data)} résidents créés\n")
        
        # Assigner les admins à la résidence
        print("🔗 Assignation des admins à la résidence...")
        admin_assignment1 = ResidenceAdmin(
            residence_id=residence.id,
            user_id=admin_user1.id,
            assigned_by=admin.id
        )
        admin_assignment2 = ResidenceAdmin(
            residence_id=residence.id,
            user_id=admin_user2.id,
            assigned_by=admin.id
        )
        db.session.add_all([admin_assignment1, admin_assignment2])
        db.session.commit()
        print(f"✅ 2 admins assignés à la résidence '{residence.name}'\n")
        
        # 5. Créer des charges (appels de fonds)
        print("💰 Création des charges...")
        charge1 = Charge(
            residence_id=residence.id,
            title="Charges Q1 2025",
            description="Appel de fonds pour le premier trimestre 2025",
            charge_type="courante",
            total_amount=50000.00,
            period_month=3,
            period_year=2025,
            due_date=datetime.now() + timedelta(days=30),
            status="published"
        )
        db.session.add(charge1)
        db.session.commit()
        
        # Créer les distributions de charges (répartition égale)
        amount_per_unit = charge1.total_amount / len(units)
        for unit in units:
            distribution = ChargeDistribution(
                charge_id=charge1.id,
                unit_id=unit.id,
                amount=amount_per_unit
            )
            db.session.add(distribution)
        
        db.session.commit()
        print(f"✅ Charges créées avec répartition\n")
        
        # 6. Créer quelques paiements
        print("💳 Création des paiements de démonstration...")
        payment1 = Payment(
            unit_id=units[0].id,
            user_id=owner.id,
            amount=10000.00,
            payment_date=datetime.now() - timedelta(days=5),
            payment_method="virement",
            reference="VIR20250101001",
            description="Paiement charges Q1 2025",
            status="validated",
            admin_notes="Paiement validé par l'administrateur"
        )
        
        payment2 = Payment(
            unit_id=units[1].id,
            user_id=residents[0].id,
            amount=10000.00,
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
            author_id=residents[0].id,
            tracking_number=MaintenanceRequest.generate_tracking_number(residence.id),
            request_type="resident_request",
            title="Fuite d'eau dans la salle de bain",
            description="Il y a une fuite sous le lavabo de la salle de bain principale. L'eau coule lentement mais constamment.",
            zone="appartement",
            zone_details=f"Appartement {units[1].unit_number}",
            priority="high",
            status="in_progress"
        )
        
        maintenance2 = MaintenanceRequest(
            residence_id=residence.id,
            author_id=residents[1].id,
            tracking_number=MaintenanceRequest.generate_tracking_number(residence.id),
            request_type="resident_request",
            title="Problème électrique - disjoncteur",
            description="Le disjoncteur saute fréquemment, surtout quand plusieurs appareils sont allumés en même temps.",
            zone="appartement",
            zone_details=f"Appartement {units[2].unit_number}",
            priority="urgent",
            status="pending"
        )
        
        maintenance3 = MaintenanceRequest(
            residence_id=residence.id,
            author_id=admin_user1.id,
            tracking_number=MaintenanceRequest.generate_tracking_number(residence.id),
            request_type="admin_announcement",
            title="Travaux d'entretien de l'ascenseur",
            description="L'ascenseur sera indisponible le 15 novembre de 8h à 17h pour maintenance annuelle obligatoire.",
            zone="ascenseur",
            zone_details="Ascenseur principal",
            priority="medium",
            status="pending",
            scheduled_date=datetime.now() + timedelta(days=15)
        )
        
        db.session.add_all([maintenance1, maintenance2, maintenance3])
        db.session.commit()
        print(f"✅ Demandes de maintenance créées\n")
        
        # 7.5. Créer des commentaires pour les demandes de maintenance
        print("💬 Création des commentaires de maintenance...")
        comment1 = MaintenanceComment(
            maintenance_request_id=maintenance1.id,
            author_id=admin_user1.id,
            comment_text="Demande bien reçue. Un plombier sera envoyé demain matin pour diagnostiquer la fuite.",
            comment_type="status_update",
            is_internal=False
        )
        
        comment2 = MaintenanceComment(
            maintenance_request_id=maintenance1.id,
            author_id=admin_user1.id,
            comment_text="Le plombier a identifié un joint défectueux. Intervention prévue cet après-midi.",
            comment_type="comment",
            is_internal=False
        )
        
        comment3 = MaintenanceComment(
            maintenance_request_id=maintenance1.id,
            author_id=residents[0].id,
            comment_text="Merci pour votre réactivité ! Je serai disponible entre 14h et 17h.",
            comment_type="comment",
            is_internal=False
        )
        
        comment4 = MaintenanceComment(
            maintenance_request_id=maintenance2.id,
            author_id=admin_user1.id,
            comment_text="@{} - Pourriez-vous nous indiquer si cela se produit avec des appareils spécifiques ?".format(residents[1].first_name + " " + residents[1].last_name),
            comment_type="mention",
            mentioned_user_id=residents[1].id,
            is_internal=False
        )
        
        comment5 = MaintenanceComment(
            maintenance_request_id=maintenance1.id,
            author_id=admin_user1.id,
            comment_text="Note interne: Vérifier si d'autres appartements ont le même problème.",
            comment_type="comment",
            is_internal=True
        )
        
        db.session.add_all([comment1, comment2, comment3, comment4, comment5])
        db.session.commit()
        print(f"✅ Commentaires de maintenance créés\n")
        
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
        
        # 9. Créer des actualités (2 types: feed pour tous, announcement pour admin/owner uniquement)
        print("📰 Création des actualités...")
        
        # Fil d'actualité (accessible à tous)
        news_feed1 = News(
            residence_id=residence.id,
            title="Bienvenue sur Shabaka Syndic!",
            content="Nous sommes ravis de vous présenter votre nouvelle plateforme de gestion de copropriété. Vous pouvez maintenant consulter vos charges, faire des demandes de maintenance et bien plus encore.",
            news_type="feed",
            category="info",
            author_id=admin.id,
            is_published=True,
            is_important=True
        )
        
        news_feed2 = News(
            residence_id=residence.id,
            title="Horaires de la piscine",
            content="La piscine est ouverte tous les jours de 7h à 21h. Merci de respecter les règles d'hygiène et de sécurité.",
            news_type="feed",
            category="info",
            author_id=admin_user1.id,
            is_published=True
        )
        
        # Actualités et annonces (pour admin/syndic/propriétaires uniquement)
        news_announcement1 = News(
            residence_id=residence.id,
            title="Prochaine Assemblée Générale - 15 Décembre 2025",
            content="L'Assemblée Générale Ordinaire se tiendra le 15 décembre 2025 à 18h00 dans la salle des fêtes de la résidence. Ordre du jour: approbation des comptes, vote du budget prévisionnel, travaux de rénovation.",
            news_type="announcement",
            category="evenement",
            author_id=admin.id,
            is_published=True,
            is_important=True,
            is_pinned=True
        )
        
        news_announcement2 = News(
            residence_id=residence.id,
            title="Travaux de rénovation de la piscine",
            content="Les travaux de rénovation de la piscine commune débuteront le 1er juin 2025. La piscine sera fermée pendant 3 semaines. Budget voté en AG: 150 000 MAD.",
            news_type="announcement",
            category="travaux",
            author_id=admin.id,
            is_published=True,
            is_important=True
        )
        
        db.session.add_all([news_feed1, news_feed2, news_announcement1, news_announcement2])
        db.session.commit()
        print(f"✅ Actualités créées (2 feed + 2 announcements)\n")
        
        # Note: Sondages, assemblées générales et documents peuvent être ajoutés 
        # manuellement via l'interface d'administration une fois l'application lancée
        
        print("=" * 70)
        print("🎉 Initialisation terminée avec succès!")
        print("=" * 70)
        print("\n📝 Comptes créés (4 rôles différents):")
        print(f"   🔑 Super Admin: admin@mysindic.ma / Admin123!")
        print(f"   👔 Admin Syndic 1: admin.syndic@mysindic.ma / Admin123!")
        print(f"   👔 Admin Syndic 2: bureau.syndic@mysindic.ma / Admin123!")
        print(f"   🏠 Propriétaire: owner@mysindic.ma / Owner123!")
        print(f"   👤 Résident 1: resident@mysindic.ma / Resident123!")
        print(f"   👤 Résident 2: karim@mysindic.ma / Resident123!")
        print(f"\n📊 Données créées:")
        print(f"   • 1 résidence (Les Jardins)")
        print(f"   • 5 unités")
        print(f"   • 6 utilisateurs (1 superadmin, 2 admin syndic, 1 propriétaire, 2 résidents)")
        print(f"   • 1 appel de fonds avec répartition")
        print(f"   • 2 paiements validés")
        print(f"   • 3 demandes de maintenance avec commentaires")
        print(f"   • 2 entrées du carnet d'entretien")
        print(f"   • 4 actualités (2 fil d'actualité + 2 actualités/annonces)")
        print("\n💡 Système de gestion de rôles:")
        print(f"   • Super Admin: Gestion complète, toutes les résidences")
        print(f"   • Admin/Syndic: Gestion de sa résidence assignée uniquement")
        print(f"   • Propriétaire: Accès étendu à sa résidence")
        print(f"   • Résident: Accès limité (maintenance + fil d'actualité)")
        print("\n📰 Deux fils d'actualité:")
        print(f"   • Fil d'actualité (news_type='feed'): Accessible à TOUS")
        print(f"   • Actualités et annonces (news_type='announcement'): Admin/Syndic/Propriétaires uniquement")
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
