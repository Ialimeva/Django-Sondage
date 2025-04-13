# SurveyDay - Application de Sondage

## Description
SurveyDay est une application web Django permettant de créer, gérer et participer à des sondages en ligne. L'application propose différents rôles utilisateurs (Administrateur, Enquêteur, Participant) avec des fonctionnalités spécifiques pour chaque rôle.

## Fonctionnalités Principales

### Administrateur
- Création et gestion des sondages
- Gestion des questions et réponses
- Visualisation des résultats
- Gestion des utilisateurs

### Enquêteur
- Création de sondages
- Ajout et modification de questions
- Consultation des réponses

### Participant
- Participation aux sondages disponibles
- Consultation des sondages
- Soumission des réponses

## Prérequis
- Python 3.8 ou supérieur
- Django 5.0
- Base de données SQLite (par défaut)

## Installation

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd sondage
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur :
```bash
python manage.py runserver
```

## Structure du Projet et Chemins (Paths)

### Structure Générale
```
sondage/
├── home/
│   ├── static/
│   │   └── css/
│   ├── templates/
│   │   ├── admin/
│   │   ├── enqueteur/
│   │   └── participants/
│   ├── models.py
│   └── views.py
└── sondage/
    ├── settings.py
    └── urls.py
```

### Chemins et Leurs Fonctions

#### Templates (home/templates/)
##### Admin (templates/admin/)
- `main_admin.html` : Page principale de l'administrateur
- `view_enquete.html` : Visualisation détaillée d'un sondage
- `enquete_creation.html` : Formulaire de création de sondage
- `question_creation.html` : Formulaire d'ajout de questions
- `addResponse.html` : Ajout de réponses possibles
- `viewEmail.html` : Liste des emails des participants
- `viewResponse.html` : Visualisation des réponses
- `delete.html` : Confirmation de suppression
- `delete_question.html` : Confirmation de suppression de question

##### Enquêteur (templates/enqueteur/)
- `home_enqueteur.html` : Page d'accueil de l'enquêteur
- `enquete_creation_enqueteur.html` : Création de sondage
- `view_enquete.html` : Vue des sondages créés
- `question_creation.html` : Ajout de questions
- `addResponse.html` : Ajout de réponses
- `viewEmail.html` : Consultation des participants
- `viewResponse.html` : Vue des réponses reçues
- `delete.html` et `delete_question.html` : Pages de suppression

##### Participants (templates/participants/)
- `enqueteList.html` : Liste des sondages disponibles
- `survey.html` : Page de participation au sondage
- `thanksPage.html` : Page de remerciement

#### Pages Principales
- `welcome.html` : Page d'accueil principale
- `login.html` : Page de connexion
- `register.html` : Page d'inscription

#### URLs Principales
- `/` : Page d'accueil
- `/login/` : Connexion
- `/register/` : Inscription
- `/home_admin/` : Interface administrateur
- `/home_enqueteur/` : Interface enquêteur
- `/all_enquete/` : Liste des sondages (participants)

#### Modèles (models.py)
- `role` : Gestion des rôles utilisateurs
- `role_and_user_connex` : Association utilisateur-rôle
- `enquete` : Définition des sondages
- `questions` : Questions des sondages
- `reponses` : Réponses possibles
- `responseSelection` : Choix de réponses
- `enqueteResponse` : Réponses des participants

#### Vues (views.py)
Organisées en trois sections :
1. **Admin** : Gestion complète des sondages
2. **Enquêteur** : Création et gestion de sondages
3. **Participants** : Participation aux sondages

## Utilisation

1. Accéder à l'interface d'administration :
   - URL : `http://localhost:8000/admin`
   - Connectez-vous avec les identifiants superutilisateur

2. Accéder à l'application :
   - URL : `http://localhost:8000`
   - Créez un compte ou connectez-vous

## Rôles Utilisateurs

### Administrateur
- Accès complet à toutes les fonctionnalités
- Gestion des utilisateurs et des rôles
- Supervision globale des sondages

### Enquêteur
- Création et gestion de ses propres sondages
- Visualisation des réponses
- Modification des questions

### Participant
- Participation aux sondages
- Consultation des sondages disponibles
