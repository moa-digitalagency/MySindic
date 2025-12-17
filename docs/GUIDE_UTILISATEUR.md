# Guide Utilisateur - Shabaka Syndic

Ce guide présente l'utilisation de Shabaka Syndic selon votre profil. L'application propose quatre niveaux d'accès avec des fonctionnalités adaptées à chaque rôle.

## Table des Matières

1. [Connexion et Navigation](#connexion-et-navigation)
2. [Profil Super Admin](#profil-super-admin)
3. [Profil Syndic (Admin)](#profil-syndic-admin)
4. [Profil Propriétaire](#profil-propriétaire)
5. [Profil Résident](#profil-résident)

---

## Connexion et Navigation

### Accéder à l'Application

Ouvrez votre navigateur et rendez-vous sur l'adresse de votre installation Shabaka Syndic. La page d'accueil présente les fonctionnalités principales et propose deux boutons : "Se connecter" et "En savoir plus".

### Se Connecter

1. Cliquez sur "Se connecter" ou "Connexion"
2. Entrez votre adresse email
3. Entrez votre mot de passe
4. Cochez "Se souvenir de moi" si vous utilisez un appareil personnel
5. Cliquez sur "Connexion"

Après connexion, vous êtes redirigé vers votre tableau de bord correspondant à votre rôle.

### Navigation Générale

Le menu latéral (sur ordinateur) ou le menu hamburger (sur mobile) permet d'accéder aux différentes sections. Les éléments du menu varient selon votre profil.

---

## Profil Super Admin

Le Super Admin dispose d'un accès complet à toutes les fonctionnalités et peut gérer l'ensemble des résidences.

### Tableau de Bord

Le tableau de bord affiche les statistiques globales :
- Nombre total de résidences
- Nombre d'utilisateurs
- Nombre de lots
- Total des impayés
- Demandes de maintenance en attente

### Gestion des Résidences

**Créer une résidence**

1. Menu "Résidences" → Bouton "Nouvelle résidence"
2. Un assistant en plusieurs étapes vous guide :
   - Informations générales (nom, adresse, ville)
   - Configuration des bâtiments/divisions
   - Création des lots
3. Validez chaque étape puis finalisez

**Modifier une résidence**

1. Liste des résidences → Cliquez sur la résidence
2. Bouton "Modifier"
3. Modifiez les informations souhaitées
4. Enregistrez

**Gérer les lots**

Chaque résidence contient des lots (appartements, commerces, parkings). Pour chaque lot, vous pouvez définir :
- Numéro du lot
- Étage et bâtiment
- Type (appartement, commerce, parking)
- Surface
- Informations du propriétaire

### Gestion des Utilisateurs

**Consulter les utilisateurs**

Menu "Utilisateurs" → Liste de tous les comptes avec leur rôle, résidence et statut.

**Modifier un utilisateur**

1. Cliquez sur un utilisateur
2. Modifiez le rôle, la résidence ou le lot associé
3. Activez ou désactivez le compte si nécessaire

**Rôles disponibles**
- Super Admin : accès total
- Admin (Syndic) : gestion d'une ou plusieurs résidences assignées
- Propriétaire : accès étendu à sa résidence
- Résident : accès limité (maintenance, fil d'actualité)

### Gestion Financière

**Créer un appel de fonds**

1. Menu "Finances" → Bouton "Nouvel appel de fonds"
2. Sélectionnez la résidence
3. Remplissez : titre, type de charge, montant total, période, date limite
4. Enregistrez (statut "brouillon")

**Publier et répartir**

1. Ouvrez l'appel de fonds créé
2. Cliquez sur "Publier"
3. Le système calcule automatiquement la répartition par lot
4. Les résidents reçoivent une notification

**Valider les paiements**

1. Menu "Finances" → Onglet "Paiements"
2. Les paiements en attente apparaissent
3. Consultez le justificatif si fourni
4. Cliquez sur "Valider" ou "Rejeter"

### Assemblées Générales

**Créer une AG**

1. Menu "Assemblées" → Bouton "Nouvelle AG"
2. Remplissez : titre, type (ordinaire/extraordinaire), date, lieu
3. Définissez le mode : présentiel, en ligne ou hybride
4. Enregistrez

**Ajouter des résolutions**

1. Ouvrez l'assemblée créée
2. Section "Résolutions" → "Ajouter une résolution"
3. Définissez le titre, la description et le type de vote

**Envoyer les convocations**

Bouton "Envoyer les convocations" → Les invitations partent aux résidents concernés.

**Gérer les présences et votes**

Pendant l'AG, vous pouvez :
- Marquer les présents
- Lancer le vote sur chaque résolution
- Consulter les résultats en temps réel

### Paramètres

Le menu "Paramètres" permet de :
- Configurer l'apparence de l'application
- Gérer les notifications
- Injecter du code personnalisé (analytics, widgets)
- Définir les rôles et permissions

---

## Profil Syndic (Admin)

L'administrateur syndic gère les résidences qui lui sont assignées par le Super Admin.

### Tableau de Bord

Affiche les statistiques uniquement pour vos résidences :
- Résidences sous votre gestion
- Nombre de lots
- Impayés
- Demandes de maintenance

### Vos Résidences

Vous accédez uniquement aux résidences assignées. Vous pouvez :
- Consulter les informations
- Gérer les lots
- Modifier les données (selon permissions)

### Gestion de la Maintenance

**Consulter les demandes**

1. Menu "Maintenance"
2. Filtrez par statut : en attente, en cours, résolu
3. Cliquez sur une demande pour voir les détails

**Traiter une demande**

1. Ouvrez la demande
2. Changez le statut (en cours, résolu, rejeté)
3. Ajoutez des notes internes
4. Assignez un prestataire si nécessaire
5. Ajoutez des commentaires visibles par le résident

**Carnet d'entretien**

Menu "Carnet d'entretien" → Historique de toutes les interventions sur la résidence avec :
- Type d'intervention
- Prestataire
- Coût
- Date de prochaine intervention prévue

### Finances

Mêmes fonctionnalités que le Super Admin, limitées à vos résidences.

### Communication

**Publier une actualité**

1. Menu "Fil d'actualité" ou "Annonces"
2. Bouton "Nouvelle publication"
3. Rédigez le titre et le contenu
4. Choisissez le type :
   - Fil d'actualité : visible par tous
   - Annonce : visible par propriétaires et admins uniquement
5. Publiez

**Créer un sondage**

1. Menu correspondant → "Nouveau sondage"
2. Rédigez la question
3. Ajoutez les options de réponse
4. Définissez la période de vote
5. Publiez

---

## Profil Propriétaire

Le propriétaire dispose d'un accès étendu concernant son lot et sa résidence.

### Tableau de Bord

Votre tableau de bord affiche :
- Solde de votre compte (charges dues - paiements)
- Dernières actualités
- Prochaines assemblées générales
- Vos demandes de maintenance récentes

### Finances

**Consulter vos charges**

Menu "Finances" → Liste de vos appels de fonds avec :
- Montant dû
- Statut (payé/impayé)
- Date limite

**Consulter votre solde**

Le solde indique votre situation financière :
- Solde positif (crédit) : vous êtes en avance sur vos paiements
- Solde négatif (débit) : vous avez des charges en attente
- Équilibré : tout est à jour

**Déclarer un paiement**

1. Menu "Finances" → "Déclarer un paiement"
2. Indiquez le montant, la méthode (virement, chèque, espèces)
3. Joignez un justificatif (photo du chèque, capture virement)
4. Envoyez → Le syndic validera

**Historique des paiements**

Consultez tous vos paiements passés avec leur statut de validation.

### Maintenance

**Créer une demande**

1. Menu "Maintenance" → "Nouvelle demande"
2. Sélectionnez la zone concernée (appartement, escalier, parking...)
3. Décrivez le problème
4. Ajoutez une photo si possible
5. Définissez la priorité
6. Envoyez

**Suivre vos demandes**

La liste affiche vos demandes avec leur statut. Cliquez sur une demande pour voir les commentaires du syndic et l'avancement.

### Assemblées Générales

**Consulter les AG**

Menu "Assemblées" → Liste des assemblées passées et à venir.

**Confirmer votre présence**

Pour une AG à venir, cliquez sur "Confirmer ma présence" pour indiquer si vous serez présent physiquement ou en ligne.

**Voter sur les résolutions**

Pendant ou après l'AG (selon configuration), vous pouvez voter :
- Pour
- Contre
- Abstention

### Actualités et Annonces

Vous avez accès :
- Au fil d'actualité général (informations pratiques)
- Aux annonces officielles (décisions, travaux votés)

Vous pouvez également publier dans le fil d'actualité pour partager des informations avec les autres résidents.

### Documents

Accédez aux documents publics de la résidence :
- Règlement de copropriété
- Procès-verbaux d'AG
- Contrats et attestations

---

## Profil Résident

Le résident (locataire ou occupant non-propriétaire) dispose d'un accès aux fonctions essentielles.

### Tableau de Bord

Affiche :
- Vos demandes de maintenance récentes
- Le fil d'actualité de la résidence
- Les prochaines assemblées (consultation uniquement)

### Maintenance

**Signaler un problème**

1. Menu "Maintenance" → "Nouvelle demande"
2. Choisissez la zone (parties communes ou votre logement)
3. Décrivez le problème en détail
4. Ajoutez une photo
5. Envoyez

**Suivre vos demandes**

Consultez l'état de vos signalements. Le syndic peut ajouter des commentaires pour vous tenir informé.

**Ajouter des informations**

Sur une demande existante, vous pouvez ajouter des commentaires pour apporter des précisions.

### Fil d'Actualité

Accédez aux informations générales publiées par le syndic :
- Horaires des espaces communs
- Informations pratiques
- Événements de la résidence

Les annonces officielles (travaux, décisions d'AG) ne sont pas accessibles aux résidents simples.

### Documents

Consultez les documents publics mis à disposition par le syndic.

### Assemblées

Vous pouvez consulter les assemblées générales mais le droit de vote est réservé aux propriétaires.

---

## Conseils d'Utilisation

### Mot de Passe Oublié

Contactez votre syndic ou l'administrateur pour réinitialiser votre mot de passe.

### Problème de Connexion

- Vérifiez que votre email est correct
- Vérifiez la casse du mot de passe
- Videz le cache de votre navigateur
- Contactez le support si le problème persiste

### Bonnes Pratiques

1. **Changez votre mot de passe** régulièrement
2. **Consultez le tableau de bord** pour rester informé
3. **Déclarez vos paiements** rapidement pour garder votre compte à jour
4. **Documentez vos demandes** de maintenance avec des photos
5. **Participez aux AG** pour exercer votre droit de vote
