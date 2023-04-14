from celery import Celery
import os

# Use RabbitMQ as the message broker
broker_url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672//")

# Create the Celery app
app = Celery("app", broker=broker_url)

@app.task
def scrape_articles_task():
    from web_scraper import scrape_articles
    scrape_articles()

@app.task
def data_preprocessing_task():
    from data_preprocessing import data_preprocessing
    data_preprocessing()
