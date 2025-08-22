# 🎯 Démonstration : Gestion des disponibilités des utilisateurs

## ✨ Nouvelle fonctionnalité ajoutée

La gestion des utilisateurs inclut maintenant une fonctionnalité complète pour configurer les **disponibilités et préférences** de chaque utilisateur (excepté les administrateurs).

## 🚀 Comment utiliser

### 1. Accès à la fonctionnalité
- Connectez-vous en tant qu'**administrateur**
- Allez dans **"⚙️ Configuration"** → **"Gestion des utilisateurs"**
- Sélectionnez un utilisateur dans la liste (superviseur ou utilisateur)
- Cliquez sur le bouton **"⚙️ Disponibilités"**

### 2. Configuration des disponibilités

#### 📅 Jours et horaires de travail
- **Jours de travail** : Sélectionnez les jours où l'utilisateur est disponible
- **Heure de début/fin** : Définissez les horaires de travail
- **Pause déjeuner** : Spécifiez la plage horaire de pause

#### ⏰ Contraintes de temps
- **Heures max/jour** : Limite quotidienne (1-12h)
- **Heures max/semaine** : Limite hebdomadaire (1-60h)
- **Shifts préférés** : Matin, Après-midi, Nuit, Flexible

#### 📝 Notes et contraintes
- **Zone de texte libre** pour des informations importantes
- Exemples : "Préfère ne pas travailler le vendredi après-midi", "Contraintes familiales"

### 3. Sauvegarde automatique
- Toutes les modifications sont **automatiquement sauvegardées**
- Les données sont stockées dans `data/users_database.json`
- Redirection automatique vers la liste des utilisateurs

## 🔒 Sécurité et permissions

- **Seuls les administrateurs** peuvent configurer les disponibilités
- **Les administrateurs** n'ont pas de disponibilités configurables
- **Superviseurs et utilisateurs** peuvent avoir des disponibilités personnalisées

## 💾 Structure des données

```json
{
  "username": "utilisateur_exemple",
  "availability": {
    "work_days": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
    "work_hours": {
      "start": "08:00",
      "end": "17:00"
    },
    "break_time": "12:00-13:00",
    "max_hours_per_day": 8,
    "max_hours_per_week": 40,
    "preferred_shifts": ["Matin"],
    "unavailable_dates": [],
    "notes": "Notes personnalisées..."
  }
}
```

## 🎨 Interface utilisateur

- **Design cohérent** avec le reste de l'application
- **Formulaires intuitifs** avec validation des données
- **Messages d'erreur clairs** et informatifs
- **Navigation fluide** entre les pages

## 🔄 Intégration

- **Compatible** avec la gestion existante des utilisateurs
- **Initialisation automatique** des disponibilités par défaut
- **Migration transparente** pour les utilisateurs existants
- **Sauvegarde persistante** dans la base de données

## 📱 Utilisation pratique

1. **Planification d'équipe** : Utilisez les disponibilités pour optimiser les plannings
2. **Gestion des ressources** : Respectez les contraintes de chaque utilisateur
3. **Flexibilité** : Adaptez les horaires selon les besoins du service
4. **Traçabilité** : Gardez une trace des préférences de chaque membre

## 🚧 Limitations actuelles

- Les disponibilités ne sont pas encore utilisées dans l'algorithme de planification
- Pas de gestion des congés ou absences exceptionnelles
- Pas de validation croisée entre utilisateurs

## 🔮 Évolutions futures

- **Intégration avec le planning** : Utilisation automatique des disponibilités
- **Gestion des congés** : Dates d'indisponibilité
- **Validation croisée** : Vérification des conflits
- **Notifications** : Alertes en cas de dépassement des limites
