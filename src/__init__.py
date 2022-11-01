from src.app import app
from pyfiglet import Figlet

def start(settings: dict, manifest: str) -> None:
    figlet = Figlet(font="standard")
    title = figlet.renderText("Rick And Morty")
    print(title)
    print(manifest)

    # Program starting point
    
    app(settings=settings)

    # Close the program

    print("Successfully completed program")
