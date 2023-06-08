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
    inputs = tokenizer(text, return_tensors="pt",  truncation=True) #max_length=512,
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
if __name__ == '__main__':
    with open('news_dataset.json', 'r') as file:
        articles = json.load(file)
    articles = classify_and_tag_articles(articles)
    print(articles)


from transformers import pipeline
import json
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english",   truncation=True)

def generate_tags(text):
    result = classifier(text)
    tags = []
    for r in result:
        label = r["label"].replace("LABEL_", "").lower()
        if label not in tags:
            tags.append(label)
    return tags

from keybert import KeyBERT
import json
model = KeyBERT('distilbert-base-nli-mean-tokens')

def extract_tags(text, num_tags=5):
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=num_tags)
    tags = [keyword[0] for keyword in keywords]
    return tags

if __name__ == '__main__':
    with open('news_dataset.json', 'r') as file:
        articles = json.load(file)
    for article in articles:
        text = article['text']
        tag = extract_tags(text)
        print (tag)