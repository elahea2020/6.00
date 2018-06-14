import string


def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    # >>> is_word(word_list, 'bat') returns
    True
    # >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def build_shift_dicts(shifts):
    '''
    Creates a list of dictionaries; each dictionary can be used to apply a
    cipher to a letter.
    The dictionary maps every uppercase and lowercase letter to a
    character shifted down the alphabet by the input shift. By shifted down, we mean
    that if 'a' is shifted down by 2, the result is 'c.'

    The dictionary should have 52 keys of all the uppercase letters and
    all the lowercase letters only.

    shifts (list of integer): the amount by which to shift every letter of the
    alphabet. 0 <= shift < 26

    Returns: a list of dictionaries mapping letter (string) to
             another letter (string).
    '''
    lower_alphabet = string.ascii_lowercase
    upper_alphabet = string.ascii_uppercase
    len_alphabet = len(lower_alphabet)
    shift_dicts = []
    # In this for loop we iterate over the shifts and assign each alphabet to the shifted version one
    for shift in shifts:
        shift_dict = {}
        for i, j in enumerate(lower_alphabet):
            # We should be aware that i+shift might be higher than the length of the alphabet string so we have
            # to count the rest from the beginning of the alphabet string
            if i + shift >= len_alphabet:
                shift_dict[j] = lower_alphabet[i + shift - len_alphabet]
            else:
                shift_dict[j] = lower_alphabet[i + shift]
        for i, j in enumerate(upper_alphabet):
            if i + shift >= len_alphabet:
                shift_dict[j] = upper_alphabet[i + shift - len_alphabet]
            else:
                shift_dict[j] = upper_alphabet[i + shift]
        shift_dicts.append(shift_dict)
    return shift_dicts


def apply_shift(text, shift_dicts):
    '''
    Applies the Caesar Cipher to self.message_text with letter shifts
    specified in shift_dict. Creates a new string that is self.message_text,
    shifted down the alphabet by some number of characters, determined by
    the shift value that shift_dict was built with.

    shift_dict: list of dictionaries; each dictionary with 52 keys, mapping
        lowercase and uppercase letters to their new letters
        (as built by build_shift_dict)

    Returns: the message text (string) with every letter shifted using the
        input shift_dicts
    '''
    new_string = ''
    j = 0
    delta = 1
    for word in text:
        if word in shift_dicts[j].keys():
            new_string += shift_dicts[j][word]
        else:
            new_string += word
        j += delta
        delta *= -1
    return new_string


def decrypt_message(text):
    '''
    Decrypts self.message_text by trying every possible combination of shift
    values and finding the "best" one.
    We will define "best" as the list of shifts that creates the maximum number
    of valid English words when we use apply_shift(shifts)on the message text.
    If [a, b] are the original shift values used to encrypt the message, then we
    would expect [(26 - a), (26 - b)] to be the best shift values for
    decrypting it.

    Note: if multiple lists of shifts are equally good, such that they all create
    the maximum number of valid words, you may choose any of those lists
    (and their corresponding decrypted messages) to return.

    Returns: a tuple of the best shift value list used to decrypt the message
    and the decrypted message text using that shift value
    '''
    best_shift = (0, 0)
    max_word_count = 0
    file_name = 'words.txt'
    valid_words = load_words(file_name)
    for i in range(26):
        for j in range(26):
            try_shift = (i, j)
            shift_dicts = build_shift_dicts(try_shift)
            decrypted = apply_shift(text, shift_dicts)
            words = decrypted.split(' ')
            count_words = 0
            for word in words:
                if is_word(valid_words, word):
                    count_words += 1
            if count_words > max_word_count:
                best_shift = try_shift
                max_word_count = count_words
    final_best = best_shift
    shifted_dicts = build_shift_dicts(final_best)
    decrypted_message = apply_shift(text, shifted_dicts)
    return final_best, decrypted_message
shift_dict = build_shift_dicts([5,10])
print(shift_dict[0])
print(shift_dict[1])
print(apply_shift('Hello World? Python',shift_dict))
print(decrypt_message('Moqvt Bywvi? Zddmys!'))
