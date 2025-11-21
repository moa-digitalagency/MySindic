#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour nettoyer la base de données et créer de nouveaux comptes de démo
avec les permissions correctes pour chaque rôle.
"""

import sys
from datetime import datetime

def clean_and_recreate():
    """Nettoie la base de données et crée de nouveaux comptes de démo"""
    
    print("🧹 Nettoyage de la base de données...")
    
    from backend.app import app
    from backend.models import db
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
        # Supprimer TOUTES les données dans l'ordre correct (foreign keys)
        print("❌ Suppression de toutes les données...")
        
        # Tables avec foreign keys vers d'autres tables
        PollVote.query.delete()
        PollOption.query.delete()
        Poll.query.delete()
        Vote.query.delete()
        Attendance.query.delete()
        Resolution.query.delete()
        GeneralAssembly.query.delete()
        Document.query.delete()
        MaintenanceComment.query.delete()
        MaintenanceLog.query.delete()
        MaintenanceRequest.query.delete()
        Payment.query.delete()
        ChargeDistribution.query.delete()
        Charge.query.delete()
        News.query.delete()
        ResidenceAdmin.query.delete()
        
        # Tables utilisateurs et unités
        User.query.delete()
        Unit.query.delete()
        Residence.query.delete()
        
        db.session.commit()
        print("✅ Toutes les données ont été supprimées!\n")
        
        # Créer de nouvelles données
        print("🔨 Création de nouvelles données de démo...\n")
        
        # 1. Créer le Super Admin
        print("👑 Création du compte Super Admin...")
        superadmin = User(
            email="superadmin@shabaka.ma",
            first_name="Super",
            last_name="Admin",
            phone="+212600000000",
            role="superadmin",
            is_active=True,
            email_verified=True
        )
        superadmin.set_password("Super123!")
        db.session.add(superadmin)
        db.session.commit()
        print(f"✅ Super Admin créé: {superadmin.email} / Super123!\n")
        
        # 2. Créer une résidence
        print("🏢 Création de la résidence...")
        residence = Residence(
            name="Résidence Al Andalous",
            address="456 Boulevard Zerktouni",
            city="Casablanca",
            postal_code="20100",
            total_units=15,
            description="Résidence moderne au cœur de Casablanca",
            syndic_name="Shabaka Syndic",
            syndic_email="contact@shabaka.ma",
            syndic_phone="+212522111111"
        )
        db.session.add(residence)
        db.session.commit()
        print(f"✅ Résidence créée: {residence.name} (ID: {residence.id})\n")
        
        # 3. Créer des unités
        print("🏠 Création des unités...")
        units_data = [
            {"number": "A101", "floor": 1, "type": "F3", "area": 90.0},
            {"number": "A102", "floor": 1, "type": "F2", "area": 70.0},
            {"number": "A201", "floor": 2, "type": "F4", "area": 120.0},
            {"number": "A202", "floor": 2, "type": "F3", "area": 85.0},
            {"number": "B101", "floor": 1, "type": "F2", "area": 65.0},
        ]
        
        units = []
        for unit_data in units_data:
            unit = Unit(
                residence_id=residence.id,
                unit_number=unit_data["number"],
                floor=unit_data["floor"],
                unit_type=unit_data["type"],
                surface_area=unit_data["area"]
            )
            db.session.add(unit)
            units.append(unit)
        
        db.session.commit()
        print(f"✅ {len(units)} unités créées\n")
        
        # 4. Créer Bureau Syndic (Admin)
        print("🏛️ Création du compte Bureau Syndic (Admin)...")
        bureau_syndic = User(
            email="syndic@shabaka.ma",
            first_name="Mohammed",
            last_name="Benali",
            phone="+212600000001",
            role="admin",
            is_active=True,
            email_verified=True,
            residence_id=residence.id
        )
        bureau_syndic.set_password("Syndic123!")
        db.session.add(bureau_syndic)
        db.session.commit()
        
        # Assigner l'admin à la résidence
        admin_assignment = ResidenceAdmin(
            residence_id=residence.id,
            user_id=bureau_syndic.id,
            assigned_by=superadmin.id
        )
        db.session.add(admin_assignment)
        db.session.commit()
        print(f"✅ Bureau Syndic créé: {bureau_syndic.email} / Syndic123!\n")
        
        # 5. Créer Propriétaire
        print("🏠 Création du compte Propriétaire...")
        proprietaire = User(
            email="proprietaire@shabaka.ma",
            first_name="Amina",
            last_name="Chakir",
            phone="+212600000002",
            role="owner",
            is_active=True,
            email_verified=True,
            residence_id=residence.id,
            unit_id=units[0].id
        )
        proprietaire.set_password("Owner123!")
        db.session.add(proprietaire)
        db.session.commit()
        print(f"✅ Propriétaire créé: {proprietaire.email} / Owner123! (Unité: {units[0].unit_number})\n")
        
        # 6. Créer Résident
        print("👤 Création du compte Résident...")
        resident = User(
            email="resident@shabaka.ma",
            first_name="Youssef",
            last_name="Alaoui",
            phone="+212600000003",
            role="resident",
            is_active=True,
            email_verified=True,
            residence_id=residence.id,
            unit_id=units[1].id
        )
        resident.set_password("Resident123!")
        db.session.add(resident)
        db.session.commit()
        print(f"✅ Résident créé: {resident.email} / Resident123! (Unité: {units[1].unit_number})\n")
        
        # 7. Créer des actualités de démo
        print("📰 Création des actualités de démo...")
        
        # Fil d'actualité (accessible à tous)
        news_feed_1 = News(
            residence_id=residence.id,
            author_id=bureau_syndic.id,
            title="Bienvenue sur Shabaka Syndic! 🎉",
            content="Nous sommes ravis de vous accueillir sur notre nouvelle plateforme de gestion de copropriété. Vous pourrez désormais consulter toutes les actualités de votre résidence en temps réel.",
            news_type="feed",
            is_published=True,
            is_pinned=True,
            published_at=datetime.utcnow()
        )
        db.session.add(news_feed_1)
        
        news_feed_2 = News(
            residence_id=residence.id,
            author_id=bureau_syndic.id,
            title="Horaires de collecte des ordures",
            content="Les ordures ménagères sont collectées tous les mardis et vendredis à partir de 7h00. Merci de déposer vos sacs la veille au soir.",
            news_type="feed",
            is_published=True,
            published_at=datetime.utcnow()
        )
        db.session.add(news_feed_2)
        
        # Actualités et annonces (super admin, syndic, propriétaires uniquement)
        news_announcement_1 = News(
            residence_id=residence.id,
            author_id=bureau_syndic.id,
            title="📋 Convocation à l'Assemblée Générale Ordinaire",
            content="Chers copropriétaires, vous êtes convoqués à l'Assemblée Générale Ordinaire qui se tiendra le 15 décembre 2025 à 18h00 dans la salle commune. Ordre du jour : approbation des comptes, budget prévisionnel, travaux d'entretien.",
            news_type="announcement",
            is_published=True,
            is_pinned=True,
            published_at=datetime.utcnow()
        )
        db.session.add(news_announcement_1)
        
        news_announcement_2 = News(
            residence_id=residence.id,
            author_id=bureau_syndic.id,
            title="💰 Appel de fonds trimestriel - Q4 2025",
            content="L'appel de fonds pour le 4ème trimestre 2025 a été émis. Montant : 450 DH par quote-part. Date limite de paiement : 30 novembre 2025. Merci de procéder au règlement dans les délais.",
            news_type="announcement",
            is_published=True,
            published_at=datetime.utcnow()
        )
        db.session.add(news_announcement_2)
        
        db.session.commit()
        print(f"✅ 4 actualités créées (2 feed + 2 announcements)\n")
        
        # Résumé final
        print("=" * 70)
        print("✨ Base de données nettoyée et recréée avec succès!")
        print("=" * 70)
        print("\n📋 COMPTES DE DÉMO CRÉÉS:\n")
        print("1️⃣  SUPER ADMIN")
        print("   Email: superadmin@shabaka.ma")
        print("   Mot de passe: Super123!")
        print("   Droits: Tous les droits, créer résidences, assigner admins\n")
        
        print("2️⃣  BUREAU SYNDIC (Admin)")
        print("   Email: syndic@shabaka.ma")
        print("   Mot de passe: Syndic123!")
        print("   Droits: Gérer résidences, utilisateurs, assemblées, maintenance,")
        print("           carnet d'entretien, finances, documents\n")
        
        print("3️⃣  PROPRIÉTAIRE")
        print("   Email: proprietaire@shabaka.ma")
        print("   Mot de passe: Owner123!")
        print("   Droits: Accès AG, gérer résidents de son unité, actualités,")
        print("           maintenance, finances, assemblées, documents\n")
        
        print("4️⃣  RÉSIDENT")
        print("   Email: resident@shabaka.ma")
        print("   Mot de passe: Resident123!")
        print("   Droits: Fil d'actualités + maintenance (demande et suivi)\n")
        
        print("=" * 70)

if __name__ == "__main__":
    try:
        clean_and_recreate()
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
