import json
import string
import sys
from gensim import corpora, models, similarities
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text, stemmer, stop_words):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    filtered_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    return filtered_tokens

def fetch_data_from_json(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# MongoDB connection details
uri = "mongodb+srv://patent_data:patent_data@cluster0.fhrejvf.mongodb.net/?retryWrites=true&w=majority"

# Initialize stemmer and stopwords
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def main():
    # Check for JSON file argument
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        patents_data = fetch_data_from_json(json_file)
    else:
        # Initialize MongoDB client
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Connect to the patent database and collection
        db = client['patent_database']
        collection = db['patents']

        # Fetch patent data from MongoDB
        patents_data = list(collection.find({}, {'_id': 0, 'processed_data': 1, 'patent_name': 1}))

        # Close the MongoDB connection
        client.close()

    # Extract the processed patent texts
    patent_texts = [patent['processed_data'] for patent in patents_data]

    # Preprocess the patent texts
    preprocessed_patents = [preprocess_text(text, stemmer, stop_words) for text in patent_texts]

    # Create a dictionary representation of the documents
    dictionary = corpora.Dictionary(preprocessed_patents)

    # Create a bag-of-words corpus
    corpus = [dictionary.doc2bow(text) for text in preprocessed_patents]

    # Create a TF-IDF model from the corpus
    tfidf_model = models.TfidfModel(corpus)
    corpus_tfidf = tfidf_model[corpus]

    # Load query terms
    with open('patent_queries.txt', 'r') as file:
        queries = file.readlines()
    queries = [query.strip() for query in queries]

    # Number of top patents to retrieve for each query
    top_n = 5

    # Store query results in a structured format
    query_results = []

    # Convert queries to TF-IDF space and find similarity
    for query in queries:
        preprocessed_query = preprocess_text(query, stemmer, stop_words)
        query_bow = dictionary.doc2bow(preprocessed_query)
        query_tfidf = tfidf_model[query_bow]

        # Compute similarity for the entire corpus
        similarities_index = similarities.MatrixSimilarity(tfidf_model[corpus], num_features=len(dictionary))
        cosine_similarities = np.array(similarities_index[query_tfidf])

        relevant_patents_indices = cosine_similarities.argsort()[-top_n:][::-1]  # Indices of top N relevant patents

        # Store relevant patents for this query
        relevant_patents = []
        for index in relevant_patents_indices:
            relevant_patents.append({
                "patent_name": patents_data[index]['patent_name'],
                "score": float(cosine_similarities[index])
            })

        # Add query and its relevant patents to results
        query_results.append({
            "query": query,
            "relevant_patents": relevant_patents
        })

    # Save query results to a JSON file
    with open('query_results.json', 'w') as file:
        json.dump(query_results, file, indent=4)

    print("query_results.json has been created.")

# Call the main function
if __name__ == "__main__":
    main()
