from crawl4ai import Crawl4aiDockerClient, CrawlerRunConfig, BrowserConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.models import CrawlResult

from typing import Iterable
import os


async def main(host: str, downloads_path: str = None, urls: Iterable[str] = None):
    # If downloads_path is not specified in config, it will be set to the default path:
    # "downloads" directory inside the .crawl4ai folder in your home directory.
    os.makedirs(downloads_path, exist_ok=True)

    extraction_strategy = JsonCssExtractionStrategy(
        schema={
            "name": "detail_info",
            "baseSelector": "div.view_cont ul li",
            "is_multiple": True,
            "fields": [
                {
                    "name": "label",
                    "selector": "span.s_title",
                    "type": "text",
                },
                {
                    "name": "content",
                    "selector": "div.txt",
                    "type": "text",
                },
            ],
        }
    )

    browser_config = BrowserConfig(
        accept_downloads=True,
        downloads_path=downloads_path,
    )

    js_code = [
        "document.querySelectorAll('a.icon_download').forEach(button => {button.click();});"
    ]

    crawler_config = CrawlerRunConfig(
        js_code=js_code,
        wait_until="domcontentloaded",
        extraction_strategy=extraction_strategy,
    )

    async with Crawl4aiDockerClient(
        base_url=host,
        verbose=True,
        timeout=600,
    ) as client:
        # If jwt is enabled, authenticate first
        auth_email = "test@example.com"
        await client.authenticate(auth_email)

        result = await client.crawl(
            urls=urls,
            browser_config=browser_config,
            crawler_config=crawler_config,
        )

        # check type with CrawlResult
        if isinstance(result, CrawlResult):
            print(f"Result 0: {result.extracted_content}")
            return

        if any(not isinstance(r, CrawlResult) for r in result):
            raise ValueError(
                "There are elements in List[CrawlResult] that are not of type CrawlResult."
            )

        for index, r in enumerate(result):
            print(f"Result {index}: {r.extracted_content}")
        return


if __name__ == "__main__":
    ## Warning: You have to use your own URL / Download JS code. this is just an example.
    ## If you are using a Docker version, mount the download folder to the host machine.
    ## Assuming a Docker version Crawl4AI is used, the download folder within the container will be mounted to the local machine's folder.

    ## Warning: Using WSL in Windows
    ## docker run -d -p 11235:11235 --name crawl4ai --shm-size=3g -v "$(pwd)/downloads":/app/downloads unclecode/crawl4ai:latest

    import asyncio

    host = "http://localhost:11235"
    downloads_path = "downloads"
    urls = [
        "<YOUR_URL_HERE>",
    ]
    asyncio.run(main(host, downloads_path, urls))
