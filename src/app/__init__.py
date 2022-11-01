import datetime
import random
from tqdm import tqdm
from src.app.middleware import Middleware
from src.utils.database import Database
from src.utils.email import Email

def app(settings: dict) -> None:
    middleware = Middleware(settings=settings["app"])
    database = Database(settings=settings["database"])
    email = Email(settings=settings["smtp"])

    # Get a random episode

    episode = middleware.get("episode", random.randint(1, 50))
    print("The episode is " + episode["name"] + " with id " + episode["episode"])

    # Verify that the episode does not exist

    verify = database.get(query=3, payload=[episode["id"]])

    if len(verify) != 0:
        raise NameError("The episode was already saved")

    # Save the episode

    database.execute(query=7, payload=[episode["id"], episode["name"], episode["episode"]])

    # Get the characters by episode

    print("\nGet characters")
    characters = []
    urls = episode["characters"]
    progress = tqdm(total=len(urls))

    for url in urls:
        character = middleware.get(url=url)
        characters.append(character)
        progress.update()
    
    progress.close()

    # Get character details

    print("\nGet character details")
    locations = []
    progress = tqdm(total=len(characters))

    for character in characters:
        character["origin"] = character["origin"]["name"]

        if not character["location"]["url"]:
            character["location"] = 0
        else:
            location = middleware.get(url=character["location"]["url"])
            character["location"] = location["id"]
            locations.append(location)

        progress.update()

    progress.close()

    # Verify that the character does not exist

    print("\nVerify the characters")
    progress = tqdm(total=len(characters))
    news = []
    saved = 0

    for character in characters:
        verify = database.get(query=4, payload=[character["id"]])

        if len(verify) == 0:

            # Save the character

            database.execute(query=8, payload=[character["id"], character["name"], character["status"], character["species"], character["gender"], character["origin"], character["location"], character["image"]])
            
            # Save the characters to send email
            
            news.append(character)
            saved = saved + 1

        progress.update()
    
    progress.close()
    print(f"\nTotal number of saved characters {saved}")

    # Get the locations

    print("\nVerify the locations")
    progress = tqdm(total=len(locations))
    saved = 0

    for location in locations:
        verify = database.get(query=5, payload=[location["id"]])

        if len(verify) == 0:

            # Save the location

            database.execute(query=9, payload=[location["id"], location["name"], location["type"], location["dimension"]])
            saved = saved + 1

        progress.update()

    progress.close()
    print(f"\nTotal number of saved locations {saved}")

    # Send the emails

    payload = {
        "template": {
            "name": "default",
            "payload": {
                "id": episode["episode"],
                "name": episode["name"],
                "total": len(characters),
                "created": str(datetime.datetime.now())
            }
        },
        "components": [{
            "name": "tr",
            "payload": news
        }]
    }
    
    email.send(subject="New characters", payload=payload)

    # End
