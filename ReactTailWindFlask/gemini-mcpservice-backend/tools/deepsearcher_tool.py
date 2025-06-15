import logging
import os, sys
from dotenv import load_dotenv
from deepsearcher.offline_loading import load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config


# Suppress unnecessary logging from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)

# Load .env from project root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

# Set API keys (ensure these are set securely in real applications)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY

def get_deepsearcher(search_info: str):
    # # Step 1: Initialize configuration
    # config = Configuration()

    # # Set up Vector Database (Milvus) and Web Crawler (Crawl4AI)
    # config.set_provider_config("vector_db", "Milvus", {})
    # # config.set_provider_config('llm', 'Gemini', { 'model': 'gemini-2.0-flash' })
    # config.set_provider_config("web_crawler", "Crawl4AICrawler", {"browser_config": {"headless": True, "verbose": True}})


    # # Apply the configuration
    # init_config(config)

    # # Step 2: Load data from a website into Milvus
    # website_url = ["https://media.aws.singtel.com/info-singtel/sr2024/Singtel-Group-Sustainability-Report-2024.pdf"]  # Replace with your target website, can be a list of URLs
    # collection_name = "Singtel_PDF" # No Spacing Allowed
    # collection_description = "Singtel Sustainability Efforts"

    # # crawl a single webpage
    # load_from_website(urls=website_url, collection_name=collection_name, collection_description=collection_description)
    # # only applicable if using Firecrawl: deepsearcher can crawl multiple webpages, by setting max_depth, limit, allow_backward_links
    # # load_from_website(urls=website_url, max_depth=2, limit=20, allow_backward_links=True, collection_name=collection_name, collection_description=collection_description)

    # # Step 3: Query the loaded data
    # result = query(search_info)
    

    config = Configuration()

    # Set providers with API keys
    config.set_provider_config("vector_db", "Milvus", {})
    config.set_provider_config("llm", "OpenAI", {
        "model": "o1-mini",
     
    })
    config.set_provider_config("embedding", "OpenAIEmbedding", {
        "model": "text-embedding-ada-002",
        
    })
    config.set_provider_config("web_crawler", "Crawl4AICrawler", {"browser_config": {"headless": True, "verbose": True}})
    init_config(config)

    # # Collection configuration
    # collection_name = "Singtel_PDF"
    # collection_description = "Singtel Sustainability Efforts 2024"

    # # Load into Milvus
    # load_from_website(
    #     urls=["https://media.aws.singtel.com/info-singtel/sr2024/Singtel-Group-Sustainability-Report-2024.pdf"],
    #     collection_name=collection_name,
    #     collection_description=collection_description
    # )

    # Query from Milvus
    result = query(search_info)


if __name__ == "__main__":
    get_deepsearcher(search_info = "What is Singtel Sustainability Efforts in 2024? Are you pulling chunks from milvus or just webcrawling?")