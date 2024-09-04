import zipfile
from process_data import ProcessData
from typing import Dict, List


class ZipOpener:
    """
    A class to handle operations on a zip file containing text files.
    """

    def __init__(self, zip_file: str):
        self.zip_file = zip_file
        self.zip = zipfile.ZipFile(zip_file, 'r')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zip.close()

    def read(self, processData: ProcessData) -> None:
        """
        Reads and processes all '.txt' files from the zip archive.

        This method iterates over all the files in the zip archive. For each
        '.txt' file, it reads the content, splits it into rows, and processes
        the rows using the provided ProcessData instance.

        Parameters:
        -----------
        processData : ProcessData
            An instance of the ProcessData class where the processed data
            will be stored.
        """
        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir() and file_info.filename.endswith('.txt'):
                    with zip_ref.open(file_info) as file:
                        file_content = file.read().decode('utf-8')
                        rows = file_content.splitlines()
                        processData.process(rows, file_info.filename)
