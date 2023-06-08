import nltk
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
# import transformers
#
# # Load the Hugging Face chatbot model.
# model = transformers.AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

def summarize_text(text):
  """Summarizes the text into 5 bullets.

  Args:
    text: The text to summarize.

  Returns:
    A list of 5 bullets.
  """

  # Encode the text.
  encoded_input = model.tokenizer(text, max_length=512, padding="max_length", truncation=True)

  # Generate the summary.
  summary = model.generate(encoded_input, max_length=100, num_beams=5, do_sample=True)

  # Convert the summary to a list of bullets.
  bullets = []
  for i in range(len(summary)):
    bullets.append(summary[i].strip())

  # Return the list of bullets.
  return bullets[:5]

def summarize_news_article(text):
    """Summarizes a news article into 5 most relevant bullets.

    Args:
        article: The news article to summarize.

    Returns:
        A list of 5 most relevant bullets.
    """

    # Create a list of sentences.
    sentences = nltk.sent_tokenize(text)

    # Extract the most important sentences.
    important_sentences = extract_important_sentences(sentences)

    # Create a list of bullets.
    bullets = []
    for sentence in important_sentences:
        bullets.append(sentence)

    # Return the list of bullets.
    return bullets

def extract_important_sentences(sentences):
    """Extracts the most important sentences from a list of sentences.

    Args:
        sentences: A list of sentences.

    Returns:
        A list of the most important sentences.
    """

    # Create a bag of words using TF-IDF.
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Calculate the sentence scores based on TF-IDF.
    sentence_scores = tfidf_matrix.sum(axis=1)

    # Get the indices of top 5 sentences with the highest scores.
    top_sentence_indices = sentence_scores.argsort(axis=0)[-5:][::-1]

    # Retrieve the important sentences.
    important_sentences = [sentences[idx[0, 0]] for idx in top_sentence_indices]

    # Return the list of important sentences.
    return important_sentences

def main():
    # Get the news articles.
    file_path = os.path.join(os.path.dirname(__file__), 'news_dataset.json')

    # Open the file.
    with open(file_path, 'r') as file:
        articles = json.load(file)

    # Summarize each news article.
    for article in articles:
        # bullets = summarize_news_article(article)
        bullets = summarize_text(article)

        # Show the news summary bullets at the top of the news article complete text.
        print(bullets)
        print()
        print(article['text'])

if __name__ == '__main__':
    main()
