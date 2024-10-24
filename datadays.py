from datetime import date, time, timedelta, datetime
from pathlib import Path
from flask import Flask, Response, render_template
from flask_frozen import Freezer
from markdown2 import Markdown
from sassutils.wsgi import SassMiddleware
from slugify import slugify
from models import load_data, Speaker, Sponsors, Talks

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


SCHEDULE = {
    "speakers": load_data(app.root_path, Speaker),
    "sponsors": load_data(app.root_path, Sponsors),
    "talks": load_data(app.root_path, Talks),
}

_GIT_MAIN = Path(app.root_path) / ".git" / "refs" / "heads" / "main"
GIT_VERSION = _GIT_MAIN.read_text().strip()[:7]


@app.template_filter()
def slug(string):
    return slugify(string, max_length=30)


@app.template_filter()
def markdown(string):
    return Markdown().convert(string)


@app.template_filter()
def version(url):
    return f"{url}?{GIT_VERSION}"


@app.route("/")
@app.route("/2025/")
@app.route("/2025/<name>")
def page(name="index", lang="fr"):
    return render_template(f"{lang}/{name}.jinja2.html", page_name=name, lang=lang)


@app.route("/2025/calendar.ics")
def calendar(lang):
    ics = render_template("calendar.jinja2.ics", lang=lang)
    return Response(ics, mimetype="text/calendar")


@app.cli.command("freeze")
def freeze():
    Freezer(app).freeze()
