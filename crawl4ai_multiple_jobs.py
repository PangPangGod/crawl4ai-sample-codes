from crawl4ai import Crawl4aiDockerClient, CrawlerRunConfig, BrowserConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.models import CrawlResult

from pydantic import BaseModel, ValidationError
from typing import Iterable, Union, Iterable, Type, List, Dict, Any
import json
import os

## 세부 Crawl할 때 파일이랑 같이 넣는거 Test


def parse_json_to_pydantic(
    cls: Type[BaseModel], json_data: Dict[str, Any]
) -> BaseModel:
    """
    Helper Function: Parses a JSON dictionary into a Pydantic model instance.
    """
    try:
        return cls(**json_data)
    except ValidationError as e:
        print(f"[Error] Validation error: {e}")
        return None


class ParsedInfo(BaseModel):
    label: str
    content: str


def process_crawl_result(crawl_result: Union[CrawlResult, Iterable[CrawlResult]]):
    if isinstance(crawl_result, CrawlResult):
        json_content: List[Dict[str, Any]] = json.loads(crawl_result.extracted_content)
        for content in json_content:
            pydantic_model = parse_json_to_pydantic(ParsedInfo, content)
            if pydantic_model:
                print(f"[Success] Parsed Pydantic model: {pydantic_model}")
            else:
                print("[Error] Failed to parse JSON content.")
        return

    if any(not isinstance(r, CrawlResult) for r in crawl_result):
        raise ValueError(
            "There are elements in List[CrawlResult] that are not of type CrawlResult."
        )

    for index, r in enumerate(crawl_result):
        json_content: List[Dict[str, Any]] = json.loads(r.extracted_content)

        for content in json_content:
            pydantic_model = parse_json_to_pydantic(ParsedInfo, content)
            if pydantic_model:
                print(
                    f"[Success] Result {index}: Parsed Pydantic model: {pydantic_model}"
                )
            else:
                print(f"[Error] Result {index}: Failed to parse JSON content.")
    return


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
        process_crawl_result(result)


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
