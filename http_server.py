# https://stackoverflow.com/questions/56825520/using-python-simplehttpserver-to-serve-files-without-html

# To have nice urls, I removed the ".html" extensions on the files, so it can break
# when using http.serve module

import http.server
import socketserver
import os
import pathlib
import sys

PORT = 8000
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
DIRECTORY = "build"


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        "": "application/octet-stream",
        ".manifest": "text/cache-manifest",
        ".html": "text/html",
        ".png": "image/png",
        ".jpg": "image/jpg",
        ".svg": "image/svg+xml",
        ".css": "text/css",
        ".js": "application/x-javascript",
        ".wasm": "application/wasm",
        ".json": "application/json",
        ".xml": "application/xml",
    }

    def __init__(self, *args, directory=None, **kwargs):
        directory = pathlib.Path(os.getcwd()) / DIRECTORY
        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)


httpd = socketserver.TCPServer(("localhost", PORT), HttpRequestHandler)

try:
    print(f"serving at http://localhost:{PORT}")
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
