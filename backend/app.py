from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the models
with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('models/svd.pkl', 'rb') as f:
    svd = pickle.load(f)

with open('models/documents_lsa.npy', 'rb') as f:
    documents_lsa = np.load(f)

with open('models/documents.pkl', 'rb') as f:
    documents = pickle.load(f)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Empty query'}), 400

    # Transform the query
    query_tfidf = vectorizer.transform([query])
    query_lsa = svd.transform(query_tfidf)

    # Compute cosine similarities
    similarities = cosine_similarity(query_lsa, documents_lsa)[0]

    # Get top 5 documents
    top_indices = similarities.argsort()[::-1][:5]
    top_scores = similarities[top_indices]
    top_documents = [documents[i] for i in top_indices]

    results = []
    for idx, (doc, score) in enumerate(zip(top_documents, top_scores)):
        results.append({
            'rank': idx + 1,
            'document': doc,
            'score': float(score)
        })

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(port=5000)
