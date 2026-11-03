# =============================================================================
# CHANGER D'ÉDITION (ex. 2027 -> 2028)
# -----------------------------------------------------------------------------
# Principe : le site de l'année en cours est généré par Flask (routes /AAAA/...),
# les éditions passées sont des builds statiques figés dans old_editions/AAAA/.
#
# 1. Archiver l'édition sortante (avant de toucher au code) :
#      make static
#      cp -R build/2027 old_editions/2027
#      rm -rf old_editions/2027/static/sass old_editions/2027/static/homepage.html
#    (les slides de static/slides partent avec l'archive : `git rm -r static/slides`)
#
# 2. Données : git mv data/current data/2027
#    puis recréer data/current/{news,speakers,sponsors,talks}/.gitkeep (vides).
#
# 3. Remplacer l'année dans le code (lister avec : grep -rn 2027 datadays.py Makefile static/sass templates) :
#      - datadays.py          : static_url_path, wsgi_path, toutes les routes /2027/
#      - Makefile             : les deux `cp build/2027/index.html ...` de la cible static
#      - static/sass/style.sass : chemins /2027/static (police, images)
#      - templates/_layout.jinja2 : titres, meta description, JSON-LD (date !),
#                               logo, footer ©, ajouter 2027 dans "Éditions précédentes"
#      - templates/fr/index.jinja2.html : titre, date, n° d'édition, textes, boutons
#      - templates/fr/qrcode.jinja2.html : URL par défaut
#
# 4. Image de partage (aperçus LinkedIn/WhatsApp) : créer static/images/og-2028.jpg
#    (1200x630) et mettre à jour son nom dans _layout.jinja2.
#
# 5. Tant que CFP / programme / inscriptions ne sont pas ouverts : commenter les
#    routes speakers, presentations, programme, infos dans datadays.py et les
#    retirer du MENU de _layout.jinja2 (url_for plante sinon). Les réactiver ensuite.
#
# 6. netlify.toml : vérifier la redirection /programme (pointe vers le dernier
#    programme publié). La racine / n'a pas de redirection : `make static` y copie
#    l'accueil de l'édition en cours.
#
# 7. Vérifier : make static && make serve-static, puis tester /, /2028/ et les
#    archives (/2027/, /2026/...). Après déploiement, rafraîchir l'aperçu LinkedIn
#    via https://www.linkedin.com/post-inspector/
#
# Hors de ce repo : le lien du site data-lille.fr pointe sur days.data-lille.fr
# (libellé sans année, rien à changer).
# =============================================================================

.venv:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

install: .venv

static: .venv
	.venv/bin/flask --app=datadays freeze
	# add an index manually to the french directory
	cp -r old_editions/* build
	cp build/2027/index.html build/2027/fr/index.html
	# la racine sert directement l'accueil de l'édition en cours (pas de redirection, meilleurs aperçus de lien)
	cp build/2027/index.html build/index.html

serve: .venv
	@echo -e "\nHome page available at \033[0;32mhttp://localhost:5000/\033[0m\n"
	.venv/bin/flask --app=datadays run --debug

serve-static: .venv
	@echo -e "\nHome page available at \033[0;33mhttp://localhost:9898/\033[0m\n"
	cd build && ../.venv/bin/python ../http_server.py 9898

schedule: .venv
	.venv/bin/python schedule.py


square_logo:
	# makes a square logo using imagemagick
	magick xc:none sfeir.png -thumbnail 720x720 -gravity center -composite sfeir_square.png

publish_all:
	find data/talks -name "*.md" -exec sed -i '' 's/published: false/published: true/' {} \;
	find data/speakers -name "*.md" -exec sed -i '' 's/published: false/published: true/' {} \;

unpublish_all:
	find data/talks -name "*.md" -exec sed -i '' 's/published: true/published: false/' {} \;
	find data/speakers -name "*.md" -exec sed -i '' 's/published: true/published: false/' {} \;

parse_selection:
	.venv/bin/python script/parse_selection.py ./selection.json

download_avatars:
	.venv/bin/python script/download_avatars.py

slugify_slides:
	.venv/bin/python scripts/slugify_slides.py

clean:
	rm -rf build .venv __pycache__

.PHONY: install static serve serve-static deploy clean slugify_slides
