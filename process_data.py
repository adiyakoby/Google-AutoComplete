import itertools
from collections import defaultdict
from typing import List
import re


class ProcessData:
    def __init__(self):
        self.__data = defaultdict(list)

    def get_all_substrings(self, s: str, sub_strings: List[str]):
        sub_strings = [s[i:j] for i, j in itertools.combinations(range(len(s) + 1), 2)]


    def remove_punctuation(self, line):
        return " ".join(re.sub(r'[^\w\s]', '', line.lower()).split())

    def process(self, lines: List, filename: str):
        sub_strings = []
        for i in range(len(lines)):
            clean_line = self.remove_punctuation(lines[i].strip())

            if clean_line:
                self.get_all_substrings(clean_line, sub_strings)
                for substring in sub_strings:
                    self.__data[substring].append({"content": lines[i], "index": i+1, "filename": filename})

    def get_data(self):
        return self.__data


if __name__ == "__main__":
    pass
