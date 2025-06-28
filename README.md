# django-pystock

Ce projet portfolio est réalisé dans le cadre de la formation Docstring.fr.


Le projet utilise `uv` en tant que gestionnaire de paquets.
[Installez-le](https://docs.astral.sh/uv/getting-started/installation/) selon votre système d'exploitation.


## Objectif de l'application

L'application PyStock permet de gérer les stocks de plusieurs entreprises sur leurs différents sites.

Deux types d'utilisateur peuvent accéder à l'interface :
- le gestionnaire (administrateur)
- l'employé (utilisateur)

Les employés peuvent gérer le catalogue de produits, organiser les stocks par site et entreprise, 
mettre à jour et tracer les mouvements de stocks, et recevoir une alerte lorsque certains stocks 
passent en-dessous d'un seuil donné.

En plus de ces fonctionnalités de base, un gestionnaire peut accéder à l'interface d'administration pour 
créer/modifier les entreprises et leurs sites, ainsi que les utilisateurs et leurs permissions.

Le gestionnaire a également accès à une vue analytique des stocks dans l'interface principale.
Enfin, il doit être en mesure d'exporter et importer des données si nécessaire.


## Installation de l'application

1. Cloner le projet sur votre ordinateur
    - `git clone https://github.com/aurechabnv/django-pystock.git`
    - `cd django-pystock`


2. Installer la version de Python requise et les dépendances
    - `uv install python`
    - `uv sync`


3. Activer l'environnement virtuel selon votre système d'exploitation
    - `source .venv/bin/activate # MacOS/Linux`
    - ou
    - `source .venv\Scripts\activate # Windows`


4. Initialiser la base de données
    - `python manage.py makemigrations`
    - `python manage.py migrate`
    - `python manage.py loaddata fixtures/initial_data.json`


5. Créer d'un administrateur (super-utilisateur)
    - `python manage.py createsuperuser`


5. Lancer le serveur
    - `python manage.py runserver`


6. Accéder au site local
   - Application : http://127.0.0.1:8000/
   - Interface admin : http://127.0.0.1:8000/backend/
