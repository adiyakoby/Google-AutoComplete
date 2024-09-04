import itertools
from collections import defaultdict
from typing import List
import re


class ProcessData:
    """
    A class to process text data by generating all possible substrings of
    each line, removing punctuation, and storing the processed data.

    Attributes:
    -----------
    __data : defaultdict
        A dictionary that stores substrings as keys and a list of dictionaries
        containing the original content, its index in the input, and the filename.

    Methods:
    --------
    get_all_substrings(s: str, sub_strings: List[str]):
        Generates all possible substrings from a given string and appends them to a list.

    remove_punctuation(line: str) -> str:
        Removes punctuation from a given string, converts it to lowercase, and returns the cleaned string.

    process(lines: List[str], filename: str):
        Processes a list of lines by cleaning them, generating all possible substrings,
        and storing the data in the class attribute __data.

    get_data() -> defaultdict:
        Returns the processed data stored in the __data attribute.
    """

    def __init__(self):
        """
        Initializes the ProcessData class with an empty defaultdict to store the processed data.
        """
        self.__data = defaultdict(list)
        self.__word_re = re.compile(r'\b[a-z]+\b')

    def get_all_substrings(self, line: str):
        """
        Generates all possible substrings from a given string `s` and appends
        them to the `sub_strings` list.

        Parameters:
        -----------
        s : str
            The input string from which substrings are generated.
        sub_strings : List[str]
            A list to store the generated substrings.
        """
        sub_strings = []
        words = line.split()
        for i in range(len(words)):
            for j in range(2, len(words[i])+1):
                sub_strings.append(words[i][0:j])
            if i > 1:
                sub_strings.append(words[i-1] + words[i][:1])
                sub_strings.append(words[i - 1][1:] + words[i][:1])
            sub_strings.append(words[i][1:])
        return sub_strings






    def remove_punctuation(self, line):
        """
        Removes punctuation from a given string, converts it to lowercase, and
        returns the cleaned string.

        Parameters:
        -----------
        line : str
            The input string to be cleaned.

        Returns:
        --------
        str
            The cleaned string without punctuation, converted to lowercase.
        """
        return ' '.join(self.__word_re.findall(line.lower()))


    def process(self, lines: List, filename: str):
        """
        Processes a list of lines by cleaning each line, generating all possible
        substrings, and storing the data in the class attribute __data.

        Parameters:
        -----------
        lines : List[str]
            A list of strings (lines) to be processed.
        filename : str
            The name of the file where the lines originated from.
        """

        for i in range(len(lines)):
            clean_line = self.remove_punctuation(lines[i].strip())

            if clean_line:
                sub_string = self.get_all_substrings(clean_line)
                for substring in sub_string:
                    self.__data[substring].append((lines[i], i+1,  filename))


    def get_data(self):
        """
        Returns the processed data stored in the __data attribute.

        Returns:
        --------
        defaultdict
            A dictionary where keys are substrings and values are lists of dictionaries
            containing the original content, its index in the input, and the filename.
        """
        return self.__data


if __name__ == "__main__":
    pass
