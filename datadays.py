from pathlib import Path
from flask import Flask, Response, render_template
from flask_frozen import Freezer
from markdown2 import Markdown
from sassutils.wsgi import SassMiddleware
from slugify import slugify
from models import Speaker, Sponsors, Talks, News
from babel.dates import format_date, format_time, format_timedelta

app = Flask(__name__, static_url_path="/2025/static")
app.wsgi_app = SassMiddleware(
    app.wsgi_app,
    {
        "datadays": {
            "sass_path": "static/sass",
            "css_path": "static/css",
            "wsgi_path": "/2025/static/css",
            "strip_extension": True,
        }
    },
)


_GIT_MAIN = Path(app.root_path) / ".git" / "refs" / "heads" / "main"
GIT_VERSION = _GIT_MAIN.read_text().strip()[:7]


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
def format_datetime(string):
    return format_date(string)


# TODO
#   * validation des models
#   * afficher listing talks / une présentation d'un talk
#   * afficher listing speakers / détails speakers
#   * faire marcher le ICS


@app.route("/2025/speakers/")
def speakers_listing(lang="fr"):
    return render_template(
        f"{lang}/speakers.jinja2.html",
        page_name="speakers",
        speakers=Speaker.get_all(),
        lang=lang,
    )


@app.route("/2025/speakers/<slug>")
def speakers_details(slug, lang="fr"):
    return render_template(
        f"{lang}/speakers-details.jinja2.html",
        page_name="speakers",
        item=Speaker.get_item(slug),
        lang=lang,
    )


@app.route("/2025/sponsors/")
def sponsors_listing(lang="fr"):
    return render_template(
        f"{lang}/sponsors.jinja2.html",
        page_name="sponsors",
        speakers=Sponsors.get_all(),
        lang=lang,
    )


@app.route("/2025/sponsors/<item>")
def sponsors_details(item, lang="fr"):
    return render_template(
        f"{lang}/sponsors-details.jinja2.html",
        page_name="sponsors",
        item=Sponsors.get_item(item),
        lang=lang,
    )


@app.route("/2025/presentations/")
def talks_listing(lang="fr"):
    return render_template(
        f"{lang}/talks.jinja2.html",
        page_name="talks",
        speakers=Talks.get_all(),
        lang=lang,
    )


@app.route("/2025/presentations/<item>")
def talks_details(item, lang="fr"):
    return render_template(
        f"{lang}/presentation-details.jinja2.html",
        page_name="talks",
        item=Talks.get_item(item),
        lang=lang,
    )


@app.route("/2025/actualites/")
def news_listing(lang="fr"):
    return render_template(
        f"{lang}/news.jinja2.html",
        page_name="news",
        news=News.get_all(),
        lang=lang,
    )


@app.route("/2025/calendar.ics")
def calendar(lang):
    ics = render_template("calendar.jinja2.ics", lang=lang)
    return Response(ics, mimetype="text/calendar")


@app.route("/")
@app.route("/2025/")
def page(name="index", lang="fr"):
    return render_template(f"{lang}/{name}.jinja2.html", page_name=name, lang=lang)


@app.cli.command("freeze")
def freeze():
    Freezer(app).freeze()
