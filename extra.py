import nltk

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("corpus")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text = "NLTK is a leading platform for building Python programs to work with human language data."

# Tokenize the text
words = word_tokenize(text)

# Load English stopwords
stop_words = set(stopwords.words("english"))

# Remove stopwords
filtered_words = [word for word in words if word.lower() not in stop_words]

# Join the filtered words back into a string
filtered_text = " ".join(filtered_words)

print("Original Text:")
print(text)
print("original Text words: ", len(text.split(" ")))
print("\nText after removing stopwords:")
print(filtered_text)
print("filter Text words: ", len(filtered_text.split(" ")))
