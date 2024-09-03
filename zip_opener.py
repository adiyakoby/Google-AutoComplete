import zipfile


class ZipOpener:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.zip = zipfile.ZipFile(zip_file, 'r')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zip.close()

    def read(self):
        """
        Function to read all .txt files in a zip archive and process each list of rows.

        Parameters:
        zip_file_path (str): Path to the zip file.

        Returns:
        None
        """

        processData = ProcessData()

        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir() and file_info.filename.endswith('.txt'):
                    with zip_ref.open(file_info) as file:
                        file_content = file.read().decode('utf-8')
                        rows = file_content.splitlines()  # Split the content into a list of rows
                        processData.process(rows, file_info.filename)

        return processData.get_data()
