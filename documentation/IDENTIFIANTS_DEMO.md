# 🔐 Shabaka Syndic - Identifiants de Démonstration

**Dernière mise à jour :** 25 octobre 2025

Ce document contient tous les identifiants de démonstration pour tester l'application Shabaka Syndic.

⚠️ **Auto-initialisation activée** - La base de données s'initialise automatiquement au premier démarrage!

---

## 👨‍💼 Compte Superadmin

Utilisez ce compte pour accéder à toutes les fonctionnalités d'administration.

**Email :** `admin@mysindic.ma`  
**Mot de passe :** `Admin123!`

### Accès Superadmin:
- ✅ Dashboard avec statistiques complètes
- ✅ Gestion des résidences (création, modification)
- ✅ Gestion des unités/lots
- ✅ Gestion des utilisateurs
- ✅ Appels de fonds et répartition des charges
- ✅ Validation des paiements
- ✅ Gestion de la maintenance
- ✅ Carnet d'entretien
- ✅ Assemblées générales et résolutions
- ✅ Documents et actualités
- ✅ Sondages et contentieux

**Pages accessibles :**
- `/admin/dashboard` - Tableau de bord
- `/admin/residences` - Gestion des résidences
- `/admin/finances` - Gestion financière
- `/admin/maintenance` - Gestion de la maintenance
- `/admin/users` - Gestion des utilisateurs
- `/admin/assemblies` - Assemblées générales
- `/admin/documents` - Gestion des documents
- `/admin/maintenance-log` - Carnet d'entretien

---

## 🏠 Comptes Résidents

Utilisez ces comptes pour tester les fonctionnalités résidents.

### Résident 1
**Email :** `resident@mysindic.ma`  
**Mot de passe :** `Resident123!`
- **Résidence :** Résidence Les Jardins
- **Unité :** A101 (Appartement F3, 85.5 m²)
- **Tantièmes :** 50/1000

### Résident 2
**Email :** `fatima@mysindic.ma`  
**Mot de passe :** `Resident123!`
- **Résidence :** Résidence Les Jardins
- **Unité :** A102 (Appartement F2, 65.0 m²)
- **Tantièmes :** 40/1000

### Résident 3
**Email :** `karim@mysindic.ma`  
**Mot de passe :** `Resident123!`
- **Résidence :** Résidence Les Jardins
- **Unité :** A201 (Appartement F4, 110.0 m²)
- **Tantièmes :** 65/1000

### Accès Résident:
- ✅ Dashboard personnalisé
- ✅ Consultation des actualités de la résidence
- ✅ Demandes de maintenance (création et suivi)
- ✅ Consultation des charges et solde du compte
- ✅ Déclaration de paiements
- ✅ Historique des paiements
- ✅ Accès aux documents de la résidence
- ✅ Participation aux sondages
- ✅ Consultation des assemblées générales
- ✅ Vote sur les résolutions
- ✅ Confirmation de présence aux AG
- ✅ Consultation du carnet d'entretien

**Pages accessibles :**
- `/resident/dashboard` - Tableau de bord résident
- `/resident/news` - Actualités de la résidence
- `/resident/maintenance` - Demandes de maintenance
- `/resident/finances` - Mes finances
- `/resident/assemblies` - Assemblées générales
- `/resident/documents` - Documents

---

## 🏢 Résidence de Démonstration

**Nom :** Résidence Les Jardins  
**Adresse :** 123 Avenue Mohammed V  
**Ville :** Casablanca  
**Code Postal :** 20000  
**Total d'unités :** 20  
**Total tantièmes :** 1000

### Unités créées:
1. **A101** - F3, 85.5 m², 50 tantièmes (Résident: resident@mysindic.ma)
2. **A102** - F2, 65.0 m², 40 tantièmes (Résident: fatima@mysindic.ma)
3. **A201** - F4, 110.0 m², 65 tantièmes (Résident: karim@mysindic.ma)
4. **B101** - Studio, 45.0 m², 25 tantièmes (Vacant)
5. **B102** - F5, 135.0 m², 80 tantièmes (Vacant)

---

## 🔗 Endpoints API

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `POST /api/auth/logout` - Déconnexion
- `GET /api/auth/me` - Utilisateur actuel
- `GET /api/auth/check` - Vérification de l'authentification

### Admin (Superadmin uniquement)
- `GET /api/admin/dashboard` - Statistiques
- `GET /api/admin/residences` - Liste des résidences
- `POST /api/admin/residences` - Créer une résidence
- `GET /api/admin/users` - Liste des utilisateurs
- `POST /api/admin/charges` - Créer un appel de fonds
- `POST /api/admin/charges/{id}/publish` - Publier une charge
- Et 25+ autres endpoints...

### Résident
- `GET /api/resident/dashboard` - Dashboard résident
- `GET /api/resident/news` - Actualités
- `POST /api/resident/maintenance` - Créer une demande
- `GET /api/resident/charges` - Mes charges
- `POST /api/resident/payments` - Déclarer un paiement
- Et 18+ autres endpoints...

### Utilitaires
- `GET /health` - Santé de l'application
- `GET /api/info` - Informations sur l'API

---

## 🧪 Comment Tester

### 1. Tester en tant que Superadmin

```bash
# Connexion
1. Aller sur http://votre-url/login
2. Entrer: admin@mysindic.ma / Admin123!
3. Vous serez redirigé vers /admin/dashboard

# Tester les fonctionnalités
- Créer une nouvelle résidence
- Ajouter des unités
- Créer des charges
- Gérer les utilisateurs
```

### 2. Tester en tant que Résident

```bash
# Connexion
1. Aller sur http://votre-url/login
2. Entrer: resident@mysindic.ma / Resident123!
3. Vous serez redirigé vers /resident/dashboard

# Tester les fonctionnalités
- Créer une demande de maintenance
- Consulter le solde
- Déclarer un paiement
- Voir les actualités
```

### 3. Tester l'API avec cURL

```bash
# Connexion superadmin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@mysindic.ma","password":"Admin123!"}' \
  -c cookies.txt

# Dashboard admin
curl http://localhost:5000/api/admin/dashboard \
  -b cookies.txt

# Liste des résidences
curl http://localhost:5000/api/admin/residences \
  -b cookies.txt
```

---

## 📊 Données de Test Disponibles

L'auto-initialisation crée automatiquement:

- ✅ 4 comptes utilisateurs (1 superadmin + 3 résidents)
- ✅ 1 résidence (Résidence Les Jardins)
- ✅ 5 unités (A101, A102, A201, B101, B102)
- ✅ 1 appel de fonds avec répartition automatique
- ✅ 2 paiements validés
- ✅ 2 demandes de maintenance avec logs
- ✅ 2 actualités publiées
- ✅ Base de données PostgreSQL avec 18 tables

---

## ⚠️ Notes Importantes

1. **Auto-initialisation :** La base de données s'initialise automatiquement au premier démarrage - aucune action manuelle requise!
2. **Idempotence :** Si un admin existe déjà, le système ne réinitialise pas les données
3. **Sécurité :** Ces identifiants sont pour la démonstration uniquement. Changez-les en production!
4. **Réinitialisation manuelle :** Pour forcer une réinitialisation, exécutez `python reset_db.py`
5. **Nouveaux comptes :** Seuls les superadmins peuvent créer de nouveaux comptes résidents
6. **Rôles :** Les rôles sont `superadmin` ou `resident`

---

## 🆘 Besoin d'Aide?

Si vous avez des problèmes:
1. Vérifiez que le workflow est en cours d'exécution
2. Vérifiez `/health` pour voir si la base de données est connectée
3. Consultez les logs du workflow
4. Réinitialisez la base de données avec `python init_db.py`

---

**Dernière mise à jour :** 25 octobre 2025  
**Version de l'application :** 0.1.0  
**Auto-initialisation :** ✅ Activée
