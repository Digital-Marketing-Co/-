#!/usr/bin/env python3
"""
Schemata extraction and JSON-LD graph builder.
Deterministic local processing for document-to-Schema.org conversion.
"""
import argparse
import hashlib
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any

# Optional imports with graceful fallbacks
try:
    import pdfplumber
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

VOCAB_PATH = Path(__file__).parent.parent / "assets" / "schemaorg-all-https.jsonld"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_text(path: Path) -> dict[str, Any]:
    """Extract content with structural records. Returns dict with status and sections."""
    suffix = path.suffix.lower()
    result = {
        "path": str(path),
        "digest": sha256_file(path),
        "status": "ok",
        "completeness": "full",
        "sections": [],
        "warnings": [],
    }
    try:
        if suffix == ".pdf" and HAS_PDF:
            with pdfplumber.open(path) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    if text.strip():
                        result["sections"].append({
                            "id": f"page-{i}",
                            "type": "page",
                            "ordinal": i,
                            "text": text,
                            "locator": f"page {i}",
                        })
        elif suffix in (".docx", ".doc") and HAS_DOCX:
            doc = Document(path)
            for i, para in enumerate(doc.paragraphs):
                if para.text.strip():
                    result["sections"].append({
                        "id": f"para-{i}",
                        "type": "paragraph",
                        "ordinal": i,
                        "text": para.text,
                        "locator": f"paragraph {i}",
                    })
        elif suffix in (".html", ".htm") and HAS_BS4:
            soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
            for i, tag in enumerate(soup.find_all(["h1", "h2", "h3", "p", "li"])):
                text = tag.get_text(strip=True)
                if text:
                    result["sections"].append({
                        "id": f"el-{i}",
                        "type": tag.name,
                        "ordinal": i,
                        "text": text,
                        "locator": tag.name,
                    })
        elif suffix in (".md", ".txt", ".json"):
            text = path.read_text(encoding="utf-8", errors="replace")
            # Simple paragraph split
            paras = [p.strip() for p in text.split("\n\n") if p.strip()]
            for i, p in enumerate(paras):
                result["sections"].append({
                    "id": f"block-{i}",
                    "type": "block",
                    "ordinal": i,
                    "text": p[:2000],  # cap long blocks
                    "locator": f"offset {i}",
                })
        else:
            result["status"] = "unsupported"
            result["completeness"] = "none"
            result["warnings"].append(f"No verified adapter for {suffix}")
    except Exception as e:
        result["status"] = "error"
        result["completeness"] = "partial"
        result["warnings"].append(str(e))
    return result


def build_document_graph(extraction: dict, canonical: str | None = None) -> dict:
    """Build a minimal but valid Schema.org JSON-LD graph for one document."""
    doc_id = canonical or f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, extraction['digest'])}"
    sections = extraction.get("sections", [])
    title = sections[0]["text"][:120] if sections else Path(extraction["path"]).stem

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@id": doc_id,
                "@type": "CreativeWork",
                "name": title,
                "identifier": extraction["digest"][:16],
            }
        ],
    }
    # Add parts if meaningful
    parts = []
    for sec in sections[:50]:  # limit
        if len(sec["text"]) > 20:
            part_id = f"{doc_id}#{sec['id']}"
            parts.append({
                "@id": part_id,
                "@type": "CreativeWork",
                "name": sec["text"][:80],
                "isPartOf": {"@id": doc_id},
            })
    if parts:
        graph["@graph"].extend(parts)
        graph["@graph"][0]["hasPart"] = [{"@id": p["@id"]} for p in parts]
    return graph


def main():
    parser = argparse.ArgumentParser(description="Schemata CLI: document to Schema.org JSON-LD")
    parser.add_argument("inputs", nargs="+", help="Input document paths")
    parser.add_argument("-o", "--output", default="./schemata-out", help="Output directory")
    parser.add_argument("--canonical", action="append", default=[], help="canonical=path=url mappings")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    manifest = []
    graphs = []
    for inp in args.inputs:
        p = Path(inp)
        if not p.exists():
            print(f"Missing: {inp}", file=sys.stderr)
            continue
        ext = extract_text(p)
        manifest.append({
            "id": ext["digest"][:16],
            "path": str(p),
            "digest": ext["digest"],
            "status": ext["status"],
            "sections": len(ext.get("sections", [])),
        })
        if ext["status"] == "ok":
            g = build_document_graph(ext)
            graphs.append(g)
            (out / f"{p.stem}.jsonld").write_text(json.dumps(g, indent=2))

    # Corpus consolidation (simple union for demo)
    corpus = {
        "@context": "https://schema.org",
        "@graph": [],
    }
    seen = set()
    for g in graphs:
        for node in g.get("@graph", []):
            nid = node.get("@id")
            if nid and nid not in seen:
                seen.add(nid)
                corpus["@graph"].append(node)

    (out / "corpus.jsonld").write_text(json.dumps(corpus, indent=2))
    (out / "corpus.min.jsonld").write_text(json.dumps(corpus, separators=(",", ":")))
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    # Safe HTML block
    escaped = json.dumps(corpus).replace("<", "\\u003c")
    html = f'<script type="application/ld+json">{escaped}</script>'
    (out / "corpus-jsonld.html").write_text(html)

    print(f"Wrote outputs to {out}")
    print(f"Documents processed: {len(manifest)}")


if __name__ == "__main__":
    main()
