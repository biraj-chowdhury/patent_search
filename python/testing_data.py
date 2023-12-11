import requests
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import time
import json

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def fetch_patent_ids(query):
    params = {
        "engine": "google_patents",
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "78c03bd07c50e637494f478ed22a4428e47dbf81366993ff396c4f81bc0e2265"
    }

    search = GoogleSearch(params)
    results = search.get_dict().get('organic_results', [])[:15]
    return results

def scrape_google_patents(patent_url):
    response = requests.get(patent_url)
    if response.status_code != 200:
        print(f"Failed to fetch patent details from {patent_url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    abstract = soup.find('section', itemprop='abstract').get_text(strip=True) if soup.find('section', itemprop='abstract') else ''
    claims = soup.find('section', itemprop='claims').get_text(strip=True) if soup.find('section', itemprop='claims') else ''
    description = soup.find('section', itemprop='description').get_text(strip=True) if soup.find('section', itemprop='description') else ''
    
    # Extracting additional fields from HTML
    background = soup.find("heading", string="BACKGROUND OF THE INVENTION")
    background = background.find_next("div").text.strip() if background else ''

    summary = soup.find("heading", string="SUMMARY OF THE INVENTION")
    summary = summary.find_next("div").text.strip() if summary else ''

    patent_data = {
        'abstract': abstract,
        'claims': claims,
        'description': description,
        'background': background,
        'summary': summary
    }
    return patent_data

def preprocess_and_remove_stopwords(text, stop_words, stemmer):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join([word for word in stemmed_tokens if word not in stop_words])

def main():
    queries = [
    "Artificial Intelligence",  # Broad and general
    "Solar Energy Systems",  # Another broad topic
    "Autonomous Vehicles in Urban Environments",  # More specific
    "CRISPR Gene Editing Applications",  # Broad in biotech
    "Machine Learning in Stock Market Prediction",  # Specific application of AI
    "Blockchain for Voting Systems",  # Specific application of technology
    "Nanotechnology in Cancer Treatment",  # Narrow focus in nanotech
    "Augmented Reality in Classroom Learning",  # Specific educational technology
    "IoT Security Protocols in Manufacturing",  # Narrow focus in IoT
    "Deep Sea Exploration Technologies",  # Broad in marine technology
    "Quantum Computing for Data Encryption",  # Specific application in quantum computing
    "Sustainable Farming Practices",  # Broad in agriculture
    "5G Network Implementation Challenges",  # Specific in telecommunication
    "Wearable Health Monitoring Devices",  # Narrow focus in healthcare tech
    "Virtual Reality in Surgical Training",  # Specific in medical training
    "Biodegradable Packaging Materials",  # Broad in materials science
    "Air Quality Monitoring using Drones",  # Specific in environmental monitoring
    "Neural Networks for Language Translation",  # Specific in computational linguistics
    "Hydroponic Systems in Urban Farming",  # Specific in urban agriculture
    "Graphene Batteries in Electric Vehicles",  # Specific in energy storage
    "Machine Learning in Cybersecurity Threat Detection",  # Narrow focus in cybersecurity
    "Biomimicry in Architectural Design",  # Specific in sustainable design
    "Robotics in Precision Agriculture",  # Specific in agricultural automation
    "3D Bioprinting of Human Organs",  # Narrow focus in medical technology
    "Microplastic Removal Techniques in Oceans",  # Specific in environmental conservation
    "Smart Cities and Traffic Management Systems",  # Specific in urban planning
    "Personalized Learning Algorithms in Online Education",  # Specific in edtech
    "Space Tourism and Commercial Spaceflight",  # Broad in aerospace
    "Virtual Assistants in Customer Service",  # Specific in AI applications
    "Renewable Energy Integration in Grid Systems",  # Specific in energy management
    "AI-Powered Personal Finance Management",  # Specific in fintech
    "Waste-to-Energy Conversion Technologies",  # Broad in waste management
    "DNA Data Storage Technologies",  # Specific in data storage
    "Wearable Exoskeletons in Rehabilitation",  # Specific in medical devices
    "Underwater Robotics for Marine Research",  # Specific in marine robotics
    "Autonomous Farming Machinery",  # Specific in agricultural tech
    "Voice Recognition Technology in Smart Homes",  # Specific in home automation
    "Quantum Sensors in Navigation Systems",  # Narrow focus in quantum tech
    "Drone Delivery Systems in Logistics",  # Specific in delivery systems
    "Artificial Photosynthesis for Carbon Capture"  # Specific in environmental tech
    ]


    all_patents_data = []

    for query in queries:
        serpapi_results = fetch_patent_ids(query)
        patents_data = []

        for result in serpapi_results:
            patent_id = result.get('patent_id')
            if patent_id:
                patent_url = f"https://patents.google.com/{patent_id}"
                patent_data = scrape_google_patents(patent_url)
                if patent_data:
                    merged_data = {
                        'title': result.get('title', ''),
                        'filing_date': result.get('filing_date', ''),
                        'patent_number': result.get('patent_id', ''),
                        **patent_data
                    }

                    concatenated_text = ' '.join([str(merged_data[field]) for field in ['title', 'abstract', 'claims', 'description', 'background', 'summary']])
                    preprocessed_text = preprocess_and_remove_stopwords(concatenated_text, stop_words, stemmer)
                    
                    final_data = {
                        "patent_name": merged_data.get('title', ''),
                        "patent_number": merged_data.get('patent_number', ''),
                        "date_produced": merged_data.get('filing_date', ''),
                        "processed_data": preprocessed_text,
                        "query": query,
                        "rank": result.get('rank')
                    }

                    patents_data.append(final_data)

            time.sleep(1)  # Rate limiting to avoid being blocked

        all_patents_data.extend(patents_data)

    # Saving all data to a JSON file
    with open('patents_test_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_patents_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
