import nltk
from nltk.corpus import movie_reviews
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from collections import Counter

# Data Collection
nltk.download('movie_reviews')
nltk.download('stopwords')
nltk.download('punkt')

def load_data():
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    return documents

documents = load_data()

# Data Preprocessing
stop_words = set(stopwords.words('english'))

def preprocess(sentence):
    words = word_tokenize(sentence)
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    return words

# Feature Extraction
def extract_features(documents):
    vectorizer = CountVectorizer(analyzer=lambda x: x)
    features = vectorizer.fit_transform([' '.join(doc) for doc, _ in documents])
    return features, vectorizer

# Check Label Distribution
def check_label_distribution(documents):
    labels = [label for _, label in documents]
    return Counter(labels)

print(check_label_distribution(documents))

# Model Training
def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

# Evaluate Model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

# Prepare Data and Train Model
labels = [label for _, label in documents]
features, vectorizer = extract_features(documents)
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
model = train_model(X_train, y_train)
evaluate_model(model, X_test, y_test)

# Sentiment Analysis Pipeline
def sentiment_analysis_pipeline(sentence):
    preprocessed_sentence = preprocess(sentence)
    features = vectorizer.transform([' '.join(preprocessed_sentence)])
    prediction = model.predict(features)
    return 'positive' if prediction[0] == 'pos' else 'negative'

# Test Sentiment Analysis
sentence = input("Enter: ")
sentiment = sentiment_analysis_pipeline(sentence)
print(f'Sentiment: {sentiment}')
