import json

def load_json_data(filename):
    with open(f'json/test/{filename}', 'r') as file:
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

def calc_average_precision_and_map_score(query_results, answer_key) -> float:
    AP_scores = []

    query_set = set()
    answer_set = set()
    for query_result, answer in zip(query_results, answer_key):
        average_precision = 0
        for retrieved_patent, relevant_patent in zip(query_result['relevant_patents'], answer['patents']):
            query_set.add(retrieved_patent['patent_name'])
            answer_set.add(relevant_patent['patent_name'])

            overlap = len(query_set.intersection(answer_set))
            total = len(answer_set)

            average_precision += (overlap / total)
        
        average_precision /= len(answer['patents'])
        query_set.clear()
        answer_set.clear()

        AP_scores.append({
            "query": query_result['query'],
            "average_precision": average_precision
        })

    map_score = sum(ap['average_precision'] for ap in AP_scores) / len(AP_scores)
    return AP_scores, map_score

def main():
    # Load data from JSON files
    query_results = load_json_data('query_results.json')
    answer_key = load_json_data('manually_annotated_answer_key.json')

    # Calculate overlap scores
    # overlap_scores, aggregate_percentage = calculate_overlap(query_results, answer_key)

    # # Save results to a JSON file
    # with open('overlap_score.json', 'w') as file:
    #     json.dump({
    #         "individual_overlap_scores": overlap_scores,
    #         "aggregate_percentage": aggregate_percentage
    #     }, file, indent=4)

    # Calculate Average-Precision per query and MAP-Score
    ap_scores, map_score = calc_average_precision_and_map_score(query_results, answer_key)

    # Save results to a JSON file
    with open('json/test/scores.json', 'w') as file:
        json.dump({
            "average_precision": ap_scores,
            "MAP-Score": map_score
        }, file, indent=4)

    print("Evaluation metrics saved to scores.json")

if __name__ == "__main__":
    main()
