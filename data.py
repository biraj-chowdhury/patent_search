from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import json

# Load NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

# Function to preprocess and remove stopwords
def preprocess_and_remove_stopwords(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    return ' '.join([word for word in tokens if word not in stop_words])

# Try loading the dataset
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
    def concatenate_and_preprocess(dataset):
        patents_data = []
        for patent in dataset:
            concatenated_text = ' '.join([str(patent[field]) for field in ['title', 'abstract', 'claims', 'background', 'summary', 'description'] if field in patent])
            preprocessed_text = preprocess_and_remove_stopwords(concatenated_text)
            patents_data.append({
                "patent_name": patent.get('title', ''),
                "patent_number": patent.get('patent_number', ''),
                "uspc_class": patent.get('uspc_class', ''),
                "uspc_subclass": patent.get('uspc_subclass', ''),
                "date_produced": patent.get('filing_date', ''),
                "processed_data": preprocessed_text
            })
        return patents_data

    patents_info = concatenate_and_preprocess(dataset)

    # Save to JSON file
    with open('patents.json', 'w') as f:
        json.dump(patents_info, f, indent=4)
else:
    print("Failed to load dataset")
