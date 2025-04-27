import sys
from pathlib import Path
from slugify import slugify

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from models import ROOT_PATH


def slugify_slides():
    slides_dir = ROOT_PATH / "static" / "slides"
    if not slides_dir.exists():
        print(f"Dossier {slides_dir} n'existe pas")
        return

    for slide_file in slides_dir.glob("*.*"):
        # Garder l'extension
        extension = slide_file.suffix
        # Slugifier le nom sans l'extension
        new_name = slugify(slide_file.stem) + extension
        new_path = slide_file.parent / new_name

        # Renommer le fichier
        try:
            slide_file.rename(new_path)
            print(f"Renommé: {slide_file.name} -> {new_name}")
        except Exception as e:
            print(f"Erreur lors du renommage de {slide_file}: {e}")


if __name__ == "__main__":
    slugify_slides()
