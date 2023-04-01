from flask import Flask, render_template
import json

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

if __name__ == '__main__':
    app.run(debug=True)
