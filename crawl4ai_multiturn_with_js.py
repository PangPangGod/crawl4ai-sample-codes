import asyncio
from crawl4ai.docker_client import Crawl4aiDockerClient
from crawl4ai import CrawlerRunConfig


async def main():
    async with Crawl4aiDockerClient(
        base_url="http://localhost:11235",
        verbose=True,
        timeout=60,
    ) as client:
        # If jwt is enabled, authenticate first
        await client.authenticate("test@example.com")

        config = CrawlerRunConfig(
            wait_for="js:() => document.querySelectorAll('tr.athing.submission').length >= 30"
        )

        result = await client.crawl(
            urls=["https://news.ycombinator.com"],
            crawler_config=config,
        )

        print("Initial items loaded.")

        load_more_js = [
            "window.scrollTo(0, document.body.scrollHeight);",
            "document.querySelector('a.morelink')?.click();",
        ]

        next_page_conf = CrawlerRunConfig(
            js_code=load_more_js,  # Mark that we do not re-navigate, but run JS in the same session:
            session_id="hn_session",
            wait_for="js:() => document.querySelectorAll('tr.athing.submission').length > 30;",
        )

        result2 = await client.crawl(
            urls=["https://news.ycombinator.com"],  # same URL but continuing session
            crawler_config=next_page_conf,
        )
        total_items = result2.cleaned_html
        print("Items after load-more:", total_items)


if __name__ == "__main__":
    asyncio.run(main())
