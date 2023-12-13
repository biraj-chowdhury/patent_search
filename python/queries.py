# Sample Queries for Testing Patent Search Models

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

# Exporting to a file
with open('patent_queries.txt', 'w') as file:
    for query in queries:
        file.write(f"{query}\n")

print("100 patent-related queries have been saved to 'patent_queries.txt'")
