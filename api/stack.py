from http.server import BaseHTTPRequestHandler
from pathlib import Path

STACK_SVG = ""
for candidate in [
    Path(__file__).parent / "tech_stack.svg",
    Path(__file__).parent.parent / "tech_stack.svg",
    Path("tech_stack.svg"),
]:
    if candidate.exists():
        STACK_SVG = candidate.read_text(encoding="utf-8")
        break


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = STACK_SVG.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "public, max-age=86400, s-maxage=86400")
        self.end_headers()
        self.wfile.write(content)
