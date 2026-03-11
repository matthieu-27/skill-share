# SkillShare - Application d'échange de compétences

## Prérequis
- Python 3.10 ou supérieur
- Git

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/skill-share.git
   cd skill-share
   ```

2. Créer un environnement virtuel :
   ```bash
   python -m venv .venv
   ```

3. Activer l'environnement virtuel :
   ```bash
   .venv\Scripts\activate
   ```

4. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

5. Configurer la base de données :
   ```bash
   python manage.py migrate
   ```

6. Créer un superutilisateur (admin) :
   ```bash
   python manage.py createsuperuser
   ```

7. Collecter les fichiers statiques :
   ```bash
   python manage.py collectstatic
   ```

## Lancement

1. Démarrer le serveur de développement :
   ```bash
   python manage.py runserver
   ```

2. Accéder à l'application dans votre navigateur :
   ```
   http://127.0.0.1:8000/
   ```

3. Accéder à l'interface d'administration :
   ```
   http://127.0.0.1:8000/admin/
   ```
