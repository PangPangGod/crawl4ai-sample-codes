from crawl4ai import Crawl4aiDockerClient, CrawlerRunConfig, LLMConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import os
import json
from typing import Iterable
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: str


async def main(urls: Iterable[str] = None, instruction: str = None):
    llm_strat = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="gemini/gemini-2.0-flash", api_token=os.getenv("GOOGLE_API_KEY")
        ),
        schema=Product.model_json_schema(),
        extraction_type="schema",
        instruction=instruction,
        overlap_rate=0.1,
        apply_chunking=True,
        input_format="markdown",
        verbose=True,
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strat,
        cache_mode=CacheMode.BYPASS,
    )

    async with Crawl4aiDockerClient(
        base_url="http://localhost:11235",
        verbose=True,
        timeout=600,
    ) as client:
        # If jwt is enabled, authenticate first
        auth_email = "docker@email.com"
        await client.authenticate(auth_email)

        response = await client.crawl(
            urls=urls,
            crawler_config=crawl_config,
        )

        if response.success:
            data = json.loads(response.extracted_content)
            print("Extracted Data:", data)


if __name__ == "__main__":
    import asyncio

    urls = ["https://www.amazon.com/s?k=doge"]
    instruction = "get merchaindise name and price from the page"
    asyncio.run(main(urls=urls, instruction=instruction))
