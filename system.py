import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load patents data
with open('patents.json', 'r') as file:
    patents_data = json.load(file)

# Extract the processed patent texts
patent_texts = [patent['processed_data'] for patent in patents_data]

# Load query terms
with open('queries.txt', 'r') as file:
    queries = file.readlines()
queries = [query.strip() for query in queries]

# Apply TF-IDF to the patent texts
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(patent_texts)

# Find the similarity of each patent to each query
query_tfidf = tfidf_vectorizer.transform(queries)

# Number of top patents to retrieve for each query
top_n = 5

for query_index, query in enumerate(queries):
    cosine_similarities = cosine_similarity(query_tfidf[query_index:query_index+1], tfidf_matrix).flatten()
    relevant_patents_indices = cosine_similarities.argsort()[-top_n:][::-1]  # Indices of top N relevant patents

    print(f"\nMost relevant patents for query: '{query}'")
    for index in relevant_patents_indices:
        print(f"Patent: {patents_data[index]['patent_name']} (Score: {cosine_similarities[index]:.4f})")
