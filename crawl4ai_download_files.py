from crawl4ai import Crawl4aiDockerClient, CrawlerRunConfig, BrowserConfig
from typing import Iterable
import os


async def main(host: str, downloads_path: str = None, urls: Iterable[str] = None):
    # If downloads_path is not specified in config, it will be set to the default path:
    # "downloads" directory inside the .crawl4ai folder in your home directory.
    os.makedirs(downloads_path, exist_ok=True)

    browser_config = BrowserConfig(
        accept_downloads=True,
        downloads_path=downloads_path,
    )

    js_code = [
        "document.querySelectorAll('a.icon_download').forEach(button => {button.click();});"
    ]

    crawler_config = CrawlerRunConfig(js_code=js_code, wait_until="domcontentloaded")

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

        if result.downloaded_files:
            print("Downloaded files:")
            for file_path in result.downloaded_files:
                print(f"- {file_path}")
                file_size = os.path.getsize(file_path)
                print(f"- File size: {file_size} bytes")
        else:
            print("No files downloaded.")


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
