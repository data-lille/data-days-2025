from datetime import date, time, timedelta, datetime
from pathlib import Path
import frontmatter
from pydantic import BaseModel, ValidationError
from typing import ClassVar

ROOT_PATH = Path(__file__).parent


class ListRetrieveMixin:
    @classmethod
    def get_all(cls):
        return load_data(ROOT_PATH, cls)

    @classmethod
    def get_item(cls, slug):
        for item in cls.get_all():
            if item["slug"] == slug:
                return item


class Speaker(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "speakers"

    name: str
    slug: str
    short_bio: str
    avatar: str  # TODO : check the file exists
    linkedin: str = ""
    website: str = ""


class Sponsors(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "sponsors"

    name: str
    slug: str
    level: str  # TODO : check levels
    short_description: str
    logo: str  # TODO : check the file exists


class Talks(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "talks"

    title: str
    slug: str
    speakers: list[str]  # TODO : check the speaker exists
    short_description: str
    duration: int
    start_time: datetime
    end_time: datetime
    categories: list[str]
    download_link: str = ""

    def get_all(self):
        return load_data(ROOT_PATH, type(self))


class News(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "news"

    publication_date: datetime
    slug: str
    name: str
    published: bool


def load_data(root_path: Path, kind: type[BaseModel]) -> list[dict]:
    data = []

    print(f"Loading {kind.PATH}")
    for f in (Path(root_path) / "data" / kind.PATH).glob("*.md"):
        parsed = frontmatter.load(f)
        validated = kind.model_validate(parsed.metadata)
        data.append({"metadata": validated.model_dump(), "content": parsed.content})
    return data
