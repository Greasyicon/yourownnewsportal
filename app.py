from flask import Flask, render_template, request
from flask_caching import Cache
import json
from web_scraper import scrape_articles, fetch_sources
from data_preprocessing import data_preprocessing
import traceback
# from redis import Redis
# from rq import Queue
# import os

# # Initialize the Redis connection
# redis_conn = Redis.from_url(os.environ.get("REDIS_URL", "redis://"))
#
# # Initialize the RQ queue
# queue = Queue(connection=redis_conn)

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
@app.route('/')
@cache.cached(timeout=3600)  # Cache for 1 hour
def index():
    with open('cleaned_news_dataset.json', 'r') as file:
        cleaned_articles = json.load(file)

    articles_by_source = {}
    for article in cleaned_articles:
        source = article['source']
        if source not in articles_by_source:
            articles_by_source[source] = []
        articles_by_source[source].append(article)

    return render_template('index.html', articles_by_source=articles_by_source)

news_sources = fetch_sources()

@app.route('/update_content', methods=['POST'])
def update_content():
    # cache.delete('view//')
    print("Scraping Articles")
    try:
        # Enqueue the scraping task
        # queue.enqueue(scrape_articles)
        scrape_articles()
        # return #"Scraping task enqueued", 202
    except Exception as e:
        print(traceback.format_exc())
        return str(e), 500
    print("Cleaning Articles")
    data_preprocessing()
    with open('cleaned_news_dataset.json', 'r') as file:
        cleaned_articles = json.load(file)

    articles_by_source = {}
    for article in cleaned_articles:
        source = article['source']
        if source not in articles_by_source:
            articles_by_source[source] = []
        articles_by_source[source].append(article)
    # cache.set('view//', articles_by_source, timeout=3600)  # Cache for 1 hour
    return render_template('index.html', articles_by_source=articles_by_source)

if __name__ == '__main__':
    app.run(debug=True)
    # # Run the app using the gunicorn web server
    # from gunicorn.app.base import BaseApplication
    #
    # class StandaloneApplication(BaseApplication):
    #     def __init__(self, app, options=None):
    #         self.options = options or {}
    #         self.application = app
    #         super().__init__()
    #
    #     def load_config(self):
    #         config = {key: value for key, value in self.options.items()
    #                   if key in self.cfg.settings and value is not None}
    #         for key, value in config.items():
    #             self.cfg.set(key.lower(), value)
    #
    #     def load(self):
    #         return self.application
    #
    # options = {
    #     'bind': '0.0.0.0:5000',
    #     'workers': 4,
    #     'timeout': 120
    # }
    # StandaloneApplication(app, options).run()
