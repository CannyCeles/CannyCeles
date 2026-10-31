import datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Load template SVG on cold start
TEMPLATE_SVG = ""
for candidate in [
    Path(__file__).parent / "sun_moon_clock.svg",
    Path(__file__).parent.parent / "sun_moon_clock.svg",
    Path("sun_moon_clock.svg"),
]:
    if candidate.exists():
        TEMPLATE_SVG = candidate.read_text(encoding="utf-8")
        break


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Calculate current Asia/Jakarta (WIB · UTC+7) seconds into day
        tz_wib = datetime.timezone(datetime.timedelta(hours=7))
        now = datetime.datetime.now(tz_wib)
        t = now.hour * 3600 + now.minute * 60 + now.second

        # Calculate negative animation delays
        d_day = -(t % 86400)
        d_hour = -(t % 43200)
        d_min = -(t % 3600)

        # Substitute time offsets into SVG (hand styles first, then general day/night delays)
        svg = (
            TEMPLATE_SVG
            .replace(
                'class="hand-hour" style="animation-delay: -36600s;"',
                f'class="hand-hour" style="animation-delay: {d_hour}s;"',
            )
            .replace(
                'class="hand-min" style="animation-delay: -600s;"',
                f'class="hand-min" style="animation-delay: {d_min}s;"',
            )
            .replace("animation-delay: -36600s;", f"animation-delay: {d_day}s;")
        )

        content = svg.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Cache-Control", "max-age=0, no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        pass
