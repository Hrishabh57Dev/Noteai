from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def abstractive_summarization(text, length="medium"):
    """
    Generates an abstractive summary using Hugging Face transformers.

    Args:
        text (str): The input text to summarize.
        length (str): The desired summary length ("short", "medium", "long").

    Returns:
        str: The summarized text.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    length_map = {"short": 50, "medium": 150, "long": 300}
    max_length = length_map.get(length, 150)
    summary = summarizer(text, max_length=max_length, min_length=max_length // 2, do_sample=False)
    return summary[0]["summary_text"]

def extractive_summarization(text, length="medium"):
    """
    Generates an extractive summary using Sumy.

    Args:
        text (str): The input text to summarize.
        length (str): The desired summary length ("short", "medium", "long").

    Returns:
        str: The summarized text.
    """
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    length_map = {"short": 3, "medium": 5, "long": 10}
    num_sentences = length_map.get(length, 5)
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

def summarize_text(text, method="abstractive", length="medium"):
    """
    Summarizes the given text using the specified method and length.

    Args:
        text (str): The input text to summarize.
        method (str): The summarization method ("abstractive" or "extractive").
        length (str): The desired summary length ("short", "medium", "long").

    Returns:
        str: The summarized text.
    """
    if method == "abstractive":
        return abstractive_summarization(text, length)
    elif method == "extractive":
        return extractive_summarization(text, length)
    else:
        raise ValueError("Invalid method. Use 'abstractive' or 'extractive'.")
