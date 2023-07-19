import requests
from bs4 import BeautifulSoup
import json
import os
import time
import tqdm

links_info = [
    {
        "url": "/liste/les_meilleurs_acteurs/924862?page={}",
        "pages": 13
    },
    {
        "url": "/liste/les_meilleurs_acteurs_francais_et_du_cinema_francais/1422440?page={}",
        "pages": 5
    },
    {
        "url": "/liste/actrices_les_plus_connu_du_cinema/855517?page={}",
        "pages": 1
    }
]

# Fonction pour récupérer les informations des acteurs depuis une page donnée
def scrap_actors(page_url):
    # Faire une requête HTTP pour récupérer le contenu de la page
    response = requests.get(page_url)
    # Utiliser BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(response.content, "html.parser")

    actors_data = [] # Liste pour stocker les données des acteurs

    # Trouver toutes les divs contenant les informations des acteurs
    actors = soup.find_all("div", class_="ContactListItem__Wrapper-sc-bv232x-1")

    # Parcourir chaque div d'acteur pour extraire les informations
    for actor in actors:
        # Récupérer le nom de l'acteur
        # Récupérer l'URL de l'image de l'acteur
        photo = actor.find("div", class_="ContactPoster__PosterWrapper-sc-1ob7mpa-0")["data-srcname"]
        # Récupérer la liste des films de l'acteur
        movies_elt = actor.find("span", class_="Text__SCUserText-sc-1aoldkr-2")
        
        if movies_elt:
            name = " ".join(actor.find("h3", class_="Text__SCText-sc-1aoldkr-0").text.strip().split(" ")[1:])
            movies = movies_elt.text.strip().split(" / ")
        else:
            name = actor.find("h3", class_="Text__SCText-sc-1aoldkr-0").text.strip()
            movies = []

        # Créer un dictionnaire contenant les informations de l'acteur et l'ajouter à la liste
        actor_data = {
            "nom": name,
            "photo": photo,
            "films": movies
        }
        actors_data.append(actor_data)

    return actors_data

# Fonction pour télécharger une image depuis une URL
def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        # Créer le dossier "img" s'il n'existe pas déjà
        os.makedirs("img", exist_ok=True)
        # Sauvegarder l'image dans le dossier "img"
        with open(os.path.join("img", file_name), "wb") as file:
            file.write(response.content)
        return True
    else:
        return False

if __name__ == "__main__":
    base_url = "https://www.senscritique.com"
    actors_data = [] # Liste pour stocker les données de tous les acteurs
    final_actors_data = [] # Liste pour stocker les données de tous les acteurs après traitement
    
    # Parcourir les informations des liens pour récupérer les données des acteurs    
    for link_info in tqdm.tqdm(links_info, desc="Récupération des données des acteurs", ncols=100):
        page_url_template = link_info["url"]
        nb_pages = link_info["pages"]

        # Parcourir toutes les pages pour récupérer les informations des acteurs
        for page_num in range(1, nb_pages + 1):
            page_url = base_url + page_url_template.format(page_num)
            actors_data.extend(scrap_actors(page_url)) # Ajouter les données des acteurs à la liste
            
    # Vérifier et mettre à jour les données des acteurs
    for actor in tqdm.tqdm(actors_data, desc="Mise à jour des données des acteurs", ncols=100):
        actor_name = actor["nom"]
        image_url = actor["photo"]
        movies = actor["films"]

        image_name = f"{actor_name.replace(' ', '_')}.jpg"
        image_path = os.path.join("img", image_name)


        # Vérifier si l'acteur existe déjà dans la liste
        existing_actor = next((a for a in final_actors_data if a["nom"] == actor_name), None)
        if existing_actor:
            # Si l'acteur existe déjà, mettre à jour la liste de films s'il y en a de nouveaux
            existing_movies = existing_actor["films"]
            new_movies = [movie for movie in movies if movie not in existing_movies]
            existing_movies.extend(new_movies)
        else:
            # Si l'acteur est nouveau, l'ajouter à la liste
            final_actors_data.append({
                "nom": actor_name,
                "films": movies,
                "photo": f"{image_name}",
            })
            # Télécharger l'image de l'acteur seulement s'il est nouveau
            download_image(image_url, image_name)
            # time.sleep(0.5)  # Ajouter une pause de 0.5 seconde avant chaque téléchargement d'image

    # Sauvegarder les données mises à jour dans le fichier JSON
    with open("actors_data.json", "w", encoding="utf-8") as file:
        json.dump(final_actors_data, file, ensure_ascii=False, indent=4)

