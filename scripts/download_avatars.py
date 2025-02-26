import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

import requests
import frontmatter
from urllib.parse import urlparse
from models import ROOT_PATH, Speaker


def download_image(url: str, output_path: Path) -> bool:
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def get_image_extension(url: str) -> str:
    path = urlparse(url).path
    return os.path.splitext(path)[1] or ".jpg"


def process_speakers():
    assets_dir = ROOT_PATH / "static" / "images" / "speakers"
    speakers_dir = ROOT_PATH / "data" / "speakers"

    for speaker_file in speakers_dir.glob("*.md"):
        post = frontmatter.load(speaker_file)
        if not post.metadata.get("avatar"):
            continue

        speaker = Speaker.model_validate(post.metadata)

        # Download image
        ext = get_image_extension(speaker.avatar)
        image_filename = f"{speaker.slug}{ext}"
        image_path = assets_dir / image_filename
        relative_path = f"/static/images/speakers/{image_filename}"

        if download_image(speaker.avatar, image_path):
            print(f"Downloaded avatar for {speaker.name} to {image_path}")

            # Update markdown file
            post.metadata["avatar"] = relative_path
            with open(speaker_file, "w") as f:
                f.write(frontmatter.dumps(post))
            print(f"Updated avatar path in {speaker_file}")


if __name__ == "__main__":
    process_speakers()
