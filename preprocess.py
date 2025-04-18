import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

nltk.download('stopwords')

def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

df = pd.read_csv('imdb_2024.csv')
df['Cleaned_Storyline'] = df['Storyline'].apply(preprocess)

# Save cleaned data
df.to_csv('cleaned_imdb_2024.csv', index=False)

# TF-IDF Vectorization
tfidf = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['Cleaned_Storyline'])

# Save vectorizer and matrix
joblib.dump(tfidf, 'tfidf_vectorizer.joblib')
joblib.dump(tfidf_matrix, 'tfidf_matrix.joblib')