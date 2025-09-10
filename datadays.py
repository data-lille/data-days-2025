from pathlib import Path
from flask import Flask, render_template
from flask_frozen import Freezer
from markdown2 import Markdown
from sassutils.wsgi import SassMiddleware
from slugify import slugify
from models import Speaker, Sponsors, Talks, News, Schedule
from babel.dates import format_date, format_time as babel_format_time
from datetime import datetime, time
import os

app = Flask(__name__, static_url_path="/2026/static")
app.wsgi_app = SassMiddleware(
    app.wsgi_app,
    {
        "datadays": {
            "sass_path": "static/sass",
            "css_path": "static/css",
            "wsgi_path": "/2026/static/css",
            "strip_extension": True,
        }
    },
)


try:
    _GIT_MAIN = Path(app.root_path) / ".git" / "refs" / "heads" / "main"
    GIT_VERSION = _GIT_MAIN.read_text().strip()[:7]
except FileNotFoundError:
    GIT_VERSION = os.environ.get("COMMIT_REF", "")[:7]


@app.template_filter()
def slug(string):
    return slugify(string, max_length=30)


@app.template_filter()
def markdown(string):
    # todo : https://stackoverflow.com/questions/35989935/decrease-html-headings-using-python-elementtree
    return Markdown().convert(string)


@app.template_filter()
def version(url):
    return f"{url}?{GIT_VERSION}"


@app.template_filter()
def format_datetime(dt: datetime):
    return format_date(dt, locale="fr_FR")


@app.template_filter()
def format_time(dt: time):
    return babel_format_time(dt, format="short", locale="fr_FR")


# TODO
#   * validation des models
#   * créer le programme
#   * afficher listing talks / une présentation d'un talk
#   * faire marcher le ICS


# @app.route("/2026/<lang>/speakers/")
# def speakers_listing(lang="fr"):
#     return render_template(
#         f"{lang}/speakers.jinja2.html",
#         page_name="speakers_listing",
#         speakers=Speaker.get_all(),
#         lang=lang,
#     )


# @app.route("/2026/<lang>/speakers/<slug>/")
# def speakers_details(slug, lang="fr"):
#     speaker = Speaker.get_item(slug)
#     talks = []

#     for talk in Talks.get_all():
#         if speaker["metadata"]["slug"] in talk["metadata"]["speakers"]:
#             talks.append(talk)

#     return render_template(
#         f"{lang}/speakers-details.jinja2.html",
#         page_name="speakers_listing",
#         item=speaker,
#         talks=talks,
#         lang=lang,
#     )


@app.route("/2026/<lang>/sponsors/")
def sponsors_listing(lang="fr"):
    return render_template(
        f"{lang}/sponsors.jinja2.html",
        page_name="sponsors_listing",
        sponsors=Sponsors.get_all(),
        lang=lang,
    )


# @app.route("/2026/<lang>/sponsors/<slug>/")
# def sponsors_details(slug, lang="fr"):
#     return render_template(
#         f"{lang}/sponsors-details.jinja2.html",
#         page_name="sponsors_details",
#         item=Sponsors.get_item(slug),
#         lang=lang,
#     )


# @app.route("/2026/<lang>/presentations/")
# def talks_listing(lang="fr"):
#     return render_template(
#         f"{lang}/talks.jinja2.html",
#         page_name="talks",
#         speakers=Talks.get_all(),
#         lang=lang,
#     )


# @app.route("/2026/<lang>/presentations/<slug>/")
# def talks_details(slug, lang="fr"):
#     talk = Talks.get_item(slug)
#     speakers = [Speaker.get_item(slug) for slug in talk["metadata"]["speakers"]]
#     return render_template(
#         f"{lang}/talks-details.jinja2.html",
#         page_name="speakers",
#         item=talk,
#         speakers=speakers,
#         lang=lang,
#     )


# @app.route("/2026/<lang>/actualites/")
# def news_listing(lang="fr"):
#     return render_template(
#         f"{lang}/news.jinja2.html",
#         page_name="news_listing",
#         news=News.get_all(),
#         lang=lang,
#     )


# @app.route("/2026/calendar.ics")
# def calendar(lang="fr"):
#     return "Bientôt"
#     # ics = render_template("calendar.jinja2.ics", lang=lang)
#     # return Response(ics, mimetype="text/calendar")


# @app.route("/2026/<lang>/programme/")
# def schedule(lang="fr"):
#     schedule = Schedule()
#     # Créer un dictionnaire des speakers indexé par leur slug
#     speakers = {s["metadata"]["slug"]: s for s in Speaker.get_all()}
#     return render_template(
#         f"{lang}/schedule.jinja2.html",
#         page_name="schedule",
#         lang=lang,
#         schedule=schedule,
#         speakers=speakers,
#     )


# @app.route("/2026/<lang>/programme-complet/")
# def full_schedule(lang="fr"):
#     schedule = Schedule()

#     day = "Vendredi 28 mars 2026"
#     schedule = {
#         "rooms": schedule.tracks,
#         "schedule": schedule,
#         "day": day,
#     }
#     return render_template(
#         f"{lang}/full-schedule.jinja2.html",
#         page_name="full-schedule",
#         lang=lang,
#         schedule=schedule,
#     )


# @app.route("/2026/<lang>/venue/")
# def venue(lang="fr"):
#     return render_template(f"{lang}/venue.jinja2.html", page_name="venue", lang=lang)


# @app.route("/2026/<lang>/support/")
# def support(lang="fr"):
#     return render_template(
#         f"{lang}/support.jinja2.html", page_name="support", lang=lang
#     )


# @app.route("/2026/<lang>/conduct/")
# def conduct(lang="fr"):
#     return render_template(
#         f"{lang}/conduct.jinja2.html", page_name="conduct", lang=lang
#     )


@app.route("/")
@app.route("/2026/")
def index(lang="fr"):
    return render_template(
        f"{lang}/index.jinja2.html",
        page_name="index",
        lang=lang,
        sponsors=Sponsors.get_all(),
    )


@app.cli.command("freeze")
def freeze():
    Freezer(app).freeze()
