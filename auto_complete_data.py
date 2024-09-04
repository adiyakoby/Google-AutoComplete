
class AutoCompleteData:

    def __init__(self, completed_sentence, source_text, offset, score):
        self.__completed_sentence = completed_sentence
        self.__source_text = source_text
        self.__offset = offset
        self.__score = score

    def __str__(self):
        return f" {self.__completed_sentence} ({self.__source_text} {self.__offset})"
