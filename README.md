# LOG210-server

### Description
Partie serveur pour le projet de laboratoire du cours LOG210 ETS

### Installation

###### Pré requis
1. Installer Python 2.7 (https://www.python.org/downloads/)
2. Installer la commande pip (>easy_install pip -- http://pip.readthedocs.org/en/latest/installing.html)
3. Installer virtualenv (>pip install virtualenv -- http://virtualenv.readthedocs.org/en/latest/)
4. Créer les environnements virtuels pour le serveur et pour le client (>virtualenv nom_dossier)
5. Activer l’environnement (>source bin/activate – depuis le dossier de l’environnement)
6. Installer les librairies (>pip install -r requirements.txt et aussi > pip install mysql-connector-python-1.2.3 (depuis le dossier LOG210-server)

###### Installation base de données
1. Installer Mamp (http://www.mamp.info/en/)
2. Lancer Mamp, sur la page d'accueil (http://localhost:8888/MAMP/) > Tools > phpMyAdmin
3. Créér une nouvelle base de donnée (nom: "restaurants", encodage: "utf8_general_ci")

###### Général
1. Se placer dans le dossier "LOG210-server"
2. Ouvrir un terminal: >python manager.py install (A faire dès que le modèle évolue pour ajouter les nouvelles tables, au préalable supprimer toutes la base de donnée afin d'être sur qu'il ne reste pas d'anciens éléments en cas de modification)
3. Vérifier dans la base de données que la première table a bien été créée

### Executer le serveur

Se placer dans le dossier "LOG210-server" et >python manager.py runserver

### Structure de l'application

* manager.py: permet de lancer le serveur et installer la base de donnée
* webserver
	* config.py: contient la configuration pour se connecter à la base de donnée
	* models: contient les modèles
	* controllers: contient les web services


### Tests
https://nose.readthedocs.org/en/latest/

* Installer les requirements (>pip install -r requirements-test.txt)
* Depuis l'environnement virtuel lancer la commande >nosetests
	* (-v: visualiser le noms des tests)
	* (-x: stopper la série de tests lorsqu'un test échoue)
	* (-s -d: visualiser les print pour débugger)


### Traduction
https://pythonhosted.org/Flask-Babel/
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n

1. Installer Flask-Babel
pip install -r requirements.txt

2. Marquer les chaines à traduire avec gettext("chaine")
3. Extraire les chaines en fichier pot
pybabel extract -F babel.cfg -o translations/en/LC_MESSAGES/messages.pot controllers
	* Commande à lancer depuis le dossier webserver (lieu où se trouve le dossier translations)
	* babel.cfg est un fichier de configuration qui permet d'indiquer où chercher les chaines à traduire
	* Le paramètres "controllers" indique le dossiers où chercher les chaines à traduire

4. Réaliser la traduction avec poedit
5. Compiler
pybabel compile -d translations
	* Commande à lancer depuis le dossier webserver (lieu où se trouve le dossier translations)
