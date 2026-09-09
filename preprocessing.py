from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


STOP_WORDS = set(stopwords.words("english"))
stemmer = PorterStemmer()


def tokenize(text):
    text = text.lower()
    words = text.split()

    cleaned_words = []

    for word in words:
        cleaned_word = ""

        for char in word:
            if char.isalnum():
                cleaned_word += char

        if cleaned_word and cleaned_word not in STOP_WORDS:
            cleaned_word = stemmer.stem(cleaned_word)
            cleaned_words.append(cleaned_word)

    return cleaned_words