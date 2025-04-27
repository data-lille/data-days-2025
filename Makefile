.venv:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

install: .venv

static: .venv
	.venv/bin/flask --app=datadays freeze
	# add an index manually to the french directory
	cp build/2025/index.html build/2025/fr/index.html
	cp static/homepage.html build/index.html

serve: .venv
	@echo -e "\nHome page available at \033[0;32mhttp://localhost:5000/\033[0m\n"
	.venv/bin/flask --app=datadays run --debug

serve-static: .venv
	@echo -e "\nHome page available at \033[0;33mhttp://localhost:8000/\033[0m\n"
	cd build && ../.venv/bin/python ../http_server.py 8000

schedule: .venv
	.venv/bin/python schedule.py

deploy: static
	rsync -vazh --delete build/2024/ datadays@deb2.afpy.org:/var/www/pycon.fr/2024/

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
