"""Fail closed if the generated Pages artifact leaks tooling or loses its policy."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

POLICY = {
    "default-src": "'none'", "script-src": "'none'", "style-src": "'self'",
    "font-src": "'self'", "img-src": "'self' data:", "connect-src": "'none'",
    "object-src": "'none'", "base-uri": "'none'", "form-action": "'none'",
    "frame-src": "'none'",
}


class Page(HTMLParser):
    def __init__(self, path, root):
        super().__init__(convert_charrefs=True)
        self.path, self.root = path, root
        self.policy = None
        self.referrer = None

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        assert tag not in {"script", "iframe", "object", "embed", "base", "form"}, (self.path, tag)
        assert not any(k.lower().startswith("on") or k.lower() == "style" for k, _ in attrs), (self.path, attrs)
        if tag == "meta":
            if a.get("http-equiv", "").lower() == "content-security-policy":
                assert self.policy is None, "Duplicate CSP"
                self.policy = dict(part.strip().split(None, 1) for part in a["content"].split(";") if part.strip())
            if a.get("name") == "referrer":
                self.referrer = a.get("content")
        if tag == "link" and a.get("rel") in {"stylesheet", "preconnect"}:
            assert not urlsplit(a.get("href", "")).netloc, (self.path, "Third-party stylesheet/connection")
        if a.get("target") == "_blank":
            assert {"noopener", "noreferrer"} <= set(a.get("rel", "").split()), self.path
        for attr in ("src", "href"):
            if attr not in a:
                continue
            url = urlsplit(a[attr])
            assert url.scheme not in {"javascript", "vbscript"}, (self.path, a[attr])
            if attr == "src":
                assert not url.scheme and not url.netloc, (self.path, "External asset")
            if url.scheme or url.netloc or not url.path:
                continue
            target = ((self.root / unquote(url.path).lstrip("/")) if url.path.startswith("/") else self.path.parent / unquote(url.path)).resolve()
            assert target.is_relative_to(self.root), (self.path, "Path traversal")
            assert target.exists() or target.with_suffix(".html").exists(), (self.path, "Missing local target", target)


def check(root):
    root = Path(root).resolve()
    assert root.is_dir(), "Build output missing"
    pages = 0
    for path in root.rglob("*"):
        assert not path.is_symlink(), (path, "Symlink in artifact")
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        allowed = rel in {"index.html", "about/index.html", "feed.xml", "CNAME", ".nojekyll", ".well-known/security.txt"}
        allowed |= bool(re.fullmatch(r"(?:[\w-]+/)*\d{4}/\d{2}/\d{2}/[\w-]+\.html", rel))
        if rel.startswith("assets/"):
            allowed |= path.suffix in {".css", ".png", ".woff2", ".ttf"} or rel in {"assets/fonts/archivo-OFL.txt", "assets/fonts/jetbrains-mono-OFL.txt"}
        assert allowed, (rel, "Unexpected file in public artifact")
        if path.suffix == ".html":
            page = Page(path, root)
            page.feed(path.read_text())
            assert page.policy == POLICY, (rel, "Missing or weakened CSP", page.policy)
            assert page.referrer == "no-referrer", (rel, "Missing referrer policy")
            pages += 1
        if path.suffix == ".css":
            css = path.read_text()
            assert not re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", css), (rel, "External CSS dependency")
            for match in re.finditer(r'''url\(\s*(?:"([^"]*)"|'([^']*)'|([^'")]*))\s*\)''', css):
                url = next(value for value in match.groups() if value is not None)
                if url.startswith("data:image/"):
                    continue
                target = (path.parent / url).resolve()
                assert target.is_relative_to(root) and target.is_file(), (rel, "Missing CSS asset", url)
    assert pages >= 4, "Expected home, about, and both posts"
    assert (root / "CNAME").read_text().strip() == "mobekk.blog"
    assert (root / ".well-known/security.txt").is_file()
    print(f"Validated {pages} HTML pages, local assets, policies, and artifact boundaries.")


if __name__ == "__main__":
    check(sys.argv[1] if len(sys.argv) > 1 else "_site")
