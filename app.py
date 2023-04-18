from flask import Flask, render_template, request, jsonify
# from flask_caching import Cache
import json
import web_scraper
# from data_preprocessing import data_preprocessing
import traceback
# import requests
# from celery import Celery
# import os
# from categorize_news import classify_and_tag_articles

app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# # Celery configuration
# app.config.from_object("celery_config")
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# Add this line at the beginning of your app code
USE_CELERY = False
# @celery.task
def update_content_task():
    try:
        web_scraper.scrape_articles()
    except Exception as e:
        print(traceback.format_exc())
        return str(e), 500


@app.route('/')
# @cache.cached(timeout=3600)  # Cache for 1 hour
def index():
    with open('news_dataset.json', 'r') as file:
        articles = json.load(file)
    # Add tags to the cleaned_articles
    # classify_and_tag_articles(articles)

    articles_by_source = {}
    for article in articles:
        source = article['source']
        if source not in articles_by_source:
            articles_by_source[source] = []
        articles_by_source[source].append(article)

    return render_template('index.html', articles_by_source=articles_by_source, news_sources=web_scraper.fetch_sources())



# Replace the current update_content() function with the following code
@app.route('/update_content', methods=['POST'])
def update_content():
    print("Scraping Articles")
    if USE_CELERY:
        update_content_task.delay()
        return "Content update started. Please refresh the page after a while.", 202
    else:
        try:
            update_content_task()
            return "Content updated successfully.", 202
        except Exception as e:
            print(traceback.format_exc())
            return str(e), 500


scraped_sources = []


@app.route('/scrape_more_articles')
def scrape_more_articles():
    global scraped_sources
    start = int(request.args.get('start', 0))
    end = int(request.args.get('end', 2))
    print("GETINGGGGGG")
    unscraped_sources = web_scraper.fetch_unscraped_sources(scraped_sources)
    new_sources = unscraped_sources[start:end]
    scraped_sources.extend(new_sources)

    new_articles = []
    for source in new_sources:
        new_articles.extend(web_scraper.process_source(source))

    with open('news_dataset.json', 'r') as file:
        all_articles = json.load(file)
    all_articles.extend(new_articles)

    with open('news_dataset.json', 'w') as file:
        json.dump(all_articles, file)

    articles_by_source = {}
    for article in new_articles:
        source = article['source']
        if source not in articles_by_source:
            articles_by_source[source] = []
        articles_by_source[source].append(article)

    return jsonify({"html": render_template('new_articles.html', articles_by_source=articles_by_source)})


if __name__ == '__main__':

    app.config['DEBUG'] = True
    app.run()
