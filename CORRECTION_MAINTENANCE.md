# Correction de la fonctionnalité "Nouvelle Demande" de Maintenance

## Problème identifié

Lorsqu'un résident cliquait sur le bouton "Nouvelle Demande" dans la page `/resident/maintenance`, rien ne se passait. Le modal ne s'ouvrait pas.

## Cause du problème

Le code HTML utilisait `Shabaka Syndic.openModal()` (avec un espace) alors que l'objet JavaScript global est défini comme `ShabakaSyndic` (sans espace) dans le fichier `frontend/static/js/main.js`.

Exemple d'erreur dans le code:
```html
<button onclick="Shabaka Syndic.openModal('createRequestModal')">
```

Au lieu de:
```html
<button onclick="ShabakaSyndic.openModal('createRequestModal')">
```

## Corrections apportées

### 1. Correction du nom d'objet JavaScript

- ✅ Remplacé toutes les occurrences de `Shabaka Syndic.` par `ShabakaSyndic.` dans tous les fichiers HTML
- ✅ Fichiers affectés : 16 fichiers template HTML
- ✅ Méthode utilisée : Script sed pour remplacement global

### 2. Création du dossier uploads

- ✅ Créé le dossier `frontend/static/uploads/maintenance/` pour stocker les images uploadées par les résidents

### 3. Vérifications effectuées

- ✅ Le bouton "Nouvelle Demande" utilise maintenant `ShabakaSyndic.openModal()`
- ✅ Le formulaire de soumission envoie correctement une requête POST à `/api/resident/maintenance`
- ✅ La route backend est configurée pour recevoir les données multipart/form-data (pour l'upload d'images)
- ✅ Le workflow a été redémarré et fonctionne correctement

## Fonctionnement après correction

1. **Ouverture du modal** : Cliquer sur "Nouvelle Demande" ouvre le modal avec le formulaire
2. **Remplissage du formulaire** : Le résident peut remplir tous les champs requis
3. **Upload d'image** : Le résident peut optionnellement ajouter une photo du problème
4. **Soumission** : Le formulaire envoie une requête POST avec FormData
5. **Traitement** : Le backend crée la demande et génère un numéro de suivi unique
6. **Notification** : Le résident reçoit un toast de confirmation et la liste des demandes est rechargée

## Code du gestionnaire de soumission

```javascript
document.getElementById('requestForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('title', document.getElementById('request-title').value);
    formData.append('description', document.getElementById('request-description').value);
    formData.append('zone', document.getElementById('request-zone').value);
    formData.append('zone_details', document.getElementById('request-zone-details').value);
    formData.append('priority', document.getElementById('request-priority').value);
    
    const imageFile = document.getElementById('request-image').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
    }
    
    try {
        const response = await fetch('/api/resident/maintenance', {
            method: 'POST',
            credentials: 'same-origin',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            ShabakaSyndic.showToast('Demande créée avec succès', 'success');
            ShabakaSyndic.closeModal('createRequestModal');
            document.getElementById('requestForm').reset();
            clearImage();
            loadMyRequests();
        } else {
            ShabakaSyndic.showToast(data.error || 'Erreur lors de la création', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        ShabakaSyndic.showToast('Erreur de connexion', 'error');
    }
});
```

## Tests recommandés

Pour tester la fonctionnalité:

1. Se connecter en tant que résident
2. Aller sur `/resident/maintenance`
3. Cliquer sur "Nouvelle Demande" → Le modal devrait s'ouvrir
4. Remplir le formulaire avec:
   - Titre: "Test de demande"
   - Description: "Ceci est un test"
   - Zone: Sélectionner une zone
   - Priorité: Sélectionner une priorité
5. Optionnel: Ajouter une photo
6. Cliquer sur "Créer la demande"
7. Vérifier que:
   - Un toast de succès apparaît
   - Le modal se ferme
   - La demande apparaît dans la liste
   - Un numéro de suivi a été généré

## Fichiers modifiés

- `frontend/templates/resident/maintenance.html` (et 15 autres templates)
- Création du dossier `frontend/static/uploads/maintenance/`
