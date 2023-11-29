from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Function to preprocess and remove stopwords
def preprocess_and_remove_stopwords(text, stop_words, stemmer):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join([word for word in stemmed_tokens if word not in stop_words])

# Function to insert data into MongoDB in batches
def batch_insert(collection, data, batch_size=100):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        try:
            collection.insert_many(batch)
            print(f"Batch {i // batch_size + 1} inserted successfully")
        except Exception as e:
            print(f"Error inserting batch {i // batch_size + 1}: {e}")

# Load NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

uri = "mongodb+srv://patent_data:patent_data@cluster0.fhrejvf.mongodb.net/?retryWrites=true&w=majority"

# Function to test MongoDB connection and ensure database and collection exist
def test_mongodb_connection_and_setup(client, db_name, collection_name):
    try:
        db = client[db_name]
        if collection_name not in db.list_collection_names():
            print(f"Collection '{collection_name}' does not exist. It will be created automatically when inserting the first document.")
        collection = db[collection_name]

        # Test insertion and deletion to confirm that the database and collection are operational
        collection.insert_one({"test": "value"})  # Insert a test document
        collection.delete_one({"test": "value"})  # Clean up test document
        print("MongoDB connection test and setup successful.")
        return True, collection
    except Exception as e:
        print(f"MongoDB connection test and setup failed: {e}")
        return False, None

# Initialize MongoDB client
client = MongoClient(uri, server_api=ServerApi('1'))

# Check MongoDB connection and setup
db_name = 'patent_database'  # Replace with your database name
collection_name = 'patents'  # Replace with your collection name
connection_successful, collection = test_mongodb_connection_and_setup(client, db_name, collection_name)

if connection_successful:
    # Try loading the dataset only if MongoDB connection is successful
    try:
        dataset = load_dataset(
            'HUPD/hupd',
            name='sample',
            split='train',
            data_files="https://huggingface.co/datasets/HUPD/hupd/blob/main/hupd_metadata_2022-02-22.feather",
            train_filing_start_date='2016-01-01',
            train_filing_end_date='2016-12-31',
            val_filing_start_date='2017-01-01',
            val_filing_end_date='2017-12-31'
        )
    except Exception as e:
        print("Error loading dataset:", e)
        dataset = None

    if dataset:
        # Function to concatenate and preprocess dataset
        def concatenate_and_preprocess(dataset):
            patents_data = []
            for patent in dataset:
                try:
                    concatenated_text = ' '.join([str(patent[field]) for field in ['title', 'abstract', 'claims', 'background', 'summary', 'description'] if field in patent])
                    preprocessed_text = preprocess_and_remove_stopwords(concatenated_text, stop_words, stemmer)
                    patents_data.append({
                        "patent_name": patent.get('title', ''),
                        "patent_number": patent.get('patent_number', ''),
                        "uspc_class": patent.get('uspc_class', ''),
                        "uspc_subclass": patent.get('uspc_subclass', ''),
                        "date_produced": patent.get('filing_date', ''),
                        "processed_data": preprocessed_text
                    })
                except Exception as e:
                    print(f"Error processing patent: {e}")
            return patents_data

        patents_info = concatenate_and_preprocess(dataset)

        # Insert into MongoDB in batches
        batch_insert(collection, patents_info)
else:
    print("Skipping dataset loading due to MongoDB connection issues.")

# Close the MongoDB connection
client.close()
