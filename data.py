from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk

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

# Try loading the dataset with specified training and validation split dates
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

# Rest of your code (if dataset_dict is not None)

if dataset:
    # Concatenate relevant fields and preprocess
    def concatenate_and_preprocess(dataset):
        concatenated_data = {}
        for patent in dataset:
            concatenated_text = ' '.join([str(patent[field]) for field in ['title', 'abstract', 'claims', 'background', 'summary', 'description'] if field in patent])
            preprocessed_text = preprocess_and_remove_stopwords(concatenated_text)
            concatenated_data[patent['patent_number']] = preprocessed_text
        return concatenated_data

    # Assuming dataset is a single dataset and not split
    data = concatenate_and_preprocess(dataset)

    # Vectorize and apply dimensionality reduction
    vectorizer = TfidfVectorizer()
    svd = TruncatedSVD(n_components=100)  # You can adjust the number of components

    data_tfidf = vectorizer.fit_transform(data.values())

    data_reduced = svd.fit_transform(data_tfidf)

    # Create dictionary with reduced text
    data_dict = {patent_number: text.tolist() for patent_number, text in zip(data.keys(), data_reduced)}

    # Print first 5 entries of the dictionary
    for i, (patent_number, text) in enumerate(data_dict.items()):
        if i < 5:
            print(patent_number, text)
else:
    print("Failed to load dataset")
