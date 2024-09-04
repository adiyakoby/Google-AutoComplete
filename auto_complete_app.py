import os
import pickle

from auto_complete import AutoComplete
from zip_opener import ZipOpener
from process_data import ProcessData


class AutoCompleteApp:
    def __init__(self):
        pass

    def user_interaction(self, data_processor):
        auto_complete = AutoComplete(data_processor.get_data())
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

            results = auto_complete.get_words_completions(current_query.strip().lower())

            # Ensure you are printing only available results
            for i in range(min(5, len(results))):
                print(i + 1, results[i])

    def start(self):
        zip_opener = ZipOpener('dataset.zip')
        data_processor = ProcessData()

        # Consistent file name for checking and loading/saving
        if not os.path.exists("data.pkl"):
            print("Processing data... Please wait.")
            zip_opener.read(data_processor)
            print("Saving data to a file... Please wait.")
            with open("data.pkl", "wb") as file:
                pickle.dump(data_processor.get_data(), file)
            print("Saved data successfully.")
        else:
            print("Loading processed data from file... Please wait.")
            with open("data.pkl", "rb") as file:
                data_processor.set_data(pickle.load(file))

        print("Data processed successfully.")

        self.user_interaction(data_processor)
