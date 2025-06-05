# Crawl4AI Sample Code

## Before Start
- This code uses Crawl4AI Docker Image. check [Crawl4AI Dockerhub](https://hub.docker.com/r/unclecode/crawl4ai)
- Currently using latest image -> 0.6.0-r2 

## Content
- `crawl4ai_css_extraction_strategy.py`
    - Example Using `JsonCssExtractionStrategy` ..
- `crawl4ai_multiturn_with_js.py`
    - Example Multiturn Crawl + Using javascript code inside crawling process
- `crawl4ai_download_files.py`
    - Mount Host Directory + Download files
- `crawl4ai_llm_extraction_strategy.py`
    - LLM Strategy Example with Google Gemini-1.5-flash
    - LLMStrategy Basically follow LiteLLM Format.
- `crawl4ai_multiple_jobs.py`
    - Multiple jobs(css_extraction / download_files) integrated in single loop