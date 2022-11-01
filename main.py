import json
import sys
from src.utils.database import Database
from src import start

def main():
    # Verify that the files used by the program exist

    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)

        manifest = open("docs/manifest.txt", "r").read()
    except:
        raise NameError("Error reading setting files")

    # All ready

    start(settings=settings, manifest=manifest)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
        sys.exit()
