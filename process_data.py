import itertools
from collections import defaultdict
from typing import List
import re


class ProcessData:
    def __init__(self):
        self.__data = defaultdict(list)

    def get_all_substrings(self, s: str) -> List[str]:
        sub_strings = [s[i:j] for i, j in itertools.combinations(range(len(s) + 1), 2)]
        return sub_strings

    def remove_punctuation(self, line):
        return " ".join(re.sub(r'[^\w\s]', '', line.lower()).split())

    def process(self, lines: List, filename: str):
        for i, line in enumerate(lines, 1):
            clean_line = self.remove_punctuation(line.strip())

            if clean_line:
                substrings = self.get_all_substrings(clean_line)
                for substring in substrings:
                    self.__data[substring].append({"content": line, "index": i, "filename": filename})

    def get_data(self):
        return self.__data


if __name__ == "__main__":
    pass
