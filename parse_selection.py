import json
from pathlib import Path
from slugify import slugify
import yaml


def create_speaker_md(speaker, output_dir):
    speaker_slug = slugify(speaker["name"])
    output_path = output_dir / f"{speaker_slug}.md"

    frontmatter = {
        "name": speaker["name"],
        "short_bio": speaker["bio"],
        "avatar": speaker.get("picture", ""),
        "linkedin": next(
            (link for link in speaker.get("socialLinks", []) if "linkedin.com" in link),
            "",
        ),
        "website": next(
            (
                link
                for link in speaker.get("socialLinks", [])
                if not "linkedin.com" in link and not "x.com" in link
            ),
            "",
        ),
        "published": True,
    }

    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

{speaker["bio"]}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return speaker_slug


def create_talk_md(talk, speaker_slugs, output_dir):
    talk_slug = slugify(talk["title"])
    output_path = output_dir / f"{talk_slug}.md"

    # Map format to kind
    format_to_kind = {
        "⚡️ Quickie (25 minutes)": "conference_courte",
        "📣 Conférence (50 minutes)": "conference_longue",
    }

    kind = format_to_kind[talk["formats"][0]["name"]]

    frontmatter = {
        "title": talk["title"],
        "kind": kind,
        "speakers": speaker_slugs,
        "short_description": talk["abstract"],
        "start_time": "09:00",  # Default time, should be adjusted based on schedule
        "track": talk["categories"][0]["name"],  # Using first category as track
        "categories": [cat["name"] for cat in talk["categories"]],
        "published": True,
    }

    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

{talk["abstract"]}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    root_dir = Path(__file__).parent
    data_dir = root_dir / "data"

    speakers_dir = data_dir / "speakers2"
    talks_dir = data_dir / "talks2"

    Path(speakers_dir).mkdir(parents=True, exist_ok=True)
    Path(talks_dir).mkdir(parents=True, exist_ok=True)

    with open(root_dir / "selection.json", "r", encoding="utf-8") as f:
        selections = json.load(f)

    for talk in selections:
        # First create speaker files and get their slugs
        speaker_slugs = []
        for speaker in talk["speakers"]:
            speaker_slug = create_speaker_md(speaker, speakers_dir)
            speaker_slugs.append(speaker_slug)

        # Then create talk file with reference to speakers
        create_talk_md(talk, speaker_slugs, talks_dir)


if __name__ == "__main__":
    main()
