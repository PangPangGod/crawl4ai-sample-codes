from crawl4ai import Crawl4aiDockerClient
from crawl4ai import CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

## Warning: You have to use your own URL / extraction strategy. this is just an example.

auth_email = "test@example.com"

extraction_strategy = JsonCssExtractionStrategy(
    schema={
        "name": "links_schema",
        "baseSelector": "div.table_basics_com_cont_area table.table_basics_area tbody tr",
        "fields": [
            {
                "name": "no",
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
                "name": "href",
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
                "selector": "td.nth-child(6)",
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


async def fetch_info_from_url(client: Crawl4aiDockerClient, url: str):
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
    print(response.extracted_content)


async def main(host: str, url: str, start: int, end: int, verbose: bool = True):
    async with Crawl4aiDockerClient(
        base_url=host,
        verbose=verbose,
        timeout=60,
    ) as client:
        # If jwt is enabled, authenticate first
        await client.authenticate(auth_email)

        for page in range(start, end + 1):
            page_url = f"{url}&page={page}"
            await fetch_info_from_url(client, page_url)


if __name__ == "__main__":
    import asyncio

    host = "http://localhost:11235"
    url = "<YOUR_URL_HERE>"

    START = 1
    END = 2

    asyncio.run(main(host, url, START, END))
