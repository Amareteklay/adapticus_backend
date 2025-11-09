# content/utils.py
from __future__ import annotations

from typing import Optional

# Supported languages (align with settings.LANGUAGES/PARLER_LANGUAGES)
SUPPORTED_LANGS = ("en", "sv", "ti-et")
DEFAULT_LANG = "en"

# Supported sites (align with core.models.Site choices)
DEFAULT_SITE = "amare"
SUPPORTED_SITES = ("amare", "adapticus")


def pick_lang(value: Optional[str]) -> str:
    """
    Choose the best language code given a query/header value.
    Accepts things like: 'sv', 'sv-SE,en;q=0.8', 'en-US', 'ti', 'ti-et'
    """
    if not value:
        return DEFAULT_LANG

    v = value.strip().lower()
    # Handle Accept-Language lists
    v = v.split(",")[0].strip()

    # Exact match first
    if v in SUPPORTED_LANGS:
        return v

    # Normalize common variants/short forms
    if v.startswith("sv"):
        return "sv"
    if v.startswith("en"):
        return "en"
    if v in ("ti", "ti-er", "ti-et"):
        return "ti-et"

    return DEFAULT_LANG


def request_lang(request) -> str:
    """
    Priority:
      1) ?lang=...
      2) Accept-Language header
      3) DEFAULT_LANG
    """
    q = request.query_params.get("lang")
    if q:
        return pick_lang(q)
    hdr = request.headers.get("Accept-Language")
    if hdr:
        return pick_lang(hdr)
    return DEFAULT_LANG


def request_site(request) -> str | None:
    s = (request.query_params.get("site") or "").strip().lower()
    if not s:
        return DEFAULT_SITE 
    return s if s in SUPPORTED_SITES else None