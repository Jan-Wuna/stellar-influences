# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py", "beautifulsoup4", "pydantic>=2", "pyyaml"]
# ///
from __future__ import annotations

import html
import re
import socket
import unicodedata
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import BaseServer
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from validate_review import ROOT, load_page

MARKDOWN = MarkdownIt("commonmark", {"html": True}).enable("table")
STYLE = """:root{color-scheme:light;--text:#242424;--muted:#666;--line:#d7d7d7;--link:#174f92}
*{box-sizing:border-box}body{margin:0;color:var(--text);background:white;
font:17px/1.65 Georgia,'Times New Roman',serif}main{max-width:900px;margin:auto;
padding:32px 28px 80px}h1,h2,h3,h4{font-family:system-ui,sans-serif;line-height:1.3;
overflow-wrap:anywhere}h1{font-size:2rem}h2{margin-top:2.2rem;font-size:1.5rem;
border-bottom:1px solid var(--line);padding-bottom:.3rem}h3{margin-top:1.8rem}
a{color:var(--link);text-underline-offset:3px;overflow-wrap:anywhere}
code,pre{font-family:Consolas,monospace;font-size:.88em}code{background:#f3f3f3;
padding:.1em .2em;overflow-wrap:anywhere}pre{overflow:auto;padding:1em}
table{border-collapse:collapse;display:block;overflow-x:auto}td,th{border:1px solid
var(--line);padding:.5em .7em;text-align:left}img{max-width:100%;height:auto}
blockquote{margin-left:0;padding-left:1em;border-left:3px solid var(--line)}
.qa{font:12px/1.5 system-ui,sans-serif;color:var(--muted);overflow-wrap:anywhere}
@media(max-width:600px){main{padding:20px 16px 60px}body{font-size:16px}}
"""


def rendered_page(relative: str) -> bytes:
    page = load_page((ROOT, relative))
    soup = BeautifulSoup(MARKDOWN.render(page.body), "html.parser")
    explicit = {str(tag["id"]) for tag in soup.find_all(id=True)}
    used: set[str] = set()
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        slug = "".join(c for c in heading.get_text().lower() if c in "_- " or unicodedata.category(c)[0] not in {"P", "S", "C"}).replace(" ", "-")
        candidate, counter = slug, 0
        while candidate in used:
            counter += 1
            candidate = f"{slug}-{counter}"
        used.add(candidate)
        if candidate not in explicit:
            heading["id"] = candidate
    title = html.escape(str(page.metadata.get("title") or Path(relative).stem))
    source = html.escape(relative, quote=True)
    heading = f"<h1>{title}</h1>" if not soup.find("h1") else ""
    output = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>{STYLE}</style><body data-source-sha256="{page.sha256}" data-source="{source}">
<main><p class="qa">Read-only CommonMark QA preview · {source}</p>{heading}{soup}</main>
</body></html>"""
    return output.encode("utf-8")


class Reader(SimpleHTTPRequestHandler):
    def __init__(self, request: socket.socket, client_address: tuple[str, int], server: BaseServer) -> None:
        super().__init__(request, client_address, server, directory=str(ROOT))

    def do_GET(self) -> None:
        request_path = unquote(urlsplit(self.path).path).lstrip("/")
        target = (ROOT / request_path).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            self.send_error(404)
            return
        if target.suffix.lower() != ".md":
            super().do_GET()
            return
        body = rendered_page(target.relative_to(ROOT).as_posix())
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with ThreadingHTTPServer(("127.0.0.1", 8769), Reader) as server:
        print("Read-only wiki QA preview: http://127.0.0.1:8769/wiki/query-guide.md", flush=True)
        server.serve_forever()
