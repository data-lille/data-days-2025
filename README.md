# Data Days 2025 homepage

Forked from AFPy/pyconfr-2024:main

This repository host the website for the data days 2025. 
It's hosted on netlify.

## Technical 

* build using flask for the template hydratation 
* static site is generated using flask-frozen 
* static site is hosted on netlify 

To build the site : 
* in local `make serve` to have flask handle the requests (useful to debug / have dynamic updates)
* in CI `make static` will generate the static HTML pages using frozen flask