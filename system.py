import json
from gensim import corpora, models, similarities
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import nltk

# MongoDB connection details
uri = "mongodb+srv://patent_data:patent_data@cluster0.fhrejvf.mongodb.net/?retryWrites=true&w=majority"

# Initialize MongoDB client
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the patent database and collection
db = client['patent_database']
collection = db['patents']

# Fetch patent data from MongoDB
patents_data = list(collection.find({}, {'_id': 0, 'processed_data': 1, 'patent_name': 1}))

# Extract the processed patent texts
patent_texts = [patent['processed_data'] for patent in patents_data]

# Tokenize the documents
tokenized_patents = [nltk.word_tokenize(text) for text in patent_texts]

# Create a dictionary representation of the documents
dictionary = corpora.Dictionary(tokenized_patents)

# Create a bag-of-words corpus
corpus = [dictionary.doc2bow(text) for text in tokenized_patents]

# Create a TF-IDF model from the corpus
tfidf_model = models.TfidfModel(corpus)
corpus_tfidf = tfidf_model[corpus]

# Train the LDA model on the TF-IDF corpus
lda_model = models.LdaModel(corpus_tfidf, num_topics=10, id2word=dictionary, passes=15)

# Load query terms
with open('patents_queries.txt', 'r') as file:
    queries = file.readlines()
queries = [query.strip() for query in queries]

# Number of top patents to retrieve for each query
top_n = 5

# Convert queries to LDA space and find similarity
for query in queries:
    query_bow = dictionary.doc2bow(nltk.word_tokenize(query))
    query_lda = lda_model[tfidf_model[query_bow]]

    similarities_index = similarities.MatrixSimilarity(lda_model[corpus_tfidf])
    cosine_similarities = similarities_index[query_lda]

    relevant_patents_indices = cosine_similarities.argsort()[-top_n:][::-1]  # Indices of top N relevant patents

    print(f"\nMost relevant patents for query: '{query}'")
    for index in relevant_patents_indices:
        print(f"Patent: {patents_data[index]['patent_name']} (Score: {cosine_similarities[index]:.4f})")

# Close the MongoDB connection
client.close()
