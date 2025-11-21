# ⚠️ Problèmes Critiques à Corriger

**Date :** 21 novembre 2025  
**Identifiés par :** Révision d'architecture

## 🚨 Problèmes Critiques Restants

### 1. Scoping des Résidences pour les Admins (CRITIQUE)

**Problème :** Les routes API admin ne filtrent pas les données par résidence assignée. Un admin peut actuellement voir les données de toutes les résidences au lieu de voir uniquement celles de sa résidence assignée.

**Impact :** Violation des spécifications - les admins doivent gérer uniquement leur résidence assignée.

**Fichiers concernés :**
- `backend/routes/admin.py` - Routes dashboard, finances, maintenance, etc.
- Toutes les routes API `/api/admin/*` qui récupèrent des données

**Solution requise :**
```python
# Au lieu de:
total_residences = Residence.query.count()

# Pour les admins, filtrer par résidence assignée:
if current_user.is_superadmin():
    total_residences = Residence.query.count()
else:
    # Admin - voir uniquement sa résidence assignée
    assigned_residences = current_user.get_assigned_residences()
    total_residences = len(assigned_residences)
```

**Routes à corriger :**
- `/admin/dashboard` (GET)
- `/api/admin/residences` (GET, POST, PUT, DELETE)
- `/api/admin/finances` (GET)
- `/api/admin/charges` (GET, POST)
- `/api/admin/maintenance` (GET)
- `/api/admin/users` (GET)
- Toutes les autres routes admin qui récupèrent des données

### 2. Contrôle d'Accès aux Annonces (CRITIQUE)

**Problème :** Les routes d'annonces (`/resident/announcements` et `/api/resident/news?type=announcement`) ne bloquent pas les résidents au niveau blueprint/API. Un résident simple pourrait accéder directement aux endpoints d'annonces.

**Impact :** Les résidents peuvent contourner les contrôles de la page web et accéder aux annonces réservées aux admin/syndic/propriétaires.

**Fichiers concernés :**
- `backend/routes/resident.py` - Routes announcements
- `backend/routes/admin.py` - Routes announcements

**Solution requise :**
```python
# Ajouter un décorateur de garde de rôle
@resident_bp.route('/announcements')
@login_required
@owner_or_above_required  # Nouveau décorateur à créer
def announcements():
    if current_user.role == 'resident':
        abort(403, "Accès interdit - Propriétaires uniquement")
    # ...

# Ou bloquer dans l'API news
@resident_bp.route('/api/news')
@login_required
def get_news():
    news_type = request.args.get('type', 'feed')
    if news_type == 'announcement' and current_user.role == 'resident':
        return jsonify({'error': 'Accès interdit'}), 403
    # ...
```

### 3. Données de Démonstration - Vérification

**Problème potentiel :** L'architecte a mentionné des incohérences dans les totaux de charges et les distributions, mais une vérification manuelle semble montrer que les données sont cohérentes (50 000 MAD / 5 unités = 10 000 MAD par unité).

**Action requise :** Vérifier manuellement après initialisation que:
- Les charges totales correspondent aux distributions
- Les paiements sont bien assignés aux bons utilisateurs
- Tous les commentaires de maintenance référencent des utilisateurs valides

### 4. Documentation - Guide de Vérification

**Problème :** La documentation IDENTIFIANTS_DEMO.md manque de:
- Instructions de vérification étape par étape
- Description claire des limitations pour chaque rôle
- Quels menus/pages sont visibles pour chaque rôle

**Solution requise :**
- Ajouter une section "Comment Vérifier" avec des étapes précises
- Ajouter des captures d'écran ou descriptions de ce que chaque rôle peut voir
- Documenter les erreurs attendues (403, 404) pour chaque rôle

### 5. Tests End-to-End

**Problème :** Aucun test end-to-end documenté n'a été effectué pour vérifier:
- Que les 4 rôles fonctionnent correctement
- Que les 2 fils d'actualité sont bien séparés
- Que les permissions sont respectées
- Que le favicon s'affiche

**Action requise :**
- Créer un script de test ou une checklist de vérification
- Tester chaque rôle manuellement et documenter les résultats
- Vérifier que les résidents ne peuvent pas accéder aux annonces
- Vérifier que les admins ne voient que leur résidence

---

## ✅ Améliorations Complétées avec Succès

Les améliorations suivantes ont été complétées avec succès:

1. **Favicon ajouté** - Un favicon SVG moderne a été créé et intégré
2. **4 rôles vérifiés** - Les 4 rôles (superadmin, admin, owner, resident) existent dans le modèle User
3. **2 types de news** - Le système distingue `feed` (tous) et `announcement` (admin/owner)
4. **Données de démonstration** - 6 utilisateurs, 4 actualités, données complètes initialisées
5. **Documentation mise à jour** - IDENTIFIANTS_DEMO.md contient tous les identifiants et descriptions
6. **Nettoyage effectué** - Fichiers inutiles supprimés
7. **Workflow configuré** - L'application démarre correctement

---

## 📋 Prochaines Étapes Recommandées

### Priorité 1 (CRITIQUE):
1. Corriger le scoping des résidences pour les admins dans toutes les routes API
2. Ajouter des gardes de rôle stricts pour les annonces au niveau blueprint

### Priorité 2 (IMPORTANT):
3. Vérifier et corriger les données de démonstration si nécessaire
4. Compléter la documentation avec guide de vérification détaillé
5. Effectuer des tests end-to-end complets et documenter les résultats

### Priorité 3 (AMÉLIORATION):
6. Créer des décorateurs réutilisables pour les contrôles de rôle
7. Ajouter des tests automatisés pour les permissions
8. Améliorer les messages d'erreur pour les accès interdits

---

## 🔧 Exemple de Corrections à Appliquer

### Pour le scoping des résidences:

```python
# Dans backend/routes/admin.py
@admin_bp.route('/api/residences', methods=['GET'])
@login_required
@admin_or_superadmin_required
def get_residences():
    if current_user.is_superadmin():
        residences = Residence.query.all()
    else:
        # Admin - uniquement les résidences assignées
        assigned_res = ResidenceAdmin.query.filter_by(
            user_id=current_user.id
        ).all()
        residence_ids = [ra.residence_id for ra in assigned_res]
        residences = Residence.query.filter(
            Residence.id.in_(residence_ids)
        ).all()
    
    return jsonify([r.to_dict() for r in residences])
```

### Pour les gardes de rôle sur les annonces:

```python
# Dans backend/utils/decorators.py (à créer)
def owner_or_above_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['owner', 'admin', 'superadmin']:
            abort(403, "Accès réservé aux propriétaires et administrateurs")
        return f(*args, **kwargs)
    return decorated_function

# Dans backend/routes/resident.py
@resident_bp.route('/announcements')
@login_required
@owner_or_above_required  # Nouveau décorateur
def announcements():
    # ...
```

---

**Note :** Ces problèmes sont critiques et doivent être résolus avant la mise en production. Les améliorations effectuées lors de cette session (favicon, données de démo, documentation) sont complètes et fonctionnelles, mais les contrôles d'accès doivent être renforcés.
