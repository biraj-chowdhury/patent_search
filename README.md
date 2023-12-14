# _Patent Search - Information Retrieval NLP Project_

## File Overview 

- `python/`
    - All codefiles can be found in this directory
    - `data.py` is a script to collect data from Harvard's USPTO dataset
    - `testing_data.py` is a script to collect relevant results from google-patents
    - `system.py` contains most of the source-code for our custom IR system for patents
    - `score.py` is used to compare, evaluate, and provide metrics on our results and test/dev/train data

- `json/`
    - `dev/`
        - Contains data/relevant-docs/results/metrics for dev set
    - `test/`
        - Contains data/documents and metrics for test set
        - Utilizes manually annotated answer key

## Results

See [scores.json](/json/test/scores.json) for results.