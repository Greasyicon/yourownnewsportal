# # data_preprocessing.py
#
# import json
# import re
# import string
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from concurrent.futures import ProcessPoolExecutor, as_completed
#
# nltk.download('punkt')
# nltk.download('stopwords')
#
# STOPWORDS = set(stopwords.words('english'))
#
#
# def clean_text(text):
#     # Remove special characters and numbers
#     text = re.sub(r'\n', ' ', text)
#     text = re.sub(r'\s+', ' ', text)
#     text = re.sub(r'\d+', '', text)
#     text = text.lower()
#
#     # Remove stopwords
#     tokens = word_tokenize(text)
#     tokens = [token for token in tokens if token not in STOPWORDS]
#
#     cleaned_text = ' '.join(tokens)
#     return cleaned_text
#
#
# def clean_article(article):
#     try:
#         cleaned_title = clean_text(article['title'])
#         cleaned_text = clean_text(article['text'])
#
#         cleaned_article = {
#             "source": article["source"],
#             "title": cleaned_title,
#             "text": cleaned_text,
#         }
#         return cleaned_article
#     except Exception as e:
#         print(f"Error while cleaning article: {e}")
#         return None
#
#
# def main():
#     with open("news_dataset.json", "r") as file:
#         all_articles = json.load(file)
#
#     cleaned_articles = []
#     articles_with_text = 0
#     articles_without_text = 0
#
#     # Process multiple articles concurrently using ProcessPoolExecutor
#     with ProcessPoolExecutor() as executor:
#         futures = {executor.submit(clean_article, article): article for article in all_articles}
#
#         for future in as_completed(futures):
#             try:
#                 cleaned_article = future.result()
#
#                 # Count articles with and without text
#                 if cleaned_article['text'].strip():
#                     articles_with_text += 1
#                     cleaned_articles.append(cleaned_article)
#                 else:
#                     articles_without_text += 1
#             except Exception as e:
#                 print(f"Error while processing an article: {e}")
#
#     with open("cleaned_news_dataset.json", "w") as file:
#         json.dump(cleaned_articles, file)
#
#     print("Cleaned dataset saved to cleaned_news_dataset.json")
#     print(f"Articles with text: {articles_with_text}")
#     print(f"Articles without text: {articles_without_text}")
#
#     # Print some examples
#     for i, article in enumerate(cleaned_articles[:5]):
#         print(f"Example {i + 1}:")
#         print(f"Source: {article['source']}")
#         print(f"Title: {article['title']}")
#         print(f"Text: {article['text']}\n")
#
#
# if __name__ == "__main__":
#     main()
# data_preprocessing.py
#

# data_preprocessing.py

import json
import re
# import string
import nltk
# from nltk.tokenize import word_tokenize
from concurrent.futures import ProcessPoolExecutor, as_completed
from unidecode import unidecode

# nltk.download('punkt')

def clean_text(text):
    # Decode Unicode characters to their closest ASCII representation
    text = unidecode(text)

    # Remove special characters and extra spaces
    text = re.sub(r'\n', ' ', text)
    # text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\"+', ' ', text)
    # text = text.lower()
    return text

def clean_article(article):
    try:
        cleaned_title = clean_text(article['title'])
        cleaned_text = clean_text(article['text'])

        cleaned_article = {
            "source": article["source"],
            "title": cleaned_title,
            "text": cleaned_text,
        }
        return cleaned_article
    except Exception as e:
        print(f"Error while cleaning article: {e}")
        return None

def data_preprocessing():
    with open("news_dataset.json", "r") as file:
        all_articles = json.load(file)

    cleaned_articles = []
    articles_with_text = 0
    articles_without_text = 0

    # Process multiple articles concurrently using ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(clean_article, article): article for article in all_articles}

        for future in as_completed(futures):
            try:
                cleaned_article = future.result()

                # Count articles with and without text
                if cleaned_article['text'].strip():
                    articles_with_text += 1
                    cleaned_articles.append(cleaned_article)
                else:
                    articles_without_text += 1
            except Exception as e:
                print(f"Error while processing an article: {e}")

    with open("cleaned_news_dataset.json", "w") as file:
        json.dump(cleaned_articles, file)

    print("Cleaned dataset saved to cleaned_news_dataset.json")
    print(f"Articles with text: {articles_with_text}")
    print(f"Articles without text: {articles_without_text}")

    # Print some examples
    for i, article in enumerate(cleaned_articles[:5]):
        print(f"Example {i + 1}:")
        print(f"Source: {article['source']}")
        print(f"Title: {article['title']}")
        print(f"Text: {article['text']}\n")


if __name__ == "__main__":
    data_preprocessing()
