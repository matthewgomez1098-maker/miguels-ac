#!/usr/bin/env python3
"""Local preview server for the Miguel's A/C static site.

    python3 miguels-ac/serve.py [port]

Serves this folder at http://localhost:8077 so the root-absolute links
(/index.html, /assets/...) resolve the same way they will in production.

Three things this does that `python3 -m http.server` does not, all of which you
notice immediately when clicking between pages:

  * HTTP/1.1 with keep-alive, so the browser reuses one connection for the page
    and its assets instead of opening a fresh socket per request.
  * Threaded, so those asset requests are served in parallel rather than queued.
  * Cache-Control: no-cache — meaning "revalidate", not "don't cache". The
    browser keeps the stylesheet, fonts and logo, and each navigation costs a
    conditional request answered with an empty 304 instead of a re-download.
    Your edits still appear on the next reload.

Production hosts (Vercel, Netlify, Pages) handle compression and long-lived
asset caching for you; see the README.
"""
import functools
import gzip
import http.server
import io
import os
import socketserver
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8077

COMPRESSIBLE = (".html", ".css", ".js", ".json", ".xml", ".svg", ".txt")
MIN_GZIP = 1024


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"          # keep-alive
    server_version = "MiguelsAC-dev"

    def end_headers(self):
        # "no-cache" = cache it, but revalidate before reuse. The opposite of
        # "no-store", which forces a full re-download on every navigation.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        """Serve gzipped when the client accepts it and the file is worth it.

        This path has to do its own conditional-request handling: the base
        class's If-Modified-Since check lives in the branch we're replacing, and
        skipping it would make every navigation re-download the stylesheet.
        """
        path = self.translate_path(self.path)
        if os.path.isdir(path) or not path.lower().endswith(COMPRESSIBLE):
            return super().send_head()
        if "gzip" not in self.headers.get("Accept-Encoding", ""):
            return super().send_head()
        try:
            st = os.stat(path)
        except OSError:
            return super().send_head()          # let the base class 404 it
        if st.st_size < MIN_GZIP:
            return super().send_head()

        # Encoding-specific: a gzipped body must not share an ETag with the
        # identity body, or a cache can hand back the wrong bytes.
        etag = '"%x-%x-gz"' % (int(st.st_mtime), st.st_size)
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            self.send_header("ETag", etag)
            self.end_headers()
            return None

        body = gzip.compress(open(path, "rb").read(), 6)
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Last-Modified", self.date_time_string(st.st_mtime))
        self.send_header("ETag", etag)
        self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        return io.BytesIO(body)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=ROOT)
    with Server(("127.0.0.1", PORT), handler) as httpd:
        print("Miguel's A/C serving %s at http://localhost:%d" % (ROOT, PORT))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
