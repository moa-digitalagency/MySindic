# Changelog - MySindic

## 2025-10-25

### 🐛 Corrections de Bugs

#### Wizard de Création de Résidence - Étape 3 Vide
**Problème:** Lors de la création d'une résidence, après avoir configuré le type de découpe et le nombre de divisions à l'étape 2, l'étape 3 "Configuration unités" s'affichait vide.

**Cause:** La fonction `saveStepData(2)` contenait un `return` précoce qui empêchait la sauvegarde des divisions si les éléments DOM `division_count` ou `division_prefix` n'étaient pas trouvés immédiatement.

**Solution:**
1. Suppression du `return` précoce qui bloquait la sauvegarde
2. Ajout de valeurs par défaut robustes (3 divisions, préfixe 'A')
3. Utilisation de l'opérateur de coalescence nulle (`?.`) pour accéder aux valeurs
4. Ajout de logs console détaillés pour le debugging
5. Ajout d'une notification toast de succès quand les divisions sont sauvegardées
6. Message d'erreur informatif avec debug si aucune division n'est configurée

**Fichiers modifiés:**
- `frontend/templates/admin/residence_wizard.html` - Fonction `saveStepData()` et `loadUnitsConfiguration()`

---

### 🎨 Améliorations de Design

#### Modernisation de la Page de Création de Résidence
**Changements:**
- Harmonisation de la palette de couleurs avec le dashboard (passage du violet au bleu #2563eb)
- Nouveau header séparé avec bordure et lien de retour animé
- Indicateur d'étapes modernisé avec coins arrondis et animations
- Formulaires avec meilleur espacement et focus amélioré
- Cartes de sélection avec effets hover élégants
- Boutons modernisés avec effet lift
- Design responsive pour mobile et tablette

**Fichiers modifiés:**
- `frontend/templates/admin/residence_wizard.html` - Refonte complète du CSS

---

### 🔧 Corrections Techniques

#### Template Admin Dashboard - Attribut Utilisateur Manquant
**Problème:** Erreur 500 sur `/admin/dashboard` - Le template tentait d'accéder à `current_user.username` qui n'existe pas dans le modèle User.

**Solution:** Remplacement de `current_user.username` par `current_user.first_name` et `current_user.last_name`

**Fichiers modifiés:**
- `frontend/templates/admin/dashboard.html` - Lignes 372-373

---

## Notes de Développement

### Architecture
- **Backend:** Flask avec SQLAlchemy
- **Frontend:** Jinja2 templates avec Tailwind CSS
- **Base de données:** PostgreSQL (Neon)

### Environnement
- Python 3.11
- Gunicorn avec hot-reload en développement
- Replit environment avec workflow automatisé
