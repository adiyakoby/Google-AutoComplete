from typing import Dict, List
from zip_opener import ZipOpener
from process_data import ProcessData
from auto_complete import AutoComplete


def user_interaction(ht: Dict[str, List[str]]):
    auto_complete = AutoComplete(ht)
    current_query = ""

    while True:
        query = input(f"{current_query}")
        if query == 'exit':
            break
        elif query == '#':
            current_query = ""
            continue
        else:
            current_query += query

        results = auto_complete.get_best_k_completion(current_query)
        print(f"\nSuggestions: {results}\n")
        print(f"Continue typing or enter '#' to start a new search.")

    print("Goodbye!")


if __name__ == "__main__":
    zip_opener = ZipOpener('dataset.zip')
    data_processor = ProcessData()
    print("Processing data... Please wait.")
    zip_opener.read(data_processor)
    print("Data processed successfully.")
    user_interaction(data_processor.get_data())
