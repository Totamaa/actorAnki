# Actor Anki Deck
![Version](https://img.shields.io/badge/Version-v1.0.0-blueviolet)
![Langage](https://img.shields.io/badge/Langage-Python-0052cf)

## Sommaire 

* **[Sommaire](#Sommaire)**
* **[Installation](#Installation)**
* **[Fonctionnalités](#fonctionnalités)**
* **[Crédits](#crédits)**
  

## Présentation du projet

J'avais pour objectif d'apprendre à reconnaitre les acteurs les plus connues car j'ai du mal a retenir leur nom. 
Pour apprendre quelque chose, j'aime bien utilisé Anki qui est une app opensource de flashcard.
Pour les données je n'ai pas trouvées de deck déjà fait dans Anki ou de données a dispositions (en sachant qu'il me fallait nom + photos).
J'ai donc décidé de faire ce POC qui récupère les données des acteurs et me fait directement mon deck Anki. 

## Installation et utilisation

1. Télécharger ou cloner le repos
2. Télécharger Python
3. Lancer la commande `pip install -r requirements.txt`
4. Lancer le scrypt pour scrapper les données `py gscrap.py`
5. Lancer le scrypt pour créer le deck Anki `py generateAnkiFile.py`
6. Vous pouvez ensuite importer le fichier généré **actors_and_movies.apkg** dans Anki et commencer à apprendre


## Fonctionnalités

* récupérer des données d'un site (scrapping)
  * Nom de l'acteur
  * Photo de l'acteur
  * Films les plus connues de l'acteur
* faire un deck Anki
  * Créer un format de deck
  * Transformer les images en base64
  * Créer toutes les cartes
  * Exporter le fichier

## Crédits

- Dev: **[Matteo Calderaro](https://github.com/Totamaa)**
- Anki:
  - **[site web](https://apps.ankiweb.net/)**
  - **[repo github](https://github.com/ankitects/anki)**
- **[SensCritique](https://www.senscritique.com)** (site pour le scrapping)
  - **[meilleurs acteurs](https://www.senscritique.com/liste/les_meilleurs_acteurs/924862)**
  - **[meilleurs acteurs français](https://www.senscritique.com/liste/les_meilleurs_acteurs_francais_et_du_cinema_francais/1422440)**
  - **[meilleurs actrices](https://www.senscritique.com/liste/actrices_les_plus_connu_du_cinema/855517)**