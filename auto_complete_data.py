class AutoCompleteData:
    # completed_sentence: str
    # source_text: str
    # offset: int
    # score: int

    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def __str__(self):
        return f"Completed Sentence: {self.completed_sentence}\n" \
               f"Source Text: {self.source_text}\nOffset: {self.offset}\nScore: {self.score}"

    def __repr__(self):
        return f"AutoCompleteData(completed_sentence='{self.completed_sentence}', source_text='{self.source_text}', offset={self.offset}, score={self.score})"

    def get_completed_sentence(self):
        return self.completed_sentence

    def get_source_text(self):
        return self.source_text

    def get_offset(self):
        return self.offset

    def get_score(self):
        return self.score

    def set_completed_sentence(self, completed_sentence):
        self.completed_sentence = completed_sentence

    def set_source_text(self, source_text):
        self.source_text = source_text

    def set_offset(self, offset):
        self.offset = offset

    def set_score(self, score):
        self.score = score

