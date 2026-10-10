"""SEO / GEO / AIO filename and hidden-metadata contract for /folio.

Do not invent a second house host. Resolve the live 301 from
https://www.DigitalMarketingCo.org and https://DigitalMarketingCo.org
at build time. The measured apex in September 2026 is

    https://DigitalMarketingCo.org

Publication path on that host is /white-papers/{slug}, matching the
existing white-paper URLs on the site.
"""

from __future__ import annotations

import re
import subprocess
from datetime import date, datetime, timezone
from urllib.parse import urlparse

SEED_URLS = (
    "https://www.DigitalMarketingCo.org/",
    "https://DigitalMarketingCo.org/",
)
FALLBACK_ORIGIN = "https://DigitalMarketingCo.org"
PUBLICATION_PATH = "/white-papers"
DOC_TYPE_TOKEN = "wca-folio"

STOP = {
    "a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "at",
    "by", "with", "from", "into", "over", "about", "as", "is", "are",
}

# Operating geography published on the house homepage; legal seat is Delaware.
GEO_COVERAGE = (
    "Baltimore, Maryland, United States; "
    "1 East Chase Street, Suite 1117, Baltimore, MD 21202; "
    "Delaware corporation, United States"
)
GEO_COUNTRY = "US"
GEO_REGION = "US-MD"
GEO_LOCALITY = "Baltimore"


def resolve_canonical_origin(timeout: int = 12) -> str:
    """Follow house 301s. www currently 301s to the apex; apex returns 200."""
    for seed in SEED_URLS:
        try:
            proc = subprocess.run(
                [
                    "curl", "-sI", "-L", "--max-redirs", "8",
                    "-A", "WCAFolio/1.1",
                    "-o", "/dev/null",
                    "-w", "%{url_effective}",
                    seed,
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            raw = (proc.stdout or "").strip()
            if not raw:
                continue
            parsed = urlparse(raw)
            if parsed.scheme in {"http", "https"} and parsed.netloc:
                origin = f"{parsed.scheme}://{parsed.netloc}".lower()
                # Prefer apex if both answer; strip a trailing www if the
                # effective URL still carried it after a partial chain.
                if origin.startswith("https://www."):
                    apex = "https://" + origin.removeprefix("https://www.")
                    return apex.rstrip("/")
                return origin.rstrip("/")
        except Exception:
            continue
    return FALLBACK_ORIGIN


def slugify_title(title: str, *, max_words: int = 10) -> str:
    text = (title or "").lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[:/;,.—–—]+", " ", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    words = [w for w in text.split() if w and w not in STOP]
    if not words:
        words = ["academic-report"]
    words = words[:max_words]
    slug = "-".join(words)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug[:72].rstrip("-")


def folio_filename(title: str, year: int | None = None) -> str:
    """SEO + AIO + academic filename.

    Pattern: YYYY-topic-slug-wca-folio.pdf
    Hyphens, lowercase, year first, publisher token last, no FINAL/v2 junk.
    """
    year = int(year or date.today().year)
    slug = slugify_title(title)
    if DOC_TYPE_TOKEN not in slug:
        slug = f"{slug}-{DOC_TYPE_TOKEN}"
    name = f"{year}-{slug}.pdf"
    if len(name) > 96:
        # Keep year + token; trim the middle.
        core = slugify_title(title, max_words=6)
        name = f"{year}-{core}-{DOC_TYPE_TOKEN}.pdf"
    return name


def publication_slug(filename: str) -> str:
    stem = filename.rsplit(".", 1)[0]
    stem = re.sub(r"^\d{4}-", "", stem)
    return stem


def canonical_record_url(filename: str, origin: str | None = None) -> str:
    origin = (origin or FALLBACK_ORIGIN).rstrip("/")
    return f"{origin}{PUBLICATION_PATH}/{publication_slug(filename)}"


def document_id(filename: str, year: int | None = None) -> str:
    year = int(year or date.today().year)
    slug = publication_slug(filename)
    return f"wca:folio:{year}:{slug}"


def keyword_string(keywords: list[str] | None, extra: list[str] | None = None) -> str:
    seen: list[str] = []
    for item in list(keywords or []) + list(extra or []):
        item = (item or "").strip()
        if item and item not in seen:
            seen.append(item)
    return ", ".join(seen)


def info_dictionary(
    *,
    title: str,
    author: str,
    abstract: str,
    keywords: list[str],
    filename: str,
    origin: str,
    year: int,
    owner_legal: str,
    house_anchor: str,
) -> dict[str, str]:
    record = canonical_record_url(filename, origin)
    ident = document_id(filename, year)
    subject = " ".join((abstract or "").split())
    if len(subject) > 280:
        subject = subject[:277].rstrip() + "..."
    if not subject:
        subject = f"{title}. Canonical record {record}"
    kw = keyword_string(
        keywords,
        extra=[
            house_anchor,
            "Web Development Corporation",
            "WCA Folio",
            "Chicago notes-bibliography",
            "Ivy League academic report",
            "Baltimore Maryland",
            "Delaware corporation",
            record,
        ],
    )
    return {
        "/Title": title,
        "/Author": author,
        "/Subject": subject,
        "/Keywords": kw,
        "/Creator": owner_legal,
        "/Producer": "WCA Folio / Web Development Corporation",
        "/Identifier": ident,
        "/URL": record,
        "/Canonical": record,
        "/Publisher": f"{owner_legal} / {house_anchor}",
        "/Copyright": f"© {2012}–{year} {owner_legal}",
        "/Language": "en-US",
        "/Coverage": GEO_COVERAGE,
        "/Type": "ScholarlyArticle",
        "/Source": record,
        "/Relation": origin + "/",
    }


def xmp_payload(
    *,
    title: str,
    author: str,
    abstract: str,
    keywords: list[str],
    filename: str,
    origin: str,
    year: int,
    owner_legal: str,
    house_anchor: str,
) -> object:
    from pypdf.xmp import XmpInformation

    record = canonical_record_url(filename, origin)
    ident = document_id(filename, year)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    xmp = XmpInformation.create()
    xmp.dc_title = {"x-default": title, "en-US": title}
    xmp.dc_creator = [author, owner_legal]
    xmp.dc_description = {
        "x-default": (abstract or title)[:1000],
        "en-US": (abstract or title)[:1000],
    }
    xmp.dc_subject = list(keywords or []) + [
        "WCA Folio",
        house_anchor,
        "Chicago notes-bibliography",
        "Baltimore",
        "Delaware",
    ]
    xmp.dc_publisher = [owner_legal, house_anchor]
    xmp.dc_identifier = ident
    xmp.dc_language = ["en-US"]
    xmp.dc_format = "application/pdf"
    xmp.dc_type = ["Text", "ScholarlyArticle"]
    rights = f"© 2012–{year} {owner_legal}. All rights reserved."
    xmp.dc_rights = {"x-default": rights, "en-US": rights}
    xmp.dc_source = record
    xmp.dc_relation = [record, origin + "/", origin + PUBLICATION_PATH + "/"]
    xmp.dc_coverage = GEO_COVERAGE
    xmp.dc_date = [f"{year}-01-01", now]
    xmp.pdf_keywords = keyword_string(keywords, extra=["WCA Folio", house_anchor])
    xmp.xmp_creator_tool = "WCA Folio"
    try:
        xmp.custom_properties["CanonicalURL"] = record
        xmp.custom_properties["HouseOrigin"] = origin
        xmp.custom_properties["GeoCountry"] = GEO_COUNTRY
        xmp.custom_properties["GeoRegion"] = GEO_REGION
        xmp.custom_properties["GeoLocality"] = GEO_LOCALITY
        xmp.custom_properties["DocumentType"] = "ScholarlyArticle"
        xmp.custom_properties["CitationStyle"] = "Chicago notes-bibliography (WCA Folio)"
        xmp.custom_properties["SchemaType"] = "https://schema.org/ScholarlyArticle"
        xmp.custom_properties["sameAs"] = record
    except Exception:
        pass
    return xmp
