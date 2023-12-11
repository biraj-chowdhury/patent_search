import json

# Define the queries
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
    "Artificial Photosynthesis for Carbon Capture"  # Specific in 
]

def process_patents(patents_data, queries):
    # Create a dictionary to hold the query results
    query_results = {query: [] for query in queries}

    # Process each patent and categorize them under the corresponding query
    for patent in patents_data:
        query = patent.get('query')
        if query in query_results:
            query_results[query].append({
                "patent_name": patent.get('patent_name', ''),
                "patent_number": patent.get('patent_number', ''),
                "date_produced": patent.get('date_produced', ''),
                "rank": patent.get('rank', -1),  # Assume a default rank if not present
                # Add any other fields you need
            })

    # Sort the patents for each query based on their rank
    for query in query_results:
        query_results[query].sort(key=lambda x: x['rank'])

    return query_results

def main():
    # Load the patent data from the JSON file
    try:
        with open('json/patents_test_data.json', 'r') as file:
            patents_data = json.load(file)
    except FileNotFoundError:
        print("File patents_test_data.json not found.")
        return

    # Process the patents and get the results
    results = process_patents(patents_data, queries)

    # Convert the results to a list of JSON objects
    answer_key = [{"query": query, "patents": patents} for query, patents in results.items()]

    # Save the results to answer_key.json
    with open('json/answer_key.json', 'w') as file:
        json.dump(answer_key, file, indent=4)

    print("answer_key.json has been created.")

if __name__ == "__main__":
    main()
