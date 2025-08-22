# 🕐 Guide de Configuration Exhaustive des Fréquences - micPlan

## 📋 Vue d'ensemble

La nouvelle configuration exhaustive des fréquences de micPlan couvre tous les cas de figure possibles pour la planification des postes de travail. Cette configuration avancée permet une gestion fine et flexible des besoins en personnel selon différents critères temporels, organisationnels et légaux.

## 🎯 Types de Fréquence Principaux

### 1. **Quotidien** 📅
- **Tous les jours** : Besoin constant, 7j/7
- **Jours ouvrés uniquement** : Lundi à Vendredi
- **Jours spécifiques** : Sélection personnalisée des jours
- **Gestion des jours fériés** : Règles spéciales pour les jours fériés

### 2. **Hebdomadaire** 📅
- **Fréquence** : 1x, 2x, 3x... par semaine
- **Jours consécutifs** : Option pour des périodes continues
- **Périodicité** : Toutes les X semaines
- **Sélection des jours** : Choix libre des jours de la semaine

### 3. **Bi-hebdomadaire** 🔄
- **Semaines paires/impaires** : Alternance automatique
- **Semaines spécifiques** : Numéros de semaines personnalisés
- **Alternance personnalisée** : Périodicité libre en semaines

### 4. **Mensuel** 📅
- **Fréquence** : 1x, 2x, 3x... par mois
- **Jours spécifiques** : Dates précises du mois (ex: 1, 15, 30)
- **Semaines spécifiques** : Semaines précises du mois (ex: 1, 3, 5)
- **Périodicité** : Tous les X mois

### 5. **Trimestriel** 📅
- **Fréquence** : 1x, 2x, 3x... par trimestre
- **Mois du trimestre** : Sélection des mois (ex: Janvier, Avril, Juillet, Octobre)
- **Sélection des jours** : Choix des jours de la semaine

### 6. **Semestriel** 📅
- **Fréquence** : 1x, 2x... par semestre
- **Mois du semestre** : Sélection des mois (ex: Janvier, Juillet)
- **Sélection des jours** : Choix des jours de la semaine

### 7. **Annuel** 📅
- **Fréquence** : 1x, 2x, 3x... par an
- **Mois de l'année** : Sélection des mois spécifiques
- **Sélection des jours** : Choix des jours de la semaine

### 8. **Personnalisé** ⚙️
- **Période libre** : Définition en jours (1 à 365)
- **Fréquence** : Nombre de fois dans cette période
- **Sélection des jours** : Choix des jours de la semaine

## ⏰ Granularité Temporelle

### **Périodes de la journée**
- **Matin** (8h-12h) : Besoin en personnel le matin
- **Après-midi** (14h-18h) : Besoin en personnel l'après-midi
- **Soirée** (18h-22h) : Besoin en personnel le soir
- **Nuit** (22h-6h) : Besoin en personnel la nuit

### **Créneaux horaires spécifiques**
- **Heure de début** : Début précis du créneau de travail
- **Heure de fin** : Fin précise du créneau de travail
- **Durée de travail** : Nombre d'heures par période
- **Gestion des pauses** : Durée et fréquence des pauses

## 🔄 Règles de Récurrence Avancées

### **Rotation d'équipes**
- **Nombre d'équipes** : 2 à 10 équipes
- **Type de rotation** : Alternance simple, par semaine, par mois
- **Équilibrage automatique** : Répartition équitable de la charge

### **Charge de travail**
- **Jours consécutifs maximum** : Limite pour éviter la surcharge
- **Jours de repos minimum** : Respect des temps de repos
- **Équilibrage automatique** : Répartition équitable des tâches

### **Gestion des compétences**
- **Compétences requises** : PCR, Extraction, Séquençage, Culture, Microscopie, Contrôle qualité
- **Niveau de compétence** : Débutant, Intermédiaire, Avancé, Expert
- **Matching automatique** : Affectation selon les compétences

### **Contraintes légales**
- **Heures hebdomadaires maximum** : Respect des limites légales (35-60h)
- **Période de repos minimum** : Temps de repos entre périodes (8-24h)
- **Conformité automatique** : Vérification des règles légales

## 🚨 Gestion des Exceptions

### **Jours fériés**
- **Travailler normalement** : Pas de changement
- **Décaler au jour ouvré suivant** : Report automatique
- **Exclure du planning** : Suppression automatique
- **Règle personnalisée** : Logique métier spécifique

### **Congés**
- **Exclure automatiquement** : Suppression des périodes de congés
- **Gérer manuellement** : Intervention humaine requise
- **Règle personnalisée** : Logique métier spécifique

### **Maintenance**
- **Exclure automatiquement** : Suppression des périodes de maintenance
- **Gérer manuellement** : Intervention humaine requise
- **Règle personnalisée** : Logique métier spécifique

### **Urgences**
- **Priorité absolue** : Remplacement automatique du planning
- **Gérer selon disponibilité** : Adaptation selon les ressources
- **Règle personnalisée** : Logique métier spécifique

## 📋 Intégration avec le Planning

### **Règles de planification**
- **Priorité** : Haute, Moyenne, Basse
- **Planification automatique** : Génération automatique des plannings
- **Algorithme** : Premier disponible, Équilibrage de charge, Rotation d'équipes, Optimisation des compétences

### **Notifications**
- **Types** : Planification confirmée, Conflit détecté, Modification de planning, Rappel de planning
- **Activation** : Choix des notifications souhaitées
- **Diffusion** : Envoi automatique selon les règles

### **Validation et approbation**
- **Niveau requis** : Superviseur, Chef d'équipe, Responsable, Directeur
- **Approbation automatique** : Si pas de conflit détecté
- **Workflow** : Processus de validation hiérarchique

### **Rapports et analyses**
- **Fréquence** : Quotidien, Hebdomadaire, Mensuel, Trimestriel
- **Types** : Utilisation des ressources, Charge de travail, Conformité, Performance
- **Génération** : Rapports automatiques selon la fréquence

## 🔧 Utilisation Pratique

### **Étape 1 : Sélection du type de fréquence**
1. Choisir le type principal (Quotidien, Hebdomadaire, etc.)
2. Configurer les paramètres spécifiques au type choisi
3. Sélectionner les jours de la semaine

### **Étape 2 : Configuration temporelle**
1. Définir les périodes de la journée
2. Optionnel : Configurer des créneaux horaires précis
3. Gérer les pauses si nécessaire

### **Étape 3 : Règles avancées**
1. Activer la rotation d'équipes si nécessaire
2. Configurer l'équilibrage de charge
3. Définir les exigences de compétences
4. Respecter les contraintes légales

### **Étape 4 : Gestion des exceptions**
1. Configurer le comportement pour les jours fériés
2. Gérer les congés et la maintenance
3. Définir les règles d'urgence

### **Étape 5 : Intégration planning**
1. Choisir l'algorithme de planification
2. Configurer les notifications
3. Définir le processus d'approbation
4. Configurer les rapports

## ✅ Validation et Sauvegarde

### **Validation automatique**
- Vérification des cohérences entre paramètres
- Contrôle des limites légales
- Validation des créneaux horaires
- Vérification des règles de récurrence

### **Résumé de configuration**
- Affichage de tous les paramètres configurés
- Vérification visuelle avant sauvegarde
- Confirmation de la configuration

### **Sauvegarde**
- Stockage de tous les paramètres dans la base de données
- Mise à jour de l'affichage des fréquences
- Intégration avec le système de planification

## 🎯 Cas d'Usage Exemples

### **Exemple 1 : Poste de PCR quotidien**
- **Type** : Quotidien
- **Jours** : Lundi à Vendredi
- **Périodes** : Matin + Après-midi
- **Compétences** : PCR (Avancé)
- **Rotation** : 2 équipes, alternance hebdomadaire

### **Exemple 2 : Poste de maintenance mensuel**
- **Type** : Mensuel
- **Fréquence** : 1x/mois
- **Jours** : 1er lundi du mois
- **Périodes** : Matin uniquement
- **Compétences** : Maintenance (Expert)

### **Exemple 3 : Poste de contrôle qualité bi-hebdomadaire**
- **Type** : Bi-hebdomadaire
- **Semaines** : Semaines paires
- **Jours** : Mardi et Jeudi
- **Périodes** : Après-midi uniquement
- **Compétences** : Contrôle qualité (Intermédiaire)

## 🚀 Avantages de la Configuration Exhaustive

1. **Flexibilité maximale** : Couvre tous les scénarios possibles
2. **Gestion fine** : Contrôle précis de chaque aspect
3. **Automatisation** : Réduction des interventions manuelles
4. **Conformité** : Respect automatique des règles légales
5. **Optimisation** : Meilleure utilisation des ressources
6. **Traçabilité** : Suivi complet des configurations
7. **Évolutivité** : Adaptation aux besoins futurs
8. **Intégration** : Cohérence avec le système global

## 📞 Support et Maintenance

Pour toute question sur la configuration exhaustive des fréquences :
- Consultez ce guide
- Contactez l'équipe technique
- Utilisez la fonction d'aide intégrée
- Consultez les logs de validation

---

*Configuration exhaustive des fréquences - micPlan v2.0*
