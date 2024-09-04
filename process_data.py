import itertools
from collections import defaultdict
from typing import List
import re


class ProcessData:
    def __init__(self):
        self.__data = defaultdict(list)

    def get_all_substrings(self, s: str, sub_strings: List[str]):
        n = len(sub_strings)
        for i in range(n):
            for j in range(i + 1, n+1):
                sub_strings.append(s[i:j])

    def remove_punctuation(self, line):
        return " ".join(re.sub(r'[^\w\s]', '', line.lower()).split())

    def process(self, lines: List, filename: str):
        for i in range(len(lines)):
            sub_strings = []
            clean_line = self.remove_punctuation(lines[i].strip())

            if clean_line:
                self.get_all_substrings(clean_line, sub_strings)
                for substring in sub_strings:
                    self.__data[substring].append({"content": lines[i], "index": i+1, "filename": filename})

    def get_data(self):
        return self.__data


if __name__ == "__main__":
    pass
