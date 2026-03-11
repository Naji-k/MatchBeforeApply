import requests
from bs4 import BeautifulSoup


def scrape_url(url: str) -> dict:
    """Fetch and extract the main text content from a web page URL.

    Args:
        url: The URL of the job description page to scrape.

    Returns:
        A dict with keys:
          - content (str): extracted page text
          - status (str): "success" or "error"
          - error_message (str): error detail if status is "error", else ""
    """
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return {"content": text, "status": "success", "error_message": ""}
    except Exception as e:
        return {"content": "", "status": "error", "error_message": str(e)}
