# Référence API - Shabaka Syndic

Cette documentation détaille tous les endpoints REST de l'application Shabaka Syndic.

## Informations Générales

### URL de Base

```
https://[votre-domaine]/api
```

### Format des Réponses

Toutes les réponses sont au format JSON.

**Succès :**
```json
{
  "success": true,
  "data": { ... },
  "message": "Opération réussie"
}
```

**Erreur :**
```json
{
  "success": false,
  "error": "Description de l'erreur"
}
```

### Authentification

L'API utilise des sessions Flask-Login. Après connexion via `/api/auth/login`, un cookie de session est défini automatiquement.

### Codes HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 201 | Création réussie |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Accès refusé |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur |

---

## Authentification

### POST /api/auth/register

Inscription d'un nouvel utilisateur.

**Corps de la requête :**
```json
{
  "email": "user@example.com",
  "password": "MotDePasse123!",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone": "+212600000000"
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Compte créé avec succès",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Prénom",
    "last_name": "Nom",
    "role": "resident"
  }
}
```

### POST /api/auth/login

Connexion d'un utilisateur.

**Corps de la requête :**
```json
{
  "email": "user@example.com",
  "password": "MotDePasse123!",
  "remember": true
}
```

**Réponse :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "admin"
  }
}
```

### POST /api/auth/logout

Déconnexion de l'utilisateur.

**Réponse :**
```json
{
  "success": true,
  "message": "Déconnexion réussie"
}
```

### GET /api/auth/me

Récupère les informations de l'utilisateur connecté.

**Réponse :**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "admin@mysindic.ma",
    "first_name": "Super",
    "last_name": "Admin",
    "role": "superadmin",
    "residence_id": null,
    "unit_id": null
  }
}
```

### GET /api/auth/check

Vérifie si l'utilisateur est authentifié.

**Réponse :**
```json
{
  "authenticated": true,
  "user": { ... }
}
```

---

## Administration

### Dashboard

#### GET /api/admin/dashboard

Récupère les statistiques du tableau de bord.

**Accès :** Admin, Superadmin

**Réponse :**
```json
{
  "success": true,
  "stats": {
    "total_residences": 5,
    "total_users": 150,
    "total_units": 200,
    "total_charges": 12,
    "total_maintenance": 45,
    "pending_maintenance": 8,
    "total_unpaid": 125000.00
  }
}
```

---

### Résidences

#### GET /api/admin/residences

Liste des résidences.

**Accès :** Admin, Superadmin, Owner

**Réponse :**
```json
{
  "success": true,
  "residences": [
    {
      "id": 1,
      "name": "Résidence Les Jardins",
      "address": "123 Avenue Mohammed V",
      "city": "Casablanca",
      "total_units": 50,
      "is_active": true
    }
  ]
}
```

#### POST /api/admin/residences

Crée une nouvelle résidence.

**Accès :** Superadmin

**Corps (format simple) :**
```json
{
  "name": "Résidence Soleil",
  "address": "45 Rue de la Paix",
  "city": "Rabat",
  "postal_code": "10000",
  "total_units": 30
}
```

**Corps (format wizard) :**
```json
{
  "residence": {
    "name": "Résidence Soleil",
    "address": "45 Rue de la Paix",
    "city": "Rabat"
  },
  "units": [
    {"unit_number": "A101", "floor": 1, "unit_type": "appartement"},
    {"unit_number": "A102", "floor": 1, "unit_type": "appartement"}
  ]
}
```

#### PUT /api/admin/residences/:id

Modifie une résidence.

**Accès :** Superadmin

**Corps :**
```json
{
  "name": "Nouveau nom",
  "syndic_email": "nouveau@email.com"
}
```

---

### Lots (Units)

#### GET /api/admin/residences/:residence_id/units

Liste des lots d'une résidence.

**Accès :** Admin, Superadmin

**Réponse :**
```json
{
  "success": true,
  "units": [
    {
      "id": 1,
      "unit_number": "A101",
      "floor": 1,
      "building": "Bâtiment A",
      "unit_type": "appartement",
      "surface_area": 85.5,
      "owner_name": "Ahmed Alami"
    }
  ]
}
```

#### POST /api/admin/residences/:residence_id/units

Crée un nouveau lot.

**Accès :** Admin, Superadmin

**Corps :**
```json
{
  "unit_number": "A103",
  "floor": 1,
  "building": "Bâtiment A",
  "unit_type": "appartement",
  "surface_area": 90.0,
  "owner_name": "Fatima El Amrani",
  "owner_email": "fatima@email.com"
}
```

#### PUT /api/admin/units/:id

Modifie un lot.

#### DELETE /api/admin/units/:id

Supprime un lot.

---

### Charges (Appels de Fonds)

#### GET /api/admin/charges

Liste des charges.

**Accès :** Admin, Superadmin

**Paramètres :**
- `residence_id` (optionnel) : Filtrer par résidence

**Réponse :**
```json
{
  "success": true,
  "charges": [
    {
      "id": 1,
      "residence_id": 1,
      "title": "Charges Q1 2025",
      "charge_type": "courante",
      "total_amount": 50000.00,
      "period_month": 3,
      "period_year": 2025,
      "status": "published",
      "due_date": "2025-03-31T00:00:00"
    }
  ]
}
```

#### POST /api/admin/charges

Crée un appel de fonds.

**Corps :**
```json
{
  "residence_id": 1,
  "title": "Charges Q2 2025",
  "description": "Appel de fonds trimestriel",
  "charge_type": "courante",
  "total_amount": 60000.00,
  "period_month": 6,
  "period_year": 2025,
  "due_date": "2025-06-30"
}
```

#### POST /api/admin/charges/:id/publish

Publie une charge et calcule la répartition.

**Réponse :**
```json
{
  "success": true,
  "message": "Charge publiée et répartie",
  "distributions_created": 50
}
```

#### GET /api/admin/charges/:id/distributions

Récupère la répartition d'une charge.

**Réponse :**
```json
{
  "success": true,
  "distributions": [
    {
      "id": 1,
      "charge_id": 1,
      "unit_id": 1,
      "amount": 1000.00,
      "is_paid": false
    }
  ]
}
```

---

### Paiements

#### GET /api/admin/payments

Liste des paiements.

**Accès :** Admin, Superadmin, Owner

**Réponse :**
```json
{
  "success": true,
  "payments": [
    {
      "id": 1,
      "unit_id": 1,
      "user_id": 5,
      "amount": 10000.00,
      "payment_method": "virement",
      "reference": "VIR123456",
      "payment_date": "2025-01-15T00:00:00",
      "status": "pending"
    }
  ]
}
```

#### POST /api/admin/payments/:id/validate

Valide un paiement.

**Corps :**
```json
{
  "admin_notes": "Paiement vérifié et validé"
}
```

#### POST /api/admin/payments/:id/reject

Rejette un paiement.

**Corps :**
```json
{
  "admin_notes": "Montant incorrect"
}
```

#### GET /api/admin/units/:id/balance

Récupère le solde d'un lot.

**Réponse :**
```json
{
  "success": true,
  "balance": {
    "unit_id": 1,
    "total_charges": 30000.00,
    "total_payments": 20000.00,
    "balance": -10000.00,
    "status": "debit"
  }
}
```

---

### Maintenance

#### GET /api/admin/maintenance

Liste des demandes de maintenance.

**Paramètres :**
- `residence_id` (optionnel)
- `status` (optionnel) : pending, in_progress, resolved

**Réponse :**
```json
{
  "success": true,
  "maintenance_requests": [
    {
      "id": 1,
      "tracking_number": "MNT-2025-R0010001",
      "title": "Fuite d'eau",
      "description": "Fuite sous le lavabo",
      "zone": "appartement",
      "priority": "high",
      "status": "pending",
      "author_name": "Ahmed Alami"
    }
  ]
}
```

#### PUT /api/admin/maintenance/:id

Met à jour une demande de maintenance.

**Corps :**
```json
{
  "status": "in_progress",
  "assigned_to": "Plombier Pro",
  "admin_notes": "Intervention prévue demain"
}
```

#### GET /api/admin/maintenance/:id/comments

Liste les commentaires d'une demande.

#### POST /api/admin/maintenance/:id/comments

Ajoute un commentaire.

**Corps :**
```json
{
  "comment_text": "Le technicien passera demain matin",
  "is_internal": false
}
```

---

### Carnet d'Entretien

#### GET /api/admin/maintenance-logs

Liste des entrées du carnet d'entretien.

**Réponse :**
```json
{
  "success": true,
  "logs": [
    {
      "id": 1,
      "title": "Entretien chaudière",
      "intervention_type": "maintenance_preventive",
      "category": "chauffage",
      "contractor_name": "Chauffage Pro",
      "intervention_date": "2025-01-10T00:00:00",
      "next_intervention_date": "2026-01-10T00:00:00",
      "cost": 3500.00
    }
  ]
}
```

#### POST /api/admin/maintenance-logs

Crée une entrée.

**Corps :**
```json
{
  "residence_id": 1,
  "title": "Nettoyage toiture",
  "description": "Nettoyage complet des gouttières",
  "intervention_type": "maintenance_preventive",
  "category": "toiture",
  "contractor_name": "Toiture Express",
  "contractor_contact": "+212600000000",
  "intervention_date": "2025-02-01",
  "cost": 2000.00
}
```

---

### Assemblées Générales

#### GET /api/admin/assemblies

Liste des assemblées générales.

#### POST /api/admin/assemblies

Crée une AG.

**Corps :**
```json
{
  "residence_id": 1,
  "title": "AG Ordinaire 2025",
  "description": "Assemblée générale annuelle",
  "assembly_type": "ordinaire",
  "meeting_mode": "both",
  "scheduled_date": "2025-03-15T18:00:00",
  "location": "Salle des fêtes"
}
```

#### PUT /api/admin/assemblies/:id

Modifie une AG.

#### POST /api/admin/assemblies/:id/resolutions

Ajoute une résolution.

**Corps :**
```json
{
  "title": "Approbation des comptes 2024",
  "description": "Vote sur l'approbation des comptes de l'exercice 2024",
  "vote_type": "simple",
  "order": 1
}
```

#### POST /api/admin/assemblies/:id/send-convocations

Envoie les convocations.

#### POST /api/admin/assemblies/:id/start

Démarre l'AG.

#### POST /api/admin/assemblies/:id/end

Termine l'AG.

#### GET /api/admin/assemblies/:id/token

Génère un token Agora pour une AG en ligne.

---

### Actualités

#### GET /api/admin/news

Liste des actualités.

**Paramètres :**
- `residence_id` (optionnel)
- `type` (optionnel) : feed, announcement

#### POST /api/admin/news

Crée une actualité.

**Corps :**
```json
{
  "residence_id": 1,
  "title": "Fermeture piscine",
  "content": "La piscine sera fermée du 1er au 15 février pour maintenance.",
  "news_type": "feed",
  "category": "info",
  "is_important": false,
  "is_pinned": false
}
```

#### PUT /api/admin/news/:id

Modifie une actualité.

#### DELETE /api/admin/news/:id

Supprime une actualité.

---

### Sondages

#### GET /api/admin/polls

Liste des sondages.

#### POST /api/admin/polls

Crée un sondage.

**Corps :**
```json
{
  "residence_id": 1,
  "question": "Souhaitez-vous installer une borne de recharge électrique ?",
  "description": "Installation dans le parking souterrain",
  "options": [
    {"option_text": "Oui", "order": 1},
    {"option_text": "Non", "order": 2},
    {"option_text": "Sans avis", "order": 3}
  ],
  "end_date": "2025-02-28"
}
```

#### POST /api/admin/polls/:id/close

Ferme un sondage.

---

### Documents

#### GET /api/admin/documents

Liste des documents.

#### POST /api/admin/documents

Upload un document (multipart/form-data).

**Champs :**
- `file` : Fichier
- `residence_id` : ID résidence
- `title` : Titre
- `document_type` : Type (reglement, pv_ag, contrat, etc.)
- `is_public` : Visible par les résidents

#### DELETE /api/admin/documents/:id

Supprime un document.

---

### Utilisateurs

#### GET /api/admin/users

Liste des utilisateurs.

#### PUT /api/admin/users/:id

Modifie un utilisateur.

**Corps :**
```json
{
  "role": "owner",
  "residence_id": 1,
  "unit_id": 5,
  "is_active": true
}
```

---

### Contentieux

#### GET /api/admin/litigations

Liste des contentieux.

#### POST /api/admin/litigations

Crée un contentieux.

#### PUT /api/admin/litigations/:id

Modifie un contentieux.

---

### Paramètres

#### GET /api/admin/settings/custom-head

Récupère le code personnalisé injecté dans le head.

#### POST /api/admin/settings/custom-head

Sauvegarde le code personnalisé.

**Corps :**
```json
{
  "custom_head_code": "<!-- Google Analytics -->\n<script>...</script>"
}
```

---

## API Résident

### Dashboard

#### GET /api/resident/dashboard

Tableau de bord personnalisé du résident.

**Réponse :**
```json
{
  "success": true,
  "maintenance_requests": [...],
  "news": [...],
  "balance": {...},
  "upcoming_assemblies": [...]
}
```

---

### Actualités

#### GET /api/resident/news

Liste des actualités accessibles.

**Paramètres :**
- `type` : feed (défaut), announcement (propriétaires uniquement)

#### GET /api/resident/news/:id

Détail d'une actualité.

#### POST /api/resident/news

Publie une actualité (propriétaires uniquement).

---

### Maintenance

#### POST /api/resident/maintenance

Crée une demande de maintenance.

**Corps (JSON) :**
```json
{
  "title": "Problème de chauffage",
  "description": "Le radiateur du salon ne chauffe plus",
  "zone": "appartement",
  "zone_details": "Salon",
  "priority": "medium"
}
```

**Corps (multipart/form-data avec image) :**
- `title`, `description`, `zone`, `priority` : champs texte
- `image` : fichier image

#### GET /api/resident/maintenance

Liste des demandes de l'utilisateur.

#### GET /api/resident/maintenance/:id

Détail d'une demande.

#### GET /api/resident/maintenance/:id/comments

Liste des commentaires (non internes).

#### POST /api/resident/maintenance/:id/comments

Ajoute un commentaire.

---

### Finances

#### GET /api/resident/charges

Liste des charges de l'utilisateur.

#### GET /api/resident/charges/unpaid

Liste des charges impayées.

#### GET /api/resident/balance

Solde du compte.

#### POST /api/resident/payments

Déclare un paiement.

**Corps :**
```json
{
  "amount": 10000.00,
  "payment_method": "virement",
  "reference": "VIR123456",
  "payment_date": "2025-01-20",
  "description": "Paiement charges Q1"
}
```

#### GET /api/resident/payments

Historique des paiements.

---

### Documents

#### GET /api/resident/documents

Liste des documents publics.

#### GET /api/resident/documents/:id

Détail d'un document.

---

### Sondages

#### GET /api/resident/polls

Liste des sondages actifs.

#### GET /api/resident/polls/:id

Détail d'un sondage avec résultats.

#### POST /api/resident/polls/:id/vote

Vote sur un sondage.

**Corps :**
```json
{
  "option_id": 1
}
```

---

### Assemblées Générales

#### GET /api/resident/assemblies

Liste des AG.

#### GET /api/resident/assemblies/:id

Détail d'une AG avec résolutions.

#### POST /api/resident/assemblies/:id/attend

Confirme la présence.

**Corps :**
```json
{
  "attendance_mode": "physical"
}
```

#### POST /api/resident/resolutions/:id/vote

Vote sur une résolution.

**Corps :**
```json
{
  "vote_value": "for"
}
```

Valeurs possibles : `for`, `against`, `abstain`

---

## Endpoints Utilitaires

### GET /health

Vérifie l'état de l'application.

**Réponse :**
```json
{
  "status": "healthy",
  "application": "Shabaka Syndic",
  "version": "0.1.0",
  "database": "connected"
}
```

### GET /api/info

Informations sur l'API.

**Réponse :**
```json
{
  "name": "Shabaka Syndic API",
  "version": "0.1.0",
  "description": "API de gestion de copropriété",
  "endpoints": {
    "health": "/health",
    "auth": "/api/auth/*",
    "admin": "/api/admin/*",
    "resident": "/api/resident/*"
  }
}
```
