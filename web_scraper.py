# web_scraper.py

import time
import requests
import json
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent

API_KEY = 'ca03000b406746cab0fae37ca959aebc'#'''8617266eaa794b5aaf3af87defbbd1ff' #'85208bdd07b540748605baf71abc6c1b'#
use_premium_version = False
REQUEST_LIMIT = 500  # Limit of requests for the free News API plan
REQUEST_COUNT = 0  # Current number of requests
ua = UserAgent()
multiprocessing = True
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
    base_url = 'https://newsapi.org/v2/sources?apiKey='
    try:
        url = f'{base_url}{API_KEY}'
        # # Use fake user agent in the headers
        # headers = {'User-Agent': ua.random}
        # response = requests.get(url, headers=headers)
        response = requests.get(url)
        if response.status_code == 429:
            print("Too Many Requests..., Try Another Api Key")
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
        return None


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
        if text is not None:
            article = {"source": source_name, "title": title, "text": text}
            articles.append(article)

    return articles

@timer
def scrape_articles(start=0, end=2):
    news_sources = fetch_sources()[start:end]
    print("News Sources Fetched.")
    # sources = [
    #     'bbc-news', 'cnn', 'reuters', 'the-hill', 'the-new-york-times',
    #     'the-washington-post', 'the-wall-street-journal', 'usa-today',
    #     'fox-news', 'msnbc'
    # ]
    all_articles = []
    if multiprocessing:
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
    else:
        # Process each source sequentially
        for source_name in news_sources:
            articles = scrape_data_from_source(source_name)
            if articles:
                all_articles.extend(articles)
            if REQUEST_COUNT >= REQUEST_LIMIT:
                print("Reached the request limit. Stopping the script.")
                break
            # Save data after every 100 requests
            if REQUEST_COUNT % 100 == 0:
                save_data(all_articles)

    save_data(all_articles)

def scrape_data_from_source(news_source):
    # Process each source
    try:
        articles = process_source(news_source)
        print(f"Scraped {len(articles)} articles from {news_source}")
        # Sleep for a short duration to avoid being blocked
        time.sleep(5)
    except Exception as e:
        print(f"Error while processing {news_source}: {e}")

def fetch_unscraped_sources(scraped_sources):
    all_sources = fetch_sources()
    unscraped_sources = [source for source in all_sources if source not in scraped_sources]
    return unscraped_sources



if __name__ == "__main__":
    scrape_articles()