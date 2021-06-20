from typing import List
import logging

import requests
from pyppeteer import launch
from pyppeteer.browser import Browser

logger = logging.getLogger(__name__)


async def get_embed_html(link: str, browser: Browser):
    """Obtain HTML code for embedding TikTok videos from short URLs

    Args:
        link (`str`): Links to TikTok, including "vm.tiktok.com"
        browser (`pyppeteer.Browser`): Browser object to travel to URL

    Returns:
        `str`: Embed code from TikTok API
    """
    page = await browser.newPage()

    logger.info("Feeding URL %s", link)
    init_response = await page.goto(link)
    videourl = init_response.request.url
    logger.info("Obtained long URL %s", videourl)

    # Sending request
    r = requests.get("https://www.tiktok.com/oembed?url=" + videourl)
    logger.info("Obtained response from TikTok API: %i", r.status_code)

    return r.json()["html"]


async def embed(links: List[str]):
    """Launch browser and get embeds for a list of TikTok links

    Args:
        links (List[str]): list of links

    Returns:
        List[str]: List of HTML embed codes
    """
    browser = await launch()
    logger.debug("Launching browser")

    html_elements = []
    # Feed each link to API
    for link in links:
        element = await get_embed_html(link, browser)
        html_elements.append(element)

    return html_elements
