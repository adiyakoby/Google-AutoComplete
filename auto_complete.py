import string
from auto_complete_data import AutoCompleteData
import random

class AutoComplete:
    def __init__(self, ht):
        self.ht = ht

    """ good """
    def create_auto_complete(self, lines):
        responses = []
        for i in range(len(lines)):
            responses.append(
                AutoCompleteData(
                    lines[i][0],  # completed_sentence
                    lines[i][2],  # source_text
                    lines[i][1]   # offset
                ))
        return responses

    """ good """
    def delete_char(self, sentence: str):
        score = (len(sentence) - 1) * 2
        valid_sentences = []

        for i in range(len(sentence), -1, -1):
            new_sentence = sentence[:i] + sentence[i + 1:]
            if new_sentence in self.ht:
                penalty = max(10 - 2 * i, 2)  # Adjusts the score based on the position
                new_score = score - penalty
                valid_sentences.append((new_sentence, new_score))
                if len(valid_sentences) == 5:
                    break

        # return the top 5 valid sentences
        return valid_sentences

    """ good """
    def addition_score(self, index, max_score):
        return max_score - ([10, 8, 6, 4][index] if index < 4 else 2)

    """ good """
    def add_char(self, sentence):  # THEE GOOD
        n = len(sentence) - 1
        res = []
        for char in range(ord('a'), ord('z') + 1):
            for i in range(n, -1, -1):
                cur_word = sentence[:i] + chr(char) + sentence[i:]
                if cur_word in self.ht:
                    res.append((cur_word, self.addition_score(i, n * 2)))
                if len(res) == 5:
                    break
        return res


    def has_multiple_mismatches(self, subtext):
        """
        Checks if the subtext contains more than one word that is not in the subtext dictionary.

        Args:
            subtext: The subtext to check.
            subtextdict:  A dictionary containing subtext strings and the mach line.

        Returns:
            True if there are multiple mismatches, False otherwise.
        """

        mismatches = 0
        for word in subtext.split():
            if word not in self.ht:
                mismatches += 1
                if mismatches > 1:  # We don't allow words with an error of more than one letter.
                    return True
        return False

    def find_mismatched_word_and_index(self, subtext):
        """
        Finds the first word in the subtext that is not in the subtext dictionary and its starting index.

        Args:
            subtext: The subtext to check.
            subtextdict:  A dictionary containing subtext strings and the mach line.

        Returns:
            A tuple containing the mismatched word and its starting index, or None if no mismatch is found.
        """

        for i, word in enumerate(subtext.split()):
            if word not in self.ht:
                return word, i
        return None

    def generate_possible_replacements(self, mismatched_word, subtext, end_word_index):
        """
        Generates possible replacements for the mismatched word by trying different characters at each position.

        Args:
            mismatched_word: The mismatched word.
            subtext: The original subtext.
            subtextdict:  A dictionary containing subtext strings and the mach line.
            end_word_index: The ending index of the mismatched word in the subtext.

        Returns:
            A list of tuples containing possible replacements and their scores.
        """
        # 2 points fot each suitable char.
        score = (len(subtext) - 1) * 2
        alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
        possible_words = []

        for i in range(len(mismatched_word), -1, -1):
            for char in alphabet:
                if char == subtext[end_word_index - i]:
                    continue

                new_word = subtext[:end_word_index - i] + char + subtext[end_word_index - i + 1:]
                if new_word in self.ht:
                    # Index 0-3 get penalty of -5 to -2 respectively.
                    penalty = 1 if (end_word_index - i) > 3 else 5 - (end_word_index - i)
                    new_score = score - penalty
                    possible_words.append((new_word, new_score))

                    if len(possible_words) == 5:
                        break

        return possible_words

    def replace_char(self, subtext):
        """
        Checks if a single character in the given subtext can be replaced to form a valid word.

        Args:
            subtext: The subtext to check.
            subtextdict:  A dictionary containing subtext strings and the mach line.

        Returns:
            A list of tuples, where each tuple contains a potential replacement and its score.
        """

        if self.has_multiple_mismatches(subtext):
            return []

        mismatched_word, start_index = self.find_mismatched_word_and_index(subtext)

        end_word_index = start_index + len(mismatched_word) - 1
        return self.generate_possible_replacements(mismatched_word, subtext, end_word_index)



    def get_best_completions(self, subtext):

        combining_list = self.replace_char(subtext) + self.delete_char(subtext) + self.add_char(subtext)
        higher = 0
        found_key = ""
        for combination in combining_list:
            if combination[1] > higher:
                higher = combination[1]
                found_key = combination[0]

        return found_key

    def get_words_completions(self, sentence):
        words = sentence.split()

        lines = set()

        for word in words:
            if word in self.ht:
                if len(lines) == 0:
                    lines = set(self.ht[word])
                else:
                    lines.intersection_update(self.ht[word])
            else:
                new_word = self.get_best_completions(word)
                if new_word:
                    lines.intersection_update(self.ht[new_word])
                else:
                    return []

        lines_list = list(lines)

        if len(lines_list) > 5:
            random_elements = random.sample(lines_list, 5)
            return random_elements
        else:
            return lines_list









    """ good """
    def get_best_k_completion(self, user_input: str, k = 5):
        """
        Gets the best k completion candidates for the given subtext.

        Args:
            :param user_input:  The subtext to complete.
            :param k:  amount of lines to retrieve.

        Returns:
            A list of tuples, where each tuple contains a completion candidate and its score.

        """
        if user_input in self.ht:
            return self.create_auto_complete(self.ht[user_input][:k])
        else:
            return self.create_auto_complete(self.ht[self.get_best_completions(user_input)][:k])


