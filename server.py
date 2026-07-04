import json
import os
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HOST = "0.0.0.0"
PORT = 8000
BUFFER = 1024 * 1024


def get_local_ips():
    ips = set()
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM):
            ips.add(info[4][0])
    except OSError:
        pass

    if not ips:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ips.add(s.getsockname()[0])
        except OSError:
            pass
        finally:
            s.close()

    return sorted(ip for ip in ips if not ip.startswith("127."))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._send_json(200, {
                "status": "ok",
                "hostname": socket.gethostname(),
                "addresses": [f"{ip}:{PORT}" for ip in get_local_ips() or ["127.0.0.1"]],
                "pid": os.getpid(),
                "uptime": time.time(),
            })
            return

        if parsed.path == "/api/throughput":
            params = parse_qs(parsed.query)
            try:
                size = int(params.get("size", [BUFFER])[0])
            except ValueError:
                size = BUFFER
            data = os.urandom(min(size, 10 * 1024 * 1024))
            body = data[:size]
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path in ["/", "/index.html", "/styles.css", "/script.js"]:
            file_path = parsed.path.lstrip("/") or "index.html"
            if os.path.exists(file_path):
                with open(file_path, "rb") as fh:
                    content = fh.read()
                mime = "text/html" if file_path.endswith(".html") else "text/css" if file_path.endswith(".css") else "application/javascript"
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        self._send_json(404, {"error": "not found"})

    def log_message(self, format, *args):
        return

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
