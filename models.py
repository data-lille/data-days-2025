from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any, ClassVar

import frontmatter  # type: ignore
from pydantic import BaseModel, field_validator, model_validator
from slugify import slugify

ROOT_PATH = Path(__file__).parent


class ListRetrieveMixin:
    slug: str

    @classmethod
    def get_all(cls):
        return load_data(ROOT_PATH, cls)

    @classmethod
    def get_item(cls, slug):
        for item in cls.get_all():
            if item["metadata"]["slug"] == slug:
                return item

    @model_validator(mode="before")
    @classmethod
    def add_slug(cls, data: Any) -> Any:
        if "title" in data:
            data["slug"] = slugify(data["title"])
        if "name" in data:
            data["slug"] = slugify(data["name"])

        return data


class Speaker(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "speakers"

    name: str
    short_bio: str
    avatar: str  # TODO : check the file exists
    linkedin: str = ""
    website: str = ""
    talks: list["Talks"] = []


class Sponsors(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "sponsors"

    name: str
    slug: str
    level: str  # TODO : check levels
    short_description: str
    logo: str  # TODO : check the file exists


talks_infos = {
    "gouter": {"duration_minutes": 15, "label": "Goûter"},
    "pleniere_courte": {"duration_minutes": 20, "label": "Plénière courte"},
    "pleniere_longue": {"duration_minutes": 30, "label": "Plénière longue"},
    "conference_courte": {"duration_minutes": 30, "label": "Conférence courte"},
    "conference_longue": {"duration_minutes": 60, "label": "Conférence longue"},
    "repas": {"duration_minutes": 90, "label": "Repas"},
}


class Talks(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "talks"

    title: str
    kind: str
    # kind_humanized: str
    speakers: list[str]  # TODO : check the speaker exists
    short_description: str
    start_time: time
    end_time: time
    duration: int
    track: str
    categories: list[str]
    download_links: list[str] = [""]
    is_extra: bool = False  # should be in all tracks (ie: gouter, petit dejeuner)
    picture: str = ""  # the picture to display in the program

    @field_validator("kind")
    @classmethod
    def validate_kind(cls, kind):
        if kind not in talks_infos:
            raise ValueError(f"must be in {talks_infos.keys()}")
        humanized = talks_infos[kind]["label"]
        return kind

    @model_validator(mode="before")
    @classmethod
    def add_end_time_and_duration(cls, data: Any) -> Any:
        start_time = datetime.strptime(data["start_time"], "%H:%M")
        duration: int = talks_infos[data["kind"]]["duration_minutes"]  # type: ignore
        data["end_time"] = (start_time + timedelta(minutes=duration)).time()
        data["duration"] = duration
        return data


class News(BaseModel, ListRetrieveMixin):
    PATH: ClassVar[str] = "news"

    publication_date: datetime
    name: str
    published: bool


def load_data(root_path: Path, kind: type[BaseModel]) -> list[dict]:
    data = []

    print(f"Loading {kind.PATH}")  # type: ignore
    for f in (Path(root_path) / "data" / kind.PATH).glob("*.md"):  # type: ignore
        parsed = frontmatter.load(f)
        validated = kind.model_validate(parsed.metadata)
        data.append({"metadata": validated.model_dump(), "content": parsed.content})
    return data


def generate_time_interval_between(start: datetime, stop: datetime, interval: int):
    hours = []
    current = start
    while current <= stop:
        hours.append(current.time())
        current += timedelta(minutes=interval)
    print(hours)
    return hours


class Schedule:
    def __init__(self):
        self.talks = Talks.get_all()
        self.tracks = list(sorted(set(t["metadata"]["track"] for t in self.talks)))

        start_day = datetime(2000, 1, 1, hour=9, minute=00)
        end_day = datetime(2000, 1, 1, hour=18, minute=0)
        self.start_times = generate_time_interval_between(
            start_day, end_day, interval=5
        )

    def get_for_track_and_time(self, track, start_time):
        for talk in self.talks:
            correct_track = talk["metadata"]["track"] == track
            talks_start_time = talk["metadata"]["start_time"]
            talks_start_time = talks_start_time.replace(tzinfo=None)
            correct_start_time = talks_start_time == start_time

            if talk["metadata"]["kind"] == "Extra" and correct_start_time:
                if track == self.tracks[0]:
                    return talk

            print(talk["metadata"]["start_time"], start_time)
            if correct_track and correct_start_time:
                return talk
        # not found
        return None
