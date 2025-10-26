#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySindic - Calculateur de Charges
Service de calcul automatique de répartition des charges

Date: 24 octobre 2025
"""

from decimal import Decimal
from backend.models import db
from backend.models.residence import Unit
from backend.models.charge import Charge, ChargeDistribution


class ChargeCalculator:
    """
    Service de calcul et répartition des charges
    """
    
    @staticmethod
    def calculate_distribution(charge_id):
        """
        Calcule la répartition égale des charges pour tous les lots
        
        Args:
            charge_id: ID de la charge à répartir
            
        Returns:
            list: Liste des distributions créées
        """
        charge = Charge.query.get(charge_id)
        if not charge:
            raise ValueError("Charge non trouvée")
        
        # Récupérer tous les lots de la résidence
        units = Unit.query.filter_by(residence_id=charge.residence_id).all()
        
        if not units:
            raise ValueError("Aucun lot trouvé pour cette résidence")
        
        # Calculer le nombre total de lots
        total_units = len(units)
        
        distributions = []
        
        for unit in units:
            # Calculer le montant égal pour chaque lot
            amount = charge.total_amount / Decimal(str(total_units))
            
            # Créer ou mettre à jour la distribution
            distribution = ChargeDistribution.query.filter_by(
                charge_id=charge_id,
                unit_id=unit.id
            ).first()
            
            if distribution:
                distribution.amount = amount
            else:
                distribution = ChargeDistribution(
                    charge_id=charge_id,
                    unit_id=unit.id,
                    amount=amount
                )
                db.session.add(distribution)
            
            distributions.append(distribution)
        
        db.session.commit()
        return distributions
    
    @staticmethod
    def get_unit_balance(unit_id):
        """
        Calcule le solde d'un lot (charges dues - paiements)
        
        Args:
            unit_id: ID du lot
            
        Returns:
            dict: Détails du solde
        """
        from backend.models.payment import Payment
        
        # Total des charges
        distributions = ChargeDistribution.query.filter_by(unit_id=unit_id).all()
        total_charges = sum(float(d.amount) for d in distributions)
        
        # Total des paiements validés
        payments = Payment.query.filter_by(unit_id=unit_id, status='validated').all()
        total_payments = sum(float(p.amount) for p in payments)
        
        balance = total_payments - total_charges
        
        return {
            'unit_id': unit_id,
            'total_charges': total_charges,
            'total_payments': total_payments,
            'balance': balance,
            'status': 'credit' if balance > 0 else 'debit' if balance < 0 else 'balanced'
        }
    
    @staticmethod
    def get_unpaid_charges(unit_id):
        """
        Récupère les charges impayées pour un lot
        
        Args:
            unit_id: ID du lot
            
        Returns:
            list: Liste des distributions impayées
        """
        unpaid = ChargeDistribution.query.filter_by(
            unit_id=unit_id,
            is_paid=False
        ).join(Charge).filter(Charge.status == 'published').all()
        
        return [d.to_dict() for d in unpaid]
