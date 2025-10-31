import requests
from bs4 import BeautifulSoup

def fetch_wikipedia_intro(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return "Could not find article content."

        paragraphs = content_div.find_all("p", recursive=False)
        for p in paragraphs:
            intro_text = p.get_text(strip=True)
            if intro_text:
                return intro_text

        return "No intro paragraph found."
    except Exception as e:
        return f"Error fetching Wikipedia intro: {str(e)}"

wiki_intro_tool_schema = {
    "name": "wiki_intro_extractor",
    "description": (
        "Extracts the introductory (lead) paragraph from the given Wikipedia article URL. "
        "Use this tool whenever the user provides a Wikipedia page link or requests a brief summary, "
        "overview, or introduction from a specific Wikipedia topic. The tool fetches and returns the original "
        "introductory text exactly as it appears on Wikipedia. It does not summarize, rephrase, or interpret—"
        "it only retrieves the first substantive paragraph from the article's main content area."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "Full Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Python_(programming_language))"
            }
        },
        "required": ["url"]
    }
}
