from auto_complete import AutoComplete
from zip_opener import ZipOpener
from process_data import ProcessData


class AutoCompleteApp:
    def __init__(self):
        pass

    def start(self):
        zip_opener = ZipOpener('dataset.zip')
        data_processor = ProcessData()
        print("Processing data... Please wait.")
        zip_opener.read(data_processor)
        print("Data processed successfully.")

        auto_complete = AutoComplete(data_processor.get_data())
        current_query = []

        while True:
            query = input(f"{' '.join(current_query)} ")
            if query == 'exit':
                break
            elif query == '#':
                current_query = []
                continue
            else:
                current_query.extend(query.strip().split())

            results = auto_complete.get_best_k_completion(' '.join(current_query))
            for i in range(5):
                print(i+1, results[i])
