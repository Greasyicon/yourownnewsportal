from flask import Flask, render_template, request
import json
from web_scraper import scrape_articles
from data_preprocessing import data_preprocessing
import traceback

app = Flask(__name__)

@app.route('/')
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

@app.route('/update_content', methods=['POST'])
def update_content():
    print("Scraping Articles")
    try:
        return scrape_articles(), 200
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

    return render_template('content.html', articles_by_source=articles_by_source)

if __name__ == '__main__':
    app.run(debug=True)
