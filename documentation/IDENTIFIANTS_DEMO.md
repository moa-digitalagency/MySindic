# 🔐 Shabaka Syndic - Identifiants de Démonstration

**Dernière mise à jour :** 21 novembre 2025

Ce document contient tous les identifiants de démonstration pour tester l'application Shabaka Syndic.

⚠️ **Auto-initialisation activée** - La base de données s'initialise automatiquement au premier démarrage!

---

## 👨‍💼 Compte Superadmin

Utilisez ce compte pour accéder à toutes les fonctionnalités d'administration.

**Email :** `admin@mysindic.ma`  
**Mot de passe :** `Admin123!`

### Accès Superadmin:
- ✅ Dashboard avec statistiques complètes de toutes les résidences
- ✅ Gestion complète des résidences (création, modification, suppression)
- ✅ Gestion des unités/lots
- ✅ Gestion de tous les utilisateurs (tous rôles)
- ✅ Assignation des admins syndic aux résidences
- ✅ Appels de fonds et répartition des charges
- ✅ Validation des paiements
- ✅ Gestion de la maintenance et carnet d'entretien
- ✅ Assemblées générales et résolutions
- ✅ Gestion des contentieux
- ✅ Documents et actualités
- ✅ Accès aux deux fils d'actualité:
  - **Fil d'actualité** (pour tous)
  - **Actualités et annonces** (admin/syndic/propriétaires)
- ✅ Paramètres de l'application

**Pages accessibles :**
- `/admin/dashboard` - Tableau de bord
- `/admin/residences` - Gestion des résidences (voir toutes, créer, modifier, supprimer)
- `/admin/finances` - Gestion financière
- `/admin/maintenance` - Gestion de la maintenance
- `/admin/users` - Gestion des utilisateurs
- `/admin/assemblies` - Assemblées générales
- `/admin/documents` - Gestion des documents
- `/admin/maintenance-log` - Carnet d'entretien
- `/admin/feed` - Fil d'actualité (pour tous)
- `/admin/announcements` - Actualités et annonces (admin/syndic/propriétaires)
- `/admin/settings` - Paramètres (superadmin uniquement)

---

## 👔 Comptes Bureau Syndic (Administrateurs)

Utilisez ces comptes pour gérer la résidence assignée (validation des paiements, gestion des charges, maintenance, etc.).

### Bureau Syndic 1 - Responsable Principal
**Email :** `admin.syndic@mysindic.ma`  
**Mot de passe :** `Admin123!`
- **Résidence :** Résidence Les Jardins
- **Rôle :** Administrateur (admin)
- **Accès :** Gestion complète de la résidence assignée uniquement

### Bureau Syndic 2 - Comptable
**Email :** `bureau.syndic@mysindic.ma`  
**Mot de passe :** `Admin123!`
- **Résidence :** Résidence Les Jardins
- **Rôle :** Administrateur (admin)
- **Accès :** Gestion complète de la résidence assignée uniquement

### Accès Bureau Syndic (Admin):
- ✅ Dashboard avec statistiques de sa résidence assignée
- ✅ **NE PEUT PAS** créer, modifier ou supprimer de résidences
- ✅ Peut ajouter des propriétaires/résidents dans sa résidence
- ✅ Gestion des charges (création, publication, répartition)
- ✅ **Validation des paiements avec notes** (rôle clé)
- ✅ **Filtres et statistiques des paiements**
- ✅ Gestion de la maintenance
- ✅ Carnet d'entretien
- ✅ Assemblées générales et résolutions
- ✅ Gestion des contentieux
- ✅ Documents et actualités
- ✅ Accès aux deux fils d'actualité:
  - **Fil d'actualité** (pour tous)
  - **Actualités et annonces** (admin/syndic/propriétaires)

**Pages accessibles :**
- `/admin/dashboard` - Tableau de bord de sa résidence
- `/admin/finances` - Gestion financière (charges et paiements)
- `/admin/maintenance` - Gestion de la maintenance
- `/admin/assemblies` - Assemblées générales
- `/admin/documents` - Gestion des documents
- `/admin/maintenance-log` - Carnet d'entretien
- `/admin/feed` - Fil d'actualité
- `/admin/announcements` - Actualités et annonces
- `/admin/users` - Gestion des utilisateurs de sa résidence

---

## 🏠 Compte Propriétaire

Utilisez ce compte pour tester les fonctionnalités propriétaire.

### Propriétaire 1
**Email :** `owner@mysindic.ma`  
**Mot de passe :** `Owner123!`
- **Résidence :** Résidence Les Jardins
- **Unité :** A101 (Appartement F3, 85.5 m²)
- **Rôle :** Propriétaire (owner)

### Accès Propriétaire:
- ✅ Dashboard propriétaire
- ✅ Accès aux deux fils d'actualité:
  - **Fil d'actualité** (pour tous)
  - **Actualités et annonces** (admin/syndic/propriétaires)
- ✅ Peut créer/ajouter/bloquer/supprimer un résident dans son unité
- ✅ Demandes de maintenance (création et suivi)
- ✅ Consultation des finances de sa résidence
- ✅ Consultation des charges et solde du compte
- ✅ Déclaration de paiements
- ✅ Accès aux assemblées générales (participation et vote)
- ✅ Consultation des documents

**Pages accessibles :**
- `/resident/dashboard` - Tableau de bord propriétaire
- `/resident/feed` - Fil d'actualité (pour tous)
- `/resident/announcements` - Actualités et annonces (propriétaires)
- `/resident/maintenance` - Demandes de maintenance
- `/resident/finances` - Mes finances
- `/resident/assemblies` - Assemblées générales
- `/resident/documents` - Documents

---

## 👤 Comptes Résidents

Utilisez ces comptes pour tester les fonctionnalités résidents (accès limité).

### Résident 1
**Email :** `resident@mysindic.ma`  
**Mot de passe :** `Resident123!`
- **Résidence :** Résidence Les Jardins
- **Unité :** A102 (Appartement F2, 65.0 m²)
- **Rôle :** Résident (resident)

### Résident 2
**Email :** `karim@mysindic.ma`  
**Mot de passe :** `Resident123!`
- **Résidence :** Résidence Les Jardins
- **Unité :** A201 (Appartement F4, 110.0 m²)
- **Rôle :** Résident (resident)

### Accès Résident (LIMITÉ):
- ✅ Dashboard résident
- ✅ **Fil d'actualité uniquement** (ne peut PAS accéder aux actualités et annonces)
- ✅ Demandes de maintenance (création, commentaires et suivi)
- ✅ **NE PEUT PAS** accéder aux finances
- ✅ **NE PEUT PAS** accéder aux assemblées générales
- ✅ **NE PEUT PAS** accéder aux documents

**Pages accessibles :**
- `/resident/dashboard` - Tableau de bord résident
- `/resident/feed` - Fil d'actualité (pour tous)
- `/resident/maintenance` - Demandes de maintenance

**Pages bloquées :**
- ❌ `/resident/announcements` - Actualités et annonces (403 Forbidden)
- ❌ `/resident/finances` - Finances
- ❌ `/resident/assemblies` - Assemblées générales
- ❌ `/resident/documents` - Documents

---

## 🏢 Résidence de Démonstration

**Nom :** Résidence Les Jardins  
**Adresse :** 123 Avenue Mohammed V  
**Ville :** Casablanca  
**Code Postal :** 20000  
**Total d'unités :** 20

### Unités créées:
1. **A101** - F3, 85.5 m² (Propriétaire: owner@mysindic.ma)
2. **A102** - F2, 65.0 m² (Résident: resident@mysindic.ma)
3. **A201** - F4, 110.0 m² (Résident: karim@mysindic.ma)
4. **A202** - F3, 85.0 m² (Vacant)
5. **B101** - F2, 60.0 m² (Vacant)

---

## 📰 Deux Fils d'Actualité

L'application Shabaka Syndic dispose de **deux fils d'actualité distincts** :

### 1. Fil d'Actualité (news_type='feed')
- **Accès :** Tous les utilisateurs (superadmin, admin, owner, resident)
- **Usage :** Actualités générales, événements de la résidence, informations pour tous
- **Routes :** 
  - Admin: `/admin/feed`
  - Résident: `/resident/feed`
- **Exemples :** 
  - Horaires de la piscine
  - Bienvenue sur Shabaka Syndic
  - Événements communautaires

### 2. Actualités et Annonces (news_type='announcement')
- **Accès :** Superadmin, Admin (syndic), Propriétaires uniquement
- **Bloqué pour :** Résidents simples (role='resident')
- **Usage :** Annonces officielles, assemblées générales, travaux importants, décisions de copropriété
- **Routes :**
  - Admin: `/admin/announcements`
  - Propriétaire: `/resident/announcements` (accessible)
  - Résident: `/resident/announcements` (403 Forbidden)
- **Exemples :**
  - Prochaine Assemblée Générale
  - Travaux de rénovation de la piscine
  - Vote du budget prévisionnel

---

## 🔗 Endpoints API

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion
- `GET /api/auth/me` - Utilisateur actuel
- `GET /api/auth/check` - Vérification de l'authentification

### Admin (Superadmin + Admin Syndic)
- `GET /api/admin/dashboard` - Statistiques
- `GET /api/admin/residences` - Liste des résidences (filtrées selon rôle)
- `POST /api/admin/residences` - Créer une résidence (superadmin uniquement)
- `GET /api/admin/users` - Liste des utilisateurs
- `POST /api/admin/charges` - Créer un appel de fonds
- `GET /api/admin/news?type=feed` - Fil d'actualité (admin)
- `GET /api/admin/news?type=announcement` - Actualités et annonces (admin)
- Et 25+ autres endpoints...

### Résident (Propriétaire + Résident)
- `GET /api/resident/dashboard` - Dashboard résident
- `GET /api/resident/news?type=feed` - Fil d'actualité (tous)
- `GET /api/resident/news?type=announcement` - Actualités et annonces (owner uniquement, resident=403)
- `POST /api/resident/maintenance` - Créer une demande
- `GET /api/resident/charges` - Mes charges (owner uniquement)
- `POST /api/resident/payments` - Déclarer un paiement (owner uniquement)
- Et 18+ autres endpoints...

### Utilitaires
- `GET /health` - Santé de l'application
- `GET /api/info` - Informations sur l'API

---

## 🧪 Comment Tester les Rôles

### 1. Tester en tant que Superadmin

```bash
# Connexion
1. Aller sur http://votre-url/login
2. Entrer: admin@mysindic.ma / Admin123!
3. Vous serez redirigé vers /admin/dashboard

# Tester les fonctionnalités
- Voir TOUTES les résidences
- Créer une nouvelle résidence
- Ajouter des unités
- Créer des charges
- Gérer tous les utilisateurs
- Accéder au fil d'actualité ET aux actualités/annonces
```

### 2. Tester en tant qu'Admin Syndic

```bash
# Connexion
1. Aller sur http://votre-url/login
2. Entrer: admin.syndic@mysindic.ma / Admin123!
3. Vous serez redirigé vers /admin/dashboard

# Tester les fonctionnalités
- Voir UNIQUEMENT sa résidence assignée (Résidence Les Jardins)
- NE PEUT PAS créer/modifier/supprimer de résidences
- Gérer les charges de sa résidence
- Valider les paiements
- Accéder au fil d'actualité ET aux actualités/annonces
```

### 3. Tester en tant que Propriétaire

```bash
# Connexion
1. Aller sur http://votre-url/login
2. Entrer: owner@mysindic.ma / Owner123!
3. Vous serez redirigé vers /resident/dashboard

# Tester les fonctionnalités
- Créer une demande de maintenance
- Consulter le solde et les charges
- Déclarer un paiement
- Accéder au fil d'actualité ET aux actualités/annonces
- Participer aux assemblées générales
```

### 4. Tester en tant que Résident

```bash
# Connexion
1. Aller sur http://votre-url/login
2. Entrer: resident@mysindic.ma / Resident123!
3. Vous serez redirigé vers /resident/dashboard

# Tester les fonctionnalités (LIMITÉES)
- Créer une demande de maintenance
- Voir le fil d'actualité uniquement
- NE PEUT PAS accéder aux actualités/annonces (403)
- NE PEUT PAS voir les finances
- NE PEUT PAS voir les assemblées générales
```

---

## 📊 Données de Test Disponibles

L'auto-initialisation crée automatiquement:

- ✅ 6 comptes utilisateurs:
  - 1 superadmin
  - 2 admins syndic (bureau)
  - 1 propriétaire
  - 2 résidents
- ✅ 1 résidence (Résidence Les Jardins)
- ✅ 5 unités (A101, A102, A201, A202, B101)
- ✅ 1 appel de fonds avec répartition automatique
- ✅ 2 paiements validés
- ✅ 3 demandes de maintenance avec commentaires
- ✅ 2 entrées du carnet d'entretien
- ✅ 4 actualités:
  - 2 dans le fil d'actualité (pour tous)
  - 2 dans actualités et annonces (admin/syndic/propriétaires uniquement)
- ✅ Base de données PostgreSQL avec 19 tables

---

## 📋 Résumé des Permissions par Rôle

| Fonctionnalité | Superadmin | Admin Syndic | Propriétaire | Résident |
|---|---|---|---|---|
| **Dashboard** | ✅ Toutes résidences | ✅ Sa résidence | ✅ Son unité | ✅ Basique |
| **Fil d'actualité** | ✅ | ✅ | ✅ | ✅ |
| **Actualités et annonces** | ✅ | ✅ | ✅ | ❌ |
| **Créer/Modifier/Supprimer résidence** | ✅ | ❌ | ❌ | ❌ |
| **Gérer résidence assignée** | ✅ | ✅ | ❌ | ❌ |
| **Ajouter propriétaires/résidents** | ✅ | ✅ | ✅ (son unité) | ❌ |
| **Maintenance** | ✅ | ✅ | ✅ | ✅ (limité) |
| **Carnet d'entretien** | ✅ | ✅ | ❌ | ❌ |
| **Finances** | ✅ | ✅ | ✅ (consultation) | ❌ |
| **Validation paiements** | ✅ | ✅ | ❌ | ❌ |
| **Assemblées générales** | ✅ | ✅ | ✅ | ❌ |
| **Contentieux** | ✅ | ✅ | ❌ | ❌ |
| **Documents** | ✅ | ✅ | ✅ | ❌ |
| **Paramètres** | ✅ | ❌ | ❌ | ❌ |

---

## ⚠️ Notes Importantes

1. **Auto-initialisation :** La base de données s'initialise automatiquement au premier démarrage - aucune action manuelle requise!
2. **Idempotence :** Si un admin existe déjà, le système ne réinitialise pas les données
3. **Sécurité :** Ces identifiants sont pour la démonstration uniquement. Changez-les en production!
4. **Réinitialisation manuelle :** Pour forcer une réinitialisation, exécutez `python reset_db.py`
5. **Rôles :** Les 4 rôles sont `superadmin`, `admin` (bureau syndic), `owner` (propriétaire), `resident` (résident)
6. **Deux fils d'actualité :** Le système distingue clairement le fil d'actualité (pour tous) des actualités et annonces (admin/syndic/propriétaires uniquement)

---

## 🆘 Besoin d'Aide?

Si vous avez des problèmes:
1. Vérifiez que le workflow est en cours d'exécution
2. Vérifiez `/health` pour voir si la base de données est connectée
3. Consultez les logs du workflow
4. Réinitialisez la base de données avec `python init_db.py`

---

**Dernière mise à jour :** 21 novembre 2025  
**Version de l'application :** 0.1.0  
**Auto-initialisation :** ✅ Activée  
**Rôles implémentés :** 4 (superadmin, admin, owner, resident)  
**Fils d'actualité :** 2 (feed + announcements)
