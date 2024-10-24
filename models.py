from datetime import date, time, timedelta, datetime
from pathlib import Path
import frontmatter
from pydantic import BaseModel, ValidationError
from typing import ClassVar


class Speaker(BaseModel):
    PATH: ClassVar[str] = "speakers"

    name: str
    short_bio: str
    avatar: str  # TODO : check the file exists
    linkedin: str = ""
    website: str = ""


class Sponsors(BaseModel):
    PATH: ClassVar[str] = "sponsors"

    name: str
    level: str  # TODO : check levels
    short_description: str
    logo: str  # TODO : check the file exists


class Talks(BaseModel):
    PATH: ClassVar[str] = "talks"

    title: str
    speakers: list[str]  # TODO : check the speaker exists
    short_description: str
    duration: int
    start_time: datetime
    end_time: datetime
    categories: list[str]
    download_link: str = ""


class News(BaseModel):
    PATH: ClassVar[str] = "news"

    publication_date: datetime
    title: str


def load_data(root_path: Path, kind: type[BaseModel]) -> list[dict]:
    data = []

    print(f"Loading {kind.PATH}")
    for f in (Path(root_path) / "data" / kind.PATH).glob("*.md"):
        parsed = frontmatter.load(f)
        validated = kind.model_validate(parsed.metadata)
        data.append(
            {"metadata": validated.model_dump_json(), "content": parsed.content}
        )
    return data
