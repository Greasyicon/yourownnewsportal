# web_scraper.py

import time
import requests
import json
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent

API_KEY = '85208bdd07b540748605baf71abc6c1b' #'8617266eaa794b5aaf3af87defbbd1ff'#
use_premium_version = False
REQUEST_LIMIT = 500  # Limit of requests for the free News API plan
REQUEST_COUNT = 0  # Current number of requests
ua = UserAgent()

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to run.")
        return result

    return wrapper

def save_data(all_articles):
    with open("news_dataset.json", "w") as file:
        json.dump(all_articles, file)
    print("Dataset saved to news_dataset.json")


# Fetch the list of news sources available from the News API
def fetch_sources():
    global REQUEST_COUNT
    try:
        url = f'https://newsapi.org/v2/sources?apiKey={API_KEY}'
        # # Use fake user agent in the headers
        # headers = {'User-Agent': ua.random}
        # response = requests.get(url, headers=headers)
        response = requests.get(url)
        REQUEST_COUNT += 1
        data = response.json()
        return [source['id'] for source in data['sources']]
    except Exception as e:
        print(f"Error while fetching sources: {e}")
        return []


# Fetch top headlines from a specific source
def fetch_articles(source):
    global REQUEST_COUNT
    try:
        url = f'https://newsapi.org/v2/top-headlines?sources={source}&apiKey={API_KEY}'
        # # Use fake user agent in the headers
        # headers = {'User-Agent': ua.random}
        # response = requests.get(url, headers=headers)
        response = requests.get(url)
        REQUEST_COUNT += 1
        data = response.json()
        return data['articles']
    except Exception as e:
        print(f"Error while fetching articles for {source}: {e}")
        return []

# Fetch segment based news based from a specific source
def fetch_articles_everything(source, query):
    global REQUEST_COUNT
    try:
        url = f'https://newsapi.org/v2/everything?sources={source}&q={query}&apiKey={API_KEY}'
        # # Use fake user agent in the headers
        # headers = {'User-Agent': ua.random}
        # response = requests.get(url, headers=headers)
        response = requests.get(url)
        REQUEST_COUNT += 1
        data = response.json()
        return data['articles']
    except Exception as e:
        print(f"Error while fetching articles for {source}: {e}")
        return []


# Scrape the full content of an article using the URL
def scrape_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error while scraping: {url} - {e}")
        return ""


# Wrapper function for error handling
def process_source(source_name):
    if REQUEST_COUNT >= REQUEST_LIMIT:
        return []

    articles_data = fetch_articles(source_name)
    if use_premium_version:
        query_ = 'technology'
        articles_data = fetch_articles_everything(source_name, query_)
    articles = []

    for article_data in articles_data:
        title = article_data['title']
        url = article_data['url']
        text = scrape_article_content(url)
        article = {"source": source_name, "title": title, "text": text}
        articles.append(article)

    return articles

@timer
def main():
    news_sources = fetch_sources()
    # sources = [
    #     'bbc-news', 'cnn', 'reuters', 'the-hill', 'the-new-york-times',
    #     'the-washington-post', 'the-wall-street-journal', 'usa-today',
    #     'fox-news', 'msnbc'
    # ]
    all_articles = []

    # Process multiple sources concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_source, source_name): source_name for source_name in news_sources}

        for future in as_completed(futures):
            source_name = futures[future]
            try:
                articles = future.result()
                all_articles.extend(articles)
                print(f"Scraped {len(articles)} articles from {source_name}")
                # Sleep for a short duration to avoid being blocked
                time.sleep(5)

                if REQUEST_COUNT >= REQUEST_LIMIT:
                    print("Reached the request limit. Stopping the script.")
                    break

                # Save data after every 100 requests
                if REQUEST_COUNT % 100 == 0:
                    save_data(all_articles)

            except Exception as e:
                print(f"Error while processing {source_name}: {e}")

    save_data(all_articles)


if __name__ == "__main__":
    main()
#
# import requests
# import json
# from newspaper import Article
# from concurrent.futures import ThreadPoolExecutor, as_completed
#
# API_KEY = '8617266eaa794b5aaf3af87defbbd1ff'#'85208bdd07b540748605baf71abc6c1b'
#
# use_premium_version = False
#
# REQUEST_LIMIT = 500  # Limit of requests for the free News API plan
# REQUEST_COUNT = 0  # Current number of requests
#
# # Wrapper around handling requests
# def request_handler(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f"Error while requesting URL: {e}")
#             return []
#     return wrapper
#
# # Fetch the list of news sources available from the News API
# @request_handler
# def fetch_sources():
#     global REQUEST_COUNT
#     url = f'https://newsapi.org/v2/sources?apiKey={API_KEY}'
#     response = requests.get(url)
#     REQUEST_COUNT += 1
#     data = response.json()
#     return [source['id'] for source in data['sources']]
#
# # Fetch top headlines from a specific source
# @request_handler
# def fetch_articles(source):
#     global REQUEST_COUNT
#     url = f'https://newsapi.org/v2/top-headlines?sources={source}&apiKey={API_KEY}'
#     response = requests.get(url)
#     REQUEST_COUNT += 1
#     data = response.json()
#     return data['articles']
#
#
# # Fetch articles using the 'everything' endpoint with a specific query
# @request_handler
# def fetch_articles_everything(source, query):
#     global REQUEST_COUNT
#     url = f'https://newsapi.org/v2/everything?sources={source}&q={query}&apiKey={API_KEY}'
#     response = requests.get(url)
#     REQUEST_COUNT += 1
#     data = response.json()
#     return data['articles']
#
# # Scrape the full content of an article using the URL
# def scrape_article_content(url):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         return article.text
#     except Exception as e:
#         print(f"Error while scraping: {url} - {e}")
#         return ""
#
# # Wrapper function for error handling
# def process_source(source_name):
#     articles_data = fetch_articles(source_name)
#     if use_premium_version:
#         query_ = 'technology'
#         articles_data = fetch_articles_everything(source_name, query_)
#     articles = []
#
#     for article_data in articles_data:
#         title = article_data['title']
#         url = article_data['url']
#         text = scrape_article_content(url)
#         article = {"source": source_name, "title": title, "text": text}
#         articles.append(article)
#
#     return articles
#
# def main():
#     news_sources = fetch_sources()
#     all_articles = []
#
#     # Process multiple sources concurrently using ThreadPoolExecutor
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         futures = {executor.submit(process_source, source_name): source_name for source_name in news_sources}
#
#         for future in as_completed(futures):
#             source_name = futures[future]
#             try:
#                 articles = future.result()
#                 all_articles.extend(articles)
#                 print(f"Scraped {len(articles)} articles from {source_name}")
#             except Exception as e:
#                 print(f"Error while processing {source_name}: {e}")
#
#     with open("news_dataset.json", "w") as file:
#         json.dump(all_articles, file)
#     print("Dataset saved to news_dataset.json")
#
# if __name__ == "__main__":
#     main()


# # web_scraper.py
#
# import requests
# import json
# from bs4 import BeautifulSoup
# from newspaper import Article
#
# def request_handler(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f"Error while requesting URL: {e}")
#             return []
#     return wrapper
#
# def get_source_config(source_name):
#     configs = {
#         "bbc": {
#             "url": "https://www.bbc.com/news",
#             "article_elements_selector": "a.gs-c-promo-heading",
#             "content_selector": "div.css-83cqas-RichTextContainer",
#             "url_prefix": "https://www.bbc.com",
#         },
#         "cnn": {
#             "url": "https://edition.cnn.com/world",
#             "article_elements_selector": "h3.card-title",
#             "content_selector": "div.zn-body__paragraph",
#             "url_prefix": "https://edition.cnn.com",
#         },
#         "aljazeera": {
#             "url": "https://www.aljazeera.com/news/",
#             "article_elements_selector": "h3.gc__title",
#             "content_selector": "div.wysiwyg",
#             "url_prefix": "https://www.aljazeera.com",
#         },
#         "reuters": {
#             "url": "https://www.reuters.com/world/",
#             "article_elements_selector": "h3.story-title",
#             "content_selector": "div.ArticleBodyWrapper",
#             "url_prefix": "https://www.reuters.com",
#         },
#         "nytimes": {
#             "url": "https://www.nytimes.com/section/world",
#             "article_elements_selector": "div.css-1l4spti",
#             "content_selector": "section.meteredContent",
#             "url_prefix": "https://www.nytimes.com",
#         },
#     }
#     return configs.get(source_name.lower(), {})
#
# # Function to scrape news headlines and content from a given source
# @request_handler
# def scrape_news(source_name):
#     config = get_source_config(source_name)
#     if not config:
#         print(f"Invalid news source: {source_name}")
#         return []
#
#     url = config["url"]
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#
#     article_elements = soup.select(config["article_elements_selector"])
#     articles = []
#
#     for article_element in article_elements:
#         title = article_element.get_text(strip=True)
#         article_url = article_element["href"]
#         if not article_url.startswith("http"):
#             article_url = config["url_prefix"] + article_url
#
#         if scraping_model == 'newspaper3k':
#             content_response = requests.get(article_url)
#             content_soup = BeautifulSoup(content_response.text, "html.parser")
#             content = content_soup.select_one(config["content_selector"])
#             if content:
#                 text = content.get_text(strip=True)
#                 articles.append({"source": source_name, "title": title, "text": text})
#
#         if scraping_model == 'newspaper3k':
#             # Scrape the article content using the newspaper3k library
#             article = Article(article_url)
#             article.download()
#             article.parse()
#             text = article.text
#
#             articles.append({"source": source_name, "title": title, "text": text})
#
#         print(".", end="", flush=True)
#
#     return articles
#
# # Function to save the dataset to a JSON file
# def save_dataset(dataset, filename):
#     with open(filename, "w") as f:
#         json.dump(dataset, f)
#
# # Main function to execute the scraping and save the dataset
# def main():
#     news_sources = [
#         "BBC",
#         "CNN",
#         "Al Jazeera",
#         "Reuters",
#         "NYTimes",
#     ]
#
#     all_articles = []
#
#     for source_name in news_sources:
#         print(f"Scraping headlines and content from {source_name}:")
#         articles = scrape_news(source_name)
#         all_articles.extend(articles)
#         print("\n")
#         for idx, article in enumerate(articles, start=1):
#             print(f"{idx}. {article['title']} ({article['source']})")
#             print(f"Content: {article['text'][:100]}... (truncated)\n")
#         print("\n")
#
#     save_dataset(all_articles, "news_dataset.json")
#     print("Dataset saved to news_dataset.json")
#
# if __name__ == "__main__":
#     scraping_model = 'newspaper3k' #'beautifulsoup'
#     main()

# web_scraper.py
#
# import requests
# import json
# from newspaper import Article
#
# API_KEY = '85208bdd07b540748605baf71abc6c1b'
#
# use_premium_version = False
#
# REQUEST_LIMIT = 500  # Limit of requests for the free News API plan
# REQUEST_COUNT = 0  # Current number of requests
#
# # Wrapper around handling requests
# def request_handler(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f"Error while requesting URL: {e}")
#             return []
#     return wrapper
#
# # Fetch the list of news sources available from the News API
# @request_handler
# def fetch_sources():
#     global REQUEST_COUNT
#     url = f'https://newsapi.org/v2/sources?apiKey={API_KEY}'
#     response = requests.get(url)
#     REQUEST_COUNT += 1
#     data = response.json()
#     return [source['id'] for source in data['sources']]
#
# # Fetch top headlines from a specific source
# @request_handler
# def fetch_articles(source):
#     global REQUEST_COUNT
#     url = f'https://newsapi.org/v2/top-headlines?sources={source}&apiKey={API_KEY}'
#     response = requests.get(url)
#     REQUEST_COUNT += 1
#     data = response.json()
#     return data['articles']
#
# # Fetch articles using the 'everything' endpoint with a specific query
# @request_handler
# def fetch_articles_everything(source, query):
#     global REQUEST_COUNT
#     url = f'https://newsapi.org/v2/everything?sources={source}&q={query}&apiKey={API_KEY}'
#     response = requests.get(url)
#     REQUEST_COUNT += 1
#     data = response.json()
#     return data['articles']
#
# # Scrape the full content of an article using the URL
# @request_handler
# def scrape_article_content(url):
#     article = Article(url)
#     article.download()
#     article.parse()
#     return article.text
#
# def main():
#     news_sources = fetch_sources()
#
#     all_articles = []
#
#     for source_name in news_sources:
#         if REQUEST_COUNT >= REQUEST_LIMIT:
#             print("Reached the request limit. Stopping the script.")
#             break
#
#         if REQUEST_COUNT % 10 == 0:
#             with open("news_dataset.json", "w") as file:
#                 json.dump(all_articles, file)
#             print("########################  Interim Dataset saved to news_dataset.json")
#
#         print(f"Scraping headlines and content from {source_name}:")
#
#         # Choose between fetch_articles (top-headlines) and fetch_articles_everything
#         articles_data = fetch_articles(source_name)
#         if use_premium_version:
#             articles_data = fetch_articles_everything(source_name, "technology")
#
#         for article_data in articles_data:
#             title = article_data['title']
#             url = article_data['url']
#             text = scrape_article_content(url)
#             article = {"source": source_name, "title": title, "text": text}
#             all_articles.append(article)
#             print(f"{title} ({source_name})")
#             print(f"Content: {text[:100]}... (truncated)\n")
#         print("\n")
#
#     with open("news_dataset.json", "w") as file:
#         json.dump(all_articles, file)
#     print("Dataset saved to news_dataset.json")
#
# if __name__ == "__main__":
#     main()
