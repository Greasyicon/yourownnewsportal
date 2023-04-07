from flask import Flask, render_template, request
from flask_caching import Cache
import json
from web_scraper import fetch_sources
from celery import Celery
import os

# Use RabbitMQ as the message broker
broker_url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672//")

# Create the Celery app
celery_app = Celery("myapp", broker=broker_url)

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Rest of the code


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

    news_sources = fetch_sources()

    return render_template('index.html', articles_by_source=articles_by_source, news_sources=news_sources)

@app.route('/update_content', methods=['POST'])
def update_content():
    # Run background tasks
    celery_app.send_task("_celery.scrape_articles_task")
    celery_app.send_task("_celery.data_preprocessing_task")

    return "Scraping and preprocessing tasks started in the background", 202

if __name__ == '__main__':
    app.run(debug=True)
