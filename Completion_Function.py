import string


def delete_char(sentence: str, ht):
    score = len(sentence) * 2
    valid_sentences = []

    for i in range(len(sentence), -1, -1):
        new_sentence = sentence[:i] + sentence[i + 1:]
        if new_sentence in ht:
            penalty = max(10 - 2 * i, 2)  # Adjusts the score based on the position
            new_score = score - penalty
            valid_sentences.append((new_sentence, new_score))
            if len(valid_sentences) == 5:
                break

    # return the top 5 valid sentences
    return valid_sentences
#####################################################################################
def has_multiple_mismatches(subtext, subtextdict):
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
        if word not in subtextdict.keys():
            mismatches += 1
            if mismatches > 1:  # We don't allow words with an error of more than one letter.
                return True
    return False


def find_mismatched_word_and_index(subtext, subtextdict):
    """
    Finds the first word in the subtext that is not in the subtext dictionary and its starting index.

    Args:
        subtext: The subtext to check.
        subtextdict:  A dictionary containing subtext strings and the mach line.

    Returns:
        A tuple containing the mismatched word and its starting index, or None if no mismatch is found.
    """

    for i, word in enumerate(subtext.split()):
        if word not in subtextdict.keys():
            return word, i
    return None


def generate_possible_replacements(mismatched_word, subtext, subtextdict, end_word_index):
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
    score = (len(subtext)-1) * 2
    alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    possible_words = []

    for i in range(len(mismatched_word), -1, -1):
        for char in alphabet:
            if char == subtext[end_word_index - i]:
                continue

            new_word = subtext[:end_word_index - i] + char + subtext[end_word_index - i + 1:]
            if new_word in subtextdict.keys():
                # Index 0-3 get penalty of -5 to -2 respectively.
                penalty = 1 if (end_word_index - i) > 3 else 5 - (end_word_index - i)
                new_score = score - penalty
                possible_words.append((new_word, new_score))

                if len(possible_words) == 5:
                    break

    return possible_words


def find_most_suitable_lines_by_replace_char(subtext, subtextdict):
    """
    Checks if a single character in the given subtext can be replaced to form a valid word.

    Args:
        subtext: The subtext to check.
        subtextdict:  A dictionary containing subtext strings and the mach line.

    Returns:
        A list of tuples, where each tuple contains a potential replacement and its score.
    """

    if has_multiple_mismatches(subtext, subtextdict):
        return []

    mismatched_word, start_index = find_mismatched_word_and_index(subtext, subtextdict)

    end_word_index = start_index + len(mismatched_word) - 1
    return generate_possible_replacements(mismatched_word, subtext, subtextdict, end_word_index)


def get_best_k_completion(subtext: str, subtextdict: dict):
    """
    Gets the best k completion candidates for the given subtext.

    Args:
        subtext: The subtext to complete.
        subtextdict: A dictionary containing subtext strings and the mach line.

    Returns:
        A list of tuples, where each tuple contains a completion candidate and its score.
    """

    if subtext in subtextdict.keys():
        # If the subtext itself is a valid word, return the five suitable lines
        return [(subtext, subtextdict[subtext][:5])]
    else:
        most_five_suitable_lines = find_most_five_suitable_lines(subtext, subtextdict)
        return




def main():
    subTextDict = {}
    suitableStrings = []
    while(True):
        user_input = input().lower()
        suitableStrings = get_best_k_completion(user_input, subTextDict)


    return 0

main()