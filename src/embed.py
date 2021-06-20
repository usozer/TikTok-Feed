from typing import List

import requests
from pyppeteer import launch
from pyppeteer.browser import Browser


async def get_embed_html(link: str, browser: Browser):

    page = await browser.newPage()
    init_response = await page.goto(link)
    videourl = init_response.request.url

    r = requests.get("https://www.tiktok.com/oembed?url=" + videourl)

    return r.json()["html"]


async def embed(links: List[str]):
    browser = await launch()

    html_elements = []
    for link in links:
        element = await get_embed_html(link, browser)
        html_elements.append(element)

    return html_elements
