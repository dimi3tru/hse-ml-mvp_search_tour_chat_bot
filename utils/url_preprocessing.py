from typing import Dict, Any, List, Tuple
import requests
from urllib.parse import urlencode, urljoin
from bs4 import BeautifulSoup

def fetch_urls(url: str, max_urls: int = 5, timeout: int = 15) -> Tuple[List[str], bool]:
    """
    Fetches a list of relevant tour urls from the page before recommendations appear.

    Args:
        url (str): The URL of the tours page.
        max_urls (int, optional): Maximum number of urls to return. Default is 5.
        timeout (int, optional): HTTP request timeout in seconds. Default is 15.

    Returns:
        Tuple[List[str], bool]:
            - list[str]: A list of up to max_urls absolute URLs to tour details.
            - bool: incomplete flag:
                * True — fewer than max_urls relevant tours were found (or error occurred).
                * False — at least max_urls relevant tours were found.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return [], True

    soup = BeautifulSoup(resp.text, 'html.parser')

    # If the page explicitly says "no results", return an empty list
    if soup.find('div', class_='tours-not-found'):
        return [], True

    urls: List[str] = []

    # Helper to match only tour previews and the "also recommended" marker
    def _is_preview_or_marker(tag):
        if tag.name != 'div':
            return False
        cls = tag.get('class', [])
        return 'tour-preview__content' in cls or 'tours-group-title' in cls

    for block in soup.find_all(_is_preview_or_marker):
        # Stop if we reach the recommendations section
        if 'tours-group-title' in block.get('class', []):
            break

        # Otherwise, extract the first url from the preview block
        a_tag = block.find('a', href=True)
        if not a_tag:
            continue
        urls.append(urljoin(url, a_tag['href']))
        if len(urls) >= max_urls:
            break

    incomplete = len(urls) < max_urls
    return urls, incomplete



def build_filtered_url(main_url: str, filters: Dict[str, Any]) -> str:
    """Build url with filter parameters, supporting multiple values per key, and always including /tury?plainSearch=1"""
    if not filters:
        return f"{main_url}/tury?plainSearch=1"

    expanded_params = []
    for key, value in filters.items():
        if isinstance(value, list):
            for v in value:
                expanded_params.append((key, v))
        else:
            expanded_params.append((key, value))

    query_string = urlencode(expanded_params, doseq=True)
    return f"{main_url}/tury?plainSearch=1&{query_string}"
