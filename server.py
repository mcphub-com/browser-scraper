import aiohttp
from typing import Literal, Annotated
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from typing import Union, Literal, List

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")

__rapidapi_url__ = 'https://rapidapi.com/particle-media-particle-media-default/api/browser-scraper/'

mcp = FastMCP('browser_scraper')


@mcp.tool()
async def browser_scrape(
        url: Annotated[str, Field(description="the url you need to scrape")],
        timeout: Annotated[Union[int, None], Field(
                description="The desired number of seconds (default 15) to give webpages to respond and load. Note that the total request time may exceed this due to network and processing latency.")] = 15,
                 ):
    """
    scrape the url by browser use tool.
    """
    request_url = "https://browser-scraper.p.rapidapi.com/scrape"
    headers = {'x-rapidapi-host': 'browser-scraper.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'url': url,
        'timeout': timeout,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(request_url, json=payload, timeout=timeout + 5, raise_for_status=True,
                                    headers=headers) as r:
                response = await r.json()
                if isinstance(response, list):
                    return {"result": response}
                return response
    except Exception as e:
        logging.warning("", exc_info=True)
        return {"status": "failed", "reason": str(e)}


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
