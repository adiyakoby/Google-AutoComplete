import string
from auto_complete_data import AutoCompleteData


class AutoComplete:
    def __init__(self, ht):
        self.ht = ht

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

    def addition_score(self, index, max_score):
        return max_score - ([10, 8, 6, 4][index] if index < 4 else 2)

    def character_addition(self, sentence):  # THEE GOOD
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

    #####################################################################################
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

    def find_most_suitable_lines_by_replace_char(self, subtext):
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

    #####################################################################################################
    def find_most_five_suitable_lines(self, subtext):
        list_of_suitable_by_replace_char = self.find_most_suitable_lines_by_replace_char(subtext)
        list_of_suitable_by_delete_char = self.delete_char(subtext)
        list_of_suitable_by_add_char = self.character_addition(subtext)

        combining_list = list_of_suitable_by_replace_char + list_of_suitable_by_add_char \
                         + list_of_suitable_by_replace_char

        combining_list.sort(reverse=True, key=lambda item: item[1])
        if len(combining_list) > 5:
            return combining_list[:5]
        else:
            return combining_list

    def create_five_auto_complete_data_objects(self, most_five_suitable_lines):
        if len(most_five_suitable_lines) == 0:
            return []

        auto_complete_object = []
        for i in range(5):
            line_in_file = self.ht[most_five_suitable_lines[i][0]][0]
            name_of_source_file = self.ht[most_five_suitable_lines[i][0]][2]
            offset = self.ht[most_five_suitable_lines[i][0]][1]
            score = most_five_suitable_lines[i][1]
            auto_complete_object.append(
                AutoCompleteData(line_in_file, name_of_source_file, offset, score))
        return auto_complete_object

    ##############################################################################################

    def get_best_k_completion(self, subtext: str):
        """
        Gets the best k completion candidates for the given subtext.

        Args:
            subtext: The subtext to complete.
            subtextdict: A dictionary containing subtext strings and the mach line.

        Returns:
            A list of tuples, where each tuple contains a completion candidate and its score.
        """

        if subtext in self.ht:
            # If the subtext itself is a valid word, return the five suitable lines
            return [(subtext, self.ht[subtext][:5])]
        else:
            most_five_suitable_lines = self.find_most_five_suitable_lines(subtext)
            autoCompleteData_list = self.create_five_auto_complete_data_objects(most_five_suitable_lines)

            return autoCompleteData_list
