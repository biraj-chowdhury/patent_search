import json

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_overlap(query_results, answer_key):
    overlap_scores = []

    for query_result in query_results:
        query = query_result['query']
        result_patents = set([patent['patent_name'] for patent in query_result['relevant_patents']])

        # Find the corresponding query in answer_key
        answer_patents = []
        for answer in answer_key:
            if answer['query'] == query:
                answer_patents = set([patent['patent_name'] for patent in answer['patents']])
                break

        # Calculate overlap
        overlap = len(result_patents.intersection(answer_patents))
        total = min(len(result_patents), len(answer_patents))
        percentage_overlap = (overlap / total) * 100 if total > 0 else 0

        overlap_scores.append({
            "query": query,
            "percentage_overlap": percentage_overlap
        })

    # Calculate aggregate percentage
    aggregate_percentage = sum(score['percentage_overlap'] for score in overlap_scores) / len(overlap_scores)
    
    return overlap_scores, aggregate_percentage

def main():
    # Load data from JSON files
    query_results = load_json_data('query_results.json')
    answer_key = load_json_data('answer_key.json')

    # Calculate overlap scores
    overlap_scores, aggregate_percentage = calculate_overlap(query_results, answer_key)

    # Save results to a JSON file
    with open('overlap_score.json', 'w') as file:
        json.dump({
            "individual_overlap_scores": overlap_scores,
            "aggregate_percentage": aggregate_percentage
        }, file, indent=4)

    print("Overlap scores have been saved to overlap_score.json")

if __name__ == "__main__":
    main()
