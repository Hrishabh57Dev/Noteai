import spacy
from yake import KeywordExtractor
from sklearn.feature_extraction.text import TfidfVectorizer  # Fixed import

def extract_keywords_spacy(text, num_keywords=10):
    """
    Extracts keywords using spaCy's Named Entity Recognition (NER).

    Args:
        text (str): Input text.
        num_keywords (int): Number of keywords to extract.

    Returns:
        list: List of dictionaries containing keywords and their relevance scores.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [{"keyword": ent.text, "score": 1.0} for ent in doc.ents][:num_keywords]
    return keywords

def extract_keywords_yake(text, num_keywords=10):
    """
    Extracts keywords using YAKE.

    Args:
        text (str): Input text.
        num_keywords (int): Number of keywords to extract.

    Returns:
        list: List of dictionaries containing keywords and their relevance scores.
    """
    extractor = KeywordExtractor(top=num_keywords, stopwords=None)
    keywords = extractor.extract_keywords(text)
    return [{"keyword": kw[0], "score": kw[1]} for kw in keywords]

def extract_keywords_tfidf(text, num_keywords=10):
    """
    Extracts keywords using TF-IDF.

    Args:
        text (str): Input text.
        num_keywords (int): Number of keywords to extract.

    Returns:
        list: List of dictionaries containing keywords and their relevance scores.
    """
    vectorizer = TfidfVectorizer(stop_words="english", max_features=num_keywords)
    tfidf_matrix = vectorizer.fit_transform([text])
    terms = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    return [{"keyword": term, "score": scores[idx]} for idx, term in enumerate(terms)]

def extract_keywords(text, method="spacy", num_keywords=10):
    """
    Extracts keywords from text using the specified method.

    Args:
        text (str): Input text.
        method (str): Extraction method ("spacy", "yake", or "tfidf").
        num_keywords (int): Number of keywords to extract.

    Returns:
        list: List of dictionaries containing keywords and their relevance scores.
    """
    if method == "spacy":
        return extract_keywords_spacy(text, num_keywords)
    elif method == "yake":
        return extract_keywords_yake(text, num_keywords)
    elif method == "tfidf":
        return extract_keywords_tfidf(text, num_keywords)
    else:
        raise ValueError("Invalid method. Use 'spacy', 'yake', or 'tfidf'.")
