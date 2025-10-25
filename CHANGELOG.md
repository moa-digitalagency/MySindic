# Changelog - MySindic

## 2025-10-25

### 🐛 Corrections de Bugs

#### Wizard de Création de Résidence - Étape 3 Vide (CORRIGÉ DÉFINITIVEMENT)
**Problème:** Lors de la création d'une résidence, après avoir configuré le type de découpe et le nombre de divisions à l'étape 2, l'étape 3 "Configuration unités" s'affichait vide. L'utilisateur était bloqué et ne pouvait pas progresser dans la création de la résidence.

**Cause:** Les divisions n'étaient créées dans `wizardData.divisions` que lors de l'appel à `saveStepData(2)`, mais cette fonction était parfois appelée trop tard ou les valeurs n'étaient pas correctement récupérées.

**Solution Finale (25 octobre 2025 - 15h40):**
1. **Création d'une fonction dédiée** `createDivisionsFromCurrentValues()` qui crée/recrée les divisions à partir des valeurs actuelles des champs
2. **Sauvegarde immédiate** : Appel de `createDivisionsFromCurrentValues()` dès la sélection du type de division dans `selectDivisionType()`
3. **Synchronisation continue** : Appel de `createDivisionsFromCurrentValues()` dans `updateDivisionPreview()` pour mettre à jour les divisions à chaque modification
4. **Simplification de saveStepData(2)** : Vérification simple et création des divisions si nécessaire
5. **Garantie de données** : Les divisions sont toujours créées AVANT de passer à l'étape 3

**Résultat:** L'étape 3 affiche maintenant systématiquement les formulaires de configuration des unités. Le problème est résolu une fois pour toutes.

**Fichiers modifiés:**
- `frontend/templates/admin/residence_wizard.html` - Fonctions `createDivisionsFromCurrentValues()`, `selectDivisionType()`, `updateDivisionPreview()`, et `saveStepData()`

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
