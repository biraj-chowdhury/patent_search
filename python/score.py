import json
import numpy as np

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

# Gather metrics for Average Precision, MAP, Normalized Discounted Cumulative Gain, and Mean NDCG
def calculate_metrics(query_results, answer_key) -> float:
    scores = []

    for query_result, answer in zip(query_results, answer_key):
        # Metric at kth document
        precision_at_k = 0
        DCG_k = 0
        IDCG_k = 0
        k = 1

        total_relevant = {}
        query_set = set()
        answer_set = set()
        for patent in answer['patents']:
            total_relevant[patent['patent_name']] = patent['relevance']

        for retrieved_patent, relevant_patent in zip(query_result['relevant_patents'], answer['patents']):
            output_patent = retrieved_patent['patent_name']
            ideal_patent = relevant_patent['patent_name']
            
            log_denominator = np.log2(k+1)
            DCG_k += (total_relevant.get(output_patent, 0) / log_denominator)
            IDCG_k += (relevant_patent['relevance'] / log_denominator)

            query_set.add(output_patent)
            answer_set.add(ideal_patent)
            overlap = len(query_set.intersection(answer_set))
            total = len(answer_set)

            precision_at_k += ((overlap / total) * (1 if output_patent in total_relevant else 0))
            k += 1
        

        average_precision = precision_at_k / len(answer['patents'])
        normalized_DCG = DCG_k / IDCG_k

        scores.append({
            "query": query_result['query'],
            "average_precision": average_precision,
            "nDCG": normalized_DCG
        })

    map_score = sum(ap['average_precision'] for ap in scores) / len(scores)
    mean_NDCG = sum(ap['nDCG'] for ap in scores) / len(scores)
    return scores, map_score, mean_NDCG

def main():
    # Load data from JSON files
    query_results = load_json_data('backup.json')
    answer_key = load_json_data('manually_annotated_answer_key.json')

    scores, map_score, mean_nDCG = calculate_metrics(query_results, answer_key)

    # Save results to a JSON file
    with open('json/test/scores.json', 'w') as file:
        json.dump({
            "average_precision": scores,
            "MAP-Score": map_score,
            "Mean nDCG": mean_nDCG
        }, file, indent=4)

    print("Evaluation metrics saved to scores.json")

if __name__ == "__main__":
    main()
