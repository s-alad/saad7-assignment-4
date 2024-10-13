import numpy as np
import pickle
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import os

# Fetch the dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data

# Create the term-document matrix
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
td_matrix = vectorizer.fit_transform(documents)

# Apply SVD
svd = TruncatedSVD(n_components=100, random_state=42)
documents_lsa = svd.fit_transform(td_matrix)

# Create 'models' directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

# Save the vectorizer, svd, documents_lsa, and documents
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('models/svd.pkl', 'wb') as f:
    pickle.dump(svd, f)

with open('models/documents_lsa.npy', 'wb') as f:
    np.save(f, documents_lsa)

with open('models/documents.pkl', 'wb') as f:
    pickle.dump(documents, f)

print("Preprocessing completed and models saved.")
