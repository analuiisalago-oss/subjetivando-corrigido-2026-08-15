#!/usr/bin/env python3
"""Gera a pasta pública do Subjetivando a partir do HTML canônico.

O script separa CSS e JavaScript sem alterar o conteúdo do acervo. A pasta
``public`` é o único diretório que deve ser publicado no Netlify.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "minha-banca.NOVO_3.html"
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")

    style_match = re.search(r"(?s)\s*<style>(.*?)</style>", html)
    if not style_match:
        raise SystemExit("Bloco <style> principal não encontrado.")
    css = style_match.group(1).strip() + "\n"
    html = html[: style_match.start()] + '\n    <link rel="stylesheet" href="/assets/styles.css" />' + html[style_match.end() :]

    tail_start = html.find('<script id="audio-shim">')
    tail_end = html.rfind("</script>")
    if tail_start < 0 or tail_end < tail_start:
        raise SystemExit("Camadas JavaScript da aplicação não encontradas.")
    tail_end += len("</script>")
    tail = html[tail_start:tail_end]
    scripts = re.findall(r"(?s)<script(?:\s+id=\"[^\"]+\")?>\s*(.*?)</script>", tail)
    if len(scripts) != 9:
        raise SystemExit(f"Esperadas 9 camadas JavaScript; encontradas {len(scripts)}.")

    js = "\n\n;\n\n".join(bloco.strip() for bloco in scripts) + "\n"
    html = html[:tail_start] + '    <script src="/assets/app.js"></script>\n' + html[tail_end:]

    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "styles.css").write_text(css, encoding="utf-8")
    (ASSETS / "app.js").write_text(js, encoding="utf-8")
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")

    for name in ("_redirects", "_headers", "robots.txt"):
        shutil.copy2(ROOT / name, PUBLIC / name)

    print(f"public/index.html: {len(html.encode('utf-8')):,} bytes")
    print(f"public/assets/styles.css: {len(css.encode('utf-8')):,} bytes")
    print(f"public/assets/app.js: {len(js.encode('utf-8')):,} bytes")


if __name__ == "__main__":
    main()

