from crawl4ai import Crawl4aiDockerClient, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from typing import Iterable
import json
import re

from dataclasses import dataclass

## Warning: You have to use your own URL / extraction strategy. this is just an example.

extraction_strategy = JsonCssExtractionStrategy(
    schema={
        "name": "links_schema",
        "baseSelector": "div.table_basics_com_cont_area table.table_basics_area tbody tr",
        "fields": [
            {
                "name": "id",
                "selector": "td:nth-child(1)",
                "type": "text",
            },
            {
                "name": "under_org",
                "selector": "td:nth-child(2)",
                "type": "text",
            },
            {
                "name": "target",
                "selector": "td:nth-child(3)",
                "type": "text",
            },
            {
                "name": "title",
                "selector": "td.tit a",
                "type": "text",
            },
            {
                "name": "url",
                "selector": "td.tit a",
                "type": "attribute",
                "attribute": "onclick",
            },
            {
                "name": "due_date",
                "selector": "td:nth-child(5)",
                "type": "text",
            },
            {
                "name": "category",
                "selector": "td:nth-child(6)",
                "type": "text",
            },
            {
                "name": "org",
                "selector": "td:nth-child(7)",
                "type": "text",
            },
        ],
        "is_multiple": True,
    }
)


@dataclass
class LinkInfo:
    id: int
    under_org: str
    target: str
    title: str
    url: str
    due_date: str
    category: str
    org: str

    def __post_init__(self):
        if self.url:
            match = re.search(r"https?://[^\']+", self.url)
            if match:
                self.url = match.group(0)
        if self.id:
            try:
                self.id = int(self.id.replace(",", ""))
            except Exception:
                print(
                    "[Error] Error Occurred when formatting. Invalid ID format:",
                    self.id,
                    "Using 0 instead.",
                )
                self.id = 0

    def __str__(self):
        return (
            f"LinkInfo(\n"
            f"    id={self.id!r},\n"
            f"    under_org={self.under_org!r},\n"
            f"    target={self.target!r},\n"
            f"    title={self.title!r},\n"
            f"    url={self.url!r},\n"
            f"    due_date={self.due_date!r},\n"
            f"    category={self.category!r},\n"
            f"    org={self.org!r}\n"
            f")"
        )


def parse_json_content(json_content: dict):
    return LinkInfo(
        id=json_content.get("id", ""),
        under_org=json_content.get("under_org", ""),
        target=json_content.get("target", ""),
        title=json_content.get("title", ""),
        url=json_content.get("url", ""),
        due_date=json_content.get("due_date", ""),
        category=json_content.get("category", ""),
        org=json_content.get("org", ""),
    )


async def fetch_info_from_url(client: Crawl4aiDockerClient, url: str):
    # load
    wait_for = "css:div.table_basics_com_cont_area table.table_basics_area tbody tr"

    crawler_config = CrawlerRunConfig(
        wait_for=wait_for,
        # css_selector="td.tit",
        extraction_strategy=extraction_strategy,
    )
    response = await client.crawl(
        urls=[url],
        crawler_config=crawler_config,
    )

    # print(response.__dict__.keys())
    json_content: Iterable[dict] = json.loads(response.extracted_content)

    for content in json_content:
        parsed_content: LinkInfo = parse_json_content(content)
        print(parsed_content)


async def main(host: str, url: str, start: int, end: int, verbose: bool = True):
    async with Crawl4aiDockerClient(
        base_url=host,
        verbose=verbose,
        timeout=60,
    ) as client:
        # If jwt is enabled, authenticate first
        auth_email = "test@example.com"
        await client.authenticate(auth_email)

        for page in range(start, end + 1):
            page_url = f"{url}&page={page}"
            await fetch_info_from_url(client, page_url)


if __name__ == "__main__":
    import asyncio

    host = "http://localhost:11235"
    url = "<YOUR_URL_HERE>"

    # IF multiple pages are needed
    START = 1
    END = 2

    asyncio.run(main(host, url, START, END))
