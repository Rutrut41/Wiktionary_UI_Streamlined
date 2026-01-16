from flask import Flask, render_template, request
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote
import json

app = Flask(__name__)

# --- Load language mappings ---
with open("DISPLAYED_LANGS_EXPANDED.json", "r", encoding="utf-8") as f:
    LANG_NATIVE_BY_INTERFACE = json.load(f)
DISPLAYED_LANGS_EXPANDED = LANG_NATIVE_BY_INTERFACE

with open("languages_reversed.json", "r", encoding="utf-8") as f:
    LANGUAGES = json.load(f)

DISPLAYED_LANGUAGES = {
    "English": "en", "Spanish": "es", "French": "fr", "Portuguese": "pt", "German": "de",
    "Italian": "it", "Russian": "ru", "Chinese": "zh", "Dutch": "nl", "Polish": "pl",
    "Swedish": "sv", "Finnish": "fi", "Hungarian": "hu", "Czech": "cs", "Japanese": "ja",
    "Korean": "ko", "Turkish": "tr", "Arabic": "ar", "Greek": "el", "Catalan": "ca",
    "Danish": "da", "Norwegian Bokmål": "no", "Esperanto": "eo", "Ukrainian": "uk",
    "Serbo-Croatian": "sh", "Slovak": "sk", "Thai": "th", "Lithuanian": "lt", "Romanian": "ro",
    "Hindi": "hi", "Bulgarian": "bg", "Estonian": "et", "Persian": "fa", "Icelandic": "is",
    "Irish": "ga", "Basque": "eu", "Hebrew": "he", "Vietnamese": "vi", "Latin": "la",
    "Malay": "ms", "Indonesian": "id", "Latvian": "lv", "Slovenian": "sl", "Breton": "br",
    "Welsh": "cy", "Albanian": "sq", "Armenian": "hy", "Azerbaijani": "az", "Bengali": "bn",
    "Swahili": "sw"
}

WIKTIONARY_API = "https://{site_lang}.wiktionary.org/w/api.php"
CACHE = {}
CACHE_EXPIRY = 3600
REDLINK_STYLE = "color:#d00; text-decoration:none; cursor:not-allowed;"


# --- HTML cleaning ---
def clean_html(html, current_site_lang="en", word=None):
    soup = BeautifulSoup(html, "html.parser")
    known_sections = []

    if word:
        sections_cached = CACHE.get((word.lower(), current_site_lang, "sections"))
        if sections_cached:
            sections_list = sections_cached[0]
            known_sections = [s.get("line", "").strip().lower() for s in sections_list if s.get("line")]

    for header in soup.find_all(["h2", "h3", "h4"]):
        if "#" in header.text:
            header.string = header.text.split("#")[-1].strip()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http://") or href.startswith("https://"):
            continue

        if "redlink=1" in href:
            a["href"] = "javascript:void(0);"
            a["style"] = REDLINK_STYLE
            continue

        if not href.startswith("/wiki/") or ":" in href.split("/wiki/", 1)[1]:
            a["href"] = f"https://{current_site_lang}.wiktionary.org{href}"
            continue

        path = href.split("/wiki/", 1)[1]
        parts = path.split("#")
        linked_word = unquote(parts[0]).strip()
        linked_anchor = unquote(parts[1]).strip() if len(parts) > 1 else None

        entry_code = current_site_lang
        if linked_anchor:
            anchor_norm = linked_anchor.replace("_", " ").strip().lower()
            mapping = DISPLAYED_LANGS_EXPANDED.get(current_site_lang, {})
            for display_name, code in mapping.items():
                if anchor_norm == display_name.lower():
                    entry_code = code
                    break
            if entry_code == current_site_lang:
                native_map = LANG_NATIVE_BY_INTERFACE.get(current_site_lang, {})
                for native_name, code in native_map.items():
                    if anchor_norm == native_name.lower():
                        entry_code = code
                        break
            if entry_code == current_site_lang:
                for name, code in LANGUAGES.items():
                    if anchor_norm == name.lower() or anchor_norm == code.lower():
                        entry_code = code
                        break

        # same-page redlink handling
        if word and linked_word.lower() == word.lower() and linked_anchor:
            anchor_norm = linked_anchor.replace("_", " ").strip().lower()
            if anchor_norm not in known_sections:
                a["href"] = "javascript:void(0);"
                a["style"] = REDLINK_STYLE
                continue
            safe_anchor = linked_anchor.replace(" ", "_")
            a["href"] = f"/link?word={linked_word}&site_language={current_site_lang}&entry_language={entry_code}#{safe_anchor}"
            continue

        a["href"] = f"/link?word={linked_word}&site_language={current_site_lang}&entry_language={entry_code}"

    return str(soup)


# --- Section lookup helper ---
def find_section(sections, site_lang_code, entry_lang_code):
    """
    Returns the section index for the entry language.
    If site_lang_code == "en", match the section header exactly (case-insensitive).
    Otherwise, allow partial match.
    """
    # 1. DISPLAYED_LANGS_EXPANDED
    entry_name = next((name for name, code in DISPLAYED_LANGS_EXPANDED.get(site_lang_code, {}).items()
                       if code == entry_lang_code), None)

    if site_lang_code == "en" and entry_name:
        for s in sections:
            if s.get("line", "").strip().lower() == entry_name.lower():
                return s.get("index")
        return None

    # Partial match fallback
    if entry_name:
        for s in sections:
            if entry_name.lower() in s.get("line", "").strip().lower():
                return s.get("index")

    # 2. LANG_NATIVE_BY_INTERFACE fallback
    dl_mapping = LANG_NATIVE_BY_INTERFACE.get(site_lang_code, {})
    entry_native_name = next((name for name, code in dl_mapping.items() if code == entry_lang_code), None)
    if entry_native_name:
        for s in sections:
            if entry_native_name.lower() in s.get("line", "").strip().lower():
                return s.get("index")

    # 3. LANGUAGES fallback
    entry_lang_name = next((name for name, code in LANGUAGES.items() if code == entry_lang_code), None)
    if entry_lang_name:
        for s in sections:
            if entry_lang_name.lower() in s.get("line", "").strip().lower():
                return s.get("index")

    return None


# --- Wiktionary fetching ---
def fetch_wiktionary_entry(word, site_lang_code="en", entry_lang_code="en"):
    if not word:
        return ""

    cache_key = (word.lower(), site_lang_code, entry_lang_code)
    cached = CACHE.get(cache_key)
    if cached and time.time() - cached[1] < CACHE_EXPIRY:
        return cached[0]

    url = WIKTIONARY_API.format(site_lang=site_lang_code)
    headers = {"User-Agent": "WiktionaryLookup/1.0"}

    try:
        params_sections = {"action": "parse", "page": word, "format": "json", "prop": "sections", "origin": "*"}
        response = requests.get(url, params=params_sections, headers=headers, timeout=15)
        response.raise_for_status()
        sections = response.json().get("parse", {}).get("sections", [])
        CACHE[(word.lower(), site_lang_code, "sections")] = (sections, time.time())

        section_id = find_section(sections, site_lang_code, entry_lang_code)
        entry_name = next((name for name, code in DISPLAYED_LANGS_EXPANDED.get(site_lang_code, {}).items()
                           if code == entry_lang_code), None) or entry_lang_code

        if section_id:
            params_text = {"action": "parse", "page": word, "format": "json", "prop": "text",
                           "section": section_id, "origin": "*"}
            response_text = requests.get(url, params=params_text, headers=headers, timeout=15)
            response_text.raise_for_status()
            html_content = response_text.json().get("parse", {}).get("text", {}).get("*", "")
            if html_content:
                html_content = clean_html(html_content, current_site_lang=site_lang_code, word=word)
                definition = f'<div>{html_content}</div>'
                CACHE[cache_key] = (definition, time.time())
                return definition
            else:
                jump_anchor = entry_name.replace(" ", "_")
                return f"No content found for {entry_name}. See: https://{site_lang_code}.wiktionary.org/wiki/{word}#{jump_anchor}"
        else:
            jump_anchor = entry_name.replace(" ", "_")
            return f"No section found for {entry_name}. See: https://{site_lang_code}.wiktionary.org/wiki/{word}#{jump_anchor}"

    except requests.RequestException as e:
        return f"Error retrieving definition: {e}"
    except ValueError:
        return "Error decoding response from Wiktionary."


def fetch_wiktionary_entry_from_link(word, site_lang_code="en", entry_lang_code="en"):
    if not word:
        return ""

    url = WIKTIONARY_API.format(site_lang=site_lang_code)
    headers = {"User-Agent": "WiktionaryLookup/1.0"}

    try:
        params_sections = {"action": "parse", "page": word, "format": "json", "prop": "sections", "origin": "*"}
        response = requests.get(url, params=params_sections, headers=headers, timeout=15)
        response.raise_for_status()
        sections = response.json().get("parse", {}).get("sections", [])
        CACHE[(word.lower(), site_lang_code, "sections")] = (sections, time.time())

        section_id = find_section(sections, site_lang_code, entry_lang_code)
        entry_name = next((name for name, code in DISPLAYED_LANGS_EXPANDED.get(site_lang_code, {}).items()
                           if code == entry_lang_code), None) or entry_lang_code

        if section_id:
            params_text = {"action": "parse", "page": word, "format": "json", "prop": "text",
                           "section": section_id, "origin": "*"}
            response_text = requests.get(url, params=params_text, headers=headers, timeout=15)
            response_text.raise_for_status()
            html_content = response_text.json().get("parse", {}).get("text", {}).get("*", "")
            if html_content:
                html_content = clean_html(html_content, current_site_lang=site_lang_code, word=word)
                definition = f'<div>{html_content}</div>'
                CACHE[(word.lower(), site_lang_code, entry_lang_code)] = (definition, time.time())
                return definition
            else:
                jump_anchor = entry_name.replace(" ", "_")
                return f"No content found for {entry_name}. See: https://{site_lang_code}.wiktionary.org/wiki/{word}#{jump_anchor}"
        else:
            jump_anchor = entry_name.replace(" ", "_")
            return f"No section found for {entry_name}. See: https://{site_lang_code}.wiktionary.org/wiki/{word}#{jump_anchor}"

    except requests.RequestException as e:
        return f"Error retrieving definition: {e}"
    except ValueError:
        return "Error decoding response from Wiktionary."


# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    word = request.args.get("word", "").strip().lower()
    site_lang_code = request.args.get("site_language", "en")
    entry_lang_code = request.args.get("entry_language", "en")

    definition = fetch_wiktionary_entry(word, site_lang_code, entry_lang_code) if word else ""

    return render_template(
        "index.html",
        word=word,
        definition=definition,
        displayed_languages=DISPLAYED_LANGUAGES,
        all_languages=LANGUAGES,
        site_lang_code=site_lang_code,
        entry_lang_code=entry_lang_code
    )


@app.route("/link", methods=["GET"])
def link_redirect():
    word = request.args.get("word", "").strip().lower()
    site_lang_code = request.args.get("site_language", "en")
    entry_lang_code = request.args.get("entry_language", site_lang_code)

    definition = fetch_wiktionary_entry_from_link(word, site_lang_code, entry_lang_code) if word else ""

    return render_template(
        "index.html",
        word=word,
        definition=definition,
        displayed_languages=DISPLAYED_LANGUAGES,
        all_languages=LANGUAGES,
        site_lang_code=site_lang_code,
        entry_lang_code=entry_lang_code
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
