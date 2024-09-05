import os
import pickle

from auto_complete import AutoComplete
from zip_opener import ZipOpener
from process_data import ProcessData


class AutoCompleteApp:
    def __init__(self):
        pass

    def save_data_to_file(self, data_processor):
        print("Saving data to a file... Please wait.")
        with open("data.pkl", "wb") as file:
            pickle.dump(data_processor.get_data(), file)
        print("Saved data successfully.")

    def load_data_from_file(self, data_processor):
        print("Loading processed data from file... Please wait.")
        with open("data.pkl", "rb") as file:
            data_processor.set_data(pickle.load(file))

    def user_interaction(self, data_processor):
        auto_complete = AutoComplete(data_processor.get_data())
        current_query = ""

        print("Hello! You can start searching:")

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

            # Ensure printing only 5 available results
            for i in range(min(5, len(results))):
                print(f"{i + 1}) {results[i][0]} (Line: {results[i][1]}, Filename: {results[i][2]})")

        print("Goodbye!")

    def start(self):
        zip_opener = ZipOpener('dataset.zip')
        data_processor = ProcessData()

        # Consistent file name for checking and loading/saving
        if not os.path.exists("data.pkl"):
            print("Processing data... Please wait.")
            zip_opener.read(data_processor)
            self.save_data_to_file(data_processor)
        else:
            self.load_data_from_file(data_processor)

        print("Data processed successfully.\n\n")

        self.user_interaction(data_processor)
