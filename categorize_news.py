import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

# Load pre-trained BERT model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define the categories
categories = {
    "AI": ["artificial intelligence", "machine learning", "deep learning", "neural networks", "robotics", "nlp"],
    "Supply Chain": ["supply chain", "logistics", "inventory", "procurement", "shipping", "warehouse"],
}

def predict_category(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    category_idx = torch.argmax(probabilities).item()
    return category_idx

def categorize_news(news_text):
    news_categories = set()

    for category, keywords in categories.items():
        for keyword in keywords:
            if predict_category(f"{news_text} {keyword}") == 1:
                news_categories.add(category)

    return list(news_categories)

# Categorize and add tags to the scraped news
def classify_and_tag_articles(articles):
    for article in articles:
        article['tags'] = categorize_news(article['text'])
    return articles

# # Print the categorized news articles
# print(json.dumps(scraped_news, indent=2))
