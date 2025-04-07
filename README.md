# Projet_10 SoftDesk Support

SoftDesk Support est une API RESTful développée avec Django et Django REST Framework. Elle permet aux entreprises B2B de gérer efficacement le suivi des problèmes techniques grâce à un système structuré de projets, de tickets (issues) et de commentaires.

---

## À propos

Développé par **SoftDesk**, éditeur de logiciels de collaboration, ce projet vise à fournir une solution de support technique personnalisée pour les entreprises.

---

## Fonctionnalités principales

- Authentification via JWT
- Gestion des utilisateurs avec consentement RGPD
- Création et gestion de projets
- Attribution de contributeurs aux projets
- Création de tickets (issues) avec priorité, statut et balise
- Commentaires sur les tickets
- Contrôle d'accès par rôle (auteur, contributeur)
---

## Ressources principales

| Ressource   | Description |
|-------------|-------------|
| **User**        | Utilisateurs avec gestion RGPD (âge, consentement, etc.) |
| **Contributor** | Lien entre un utilisateur et un projet, avec droits spécifiques |
| **Project**     | Projets créés par les utilisateurs |
| **Issue**       | Problèmes/tâches à résoudre, liés à un projet |
| **Comment**     | Commentaires sur une issue |

---

## Gestion des utilisateurs

- Authentification avec **JWT**
- Vérification de l’âge (>= 15 ans) pour conformité RGPD
- Deux attributs RGPD :
  - `can_be_contacted`: Oui / Non
  - `can_data_be_shared`: Oui / Non


## Installation

### 1. Cloner le projet

```bash
git https://github.com/annelsopenclassrooms/Projet_10_API.git
cd softdesk
```
### 2. Créer un environnement virtuel et l’activer :
   ```sh
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
### 3. Installer les dépendances :
   ```sh
   pip install -r requirements.txt
   ```
### 4. Appliquer les migrations de la base de données :
   ```sh
   python manage.py migrate
   ```
### 5. Lancer le serveur de développement :
   ```sh
   python manage.py runserver
   ```
## Tests des endpoints

Vous pouvez utiliser :

    * Postman
    * curl
    * l’interface web du Django REST Framework :
    http://127.0.0.1:8000/