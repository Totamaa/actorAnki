import os
import genanki
import json
import base64

# Function to download the image and convert it to a base64 string
def image_to_base64(url):
    img_path = os.path.join("img", url)
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            return base64_image
    else:
        return ""

# Load data from the JSON file
with open("actors_data.json", "r", encoding="utf-8") as file:
    actors_data = json.load(file)

# Create a new Anki deck model
anki_model = genanki.Model(
    model_id=1,
    name="Actors and Movies",
    fields=[{"name": "Actor"}, {"name": "Movies"}, {"name": "Image"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '<div style="text-align: center;"><img src="data:image/png;base64,{{Image}}"></div>',
            "afmt": '<div style="text-align: center;">{{FrontSide}}<hr id="answer">{{Actor}}<br>{{Movies}}</div>'
        },
    ],
    css='''\
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
}

img {
    max-width: 100%;
    height: auto;
}
'''
)

# Create an Anki deck with the model
anki_deck = genanki.Deck(
    deck_id=1234567890,
    name="Actors and Movies"
)

# Add flashcards for each actor and their movies
for actor_data in actors_data:
    actor_name = actor_data["nom"]
    movies = ", ".join(actor_data["films"][:10])
    actor_image = actor_data["photo"]
    base64_image = image_to_base64(actor_image)
    anki_note = genanki.Note(
        model=anki_model,
        fields=[actor_name, movies, base64_image]
    )
    anki_deck.add_note(anki_note)

# Create an Anki package and save it to a file
anki_package = genanki.Package(anki_deck)
anki_package.write_to_file("actors_and_movies.apkg")
