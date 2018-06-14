# Problem Set 4B
# Name: Elaheh Ahmadi
# Collaborators: Julia Castiglia, Kristian Georgied
# Time Spent: 10h
# Late Days Used: 0

import string
### HELPER CODE ###


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


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy_valid_words = self.valid_words.copy()
        return copy_valid_words

    def build_shift_dicts(self, shifts):
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
                    shift_dict[j] = lower_alphabet[i+shift-len_alphabet]
                else:
                    shift_dict[j] = lower_alphabet[i+shift]
            for i, j in enumerate(upper_alphabet):
                if i + shift >= len_alphabet:
                    shift_dict[j] = upper_alphabet[i+shift-len_alphabet]
                else:
                    shift_dict[j] = upper_alphabet[i+shift]
            shift_dicts.append(shift_dict)
        return shift_dicts

    def apply_shift(self, shift_dicts):
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
        # Here I iterate over letters in the text. If it was a valid letter I shift it by replacing the letter with the
        # shifted version of it. Otherwise, I just add whatever it was to the coded string.
        new_string = ''
        j = 0
        delta = 1
        for letter in self.message_text:
            if letter in shift_dicts[j].keys():
                new_string += shift_dicts[j][letter]
            else:
                new_string += letter
            j += delta
            delta *= -1
        return new_string


class PlaintextMessage(Message):
    def __init__(self, text, shifts):
        '''
        Initializes a PlaintextMessage object.
        text (string): the message's text
        shifts (list of integers): the list of shifts associated with this message

        A PlaintextMessage object inherits from Message. It has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shifts (list of integers, determined by input shifts)
            self.encryption_dicts (list of dictionaries, built using shifts)
            self.encrypted_message_text (string, encrypted using self.encryption_dict)

        '''
        Message.__init__(self, text)
        self.shifts = shifts
        self.encryption_dicts = self.build_shift_dicts(shifts)
        self.encrypted_message_text = self.apply_shift(self.encryption_dicts)

    def get_shifts(self):
        '''
        Used to safely access self.shifts outside of the class
        
        Returns: self.shifts
        '''
        return self.shifts

    def get_encryption_dicts(self):
        '''
        Used to safely access a copy self.encryption_dicts outside of the class
        
        Returns: a COPY of self.encryption_dicts
        '''
        self.encryption_dicts = self.build_shift_dicts(self.shifts)
        copy_encryption_dicts = self.encryption_dicts.copy()
        return copy_encryption_dicts

    def get_encrypted_message_text(self):
        '''
        Used to safely access self.encrypted_message_text outside of the class
        
        Returns: self.encrypted_message_text
        '''
        copy_encrypted_message_text = self.encrypted_message_text[:]
        return copy_encrypted_message_text

    def change_shifts(self, shifts):
        '''
        Changes self.shifts of the PlaintextMessage, and updates any other 
        attributes that are determined by the shift list.        
        
        shifts (list of length 2): the new shift that should be associated with this message.
        [0 <= shift < 26]

        Returns: nothing
        '''
        self.shifts = shifts
        self.encryption_dicts = self.build_shift_dicts(shifts)
        self.encrypted_message_text = self.apply_shift(self.encryption_dicts)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text
        
        a CiphertextMessage object inherits from Message. It has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
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
        best_shift = [0, 0]
        max_word_count = 0
        # Here I decrypt the string for all the possible shifts and check how many valid word I get. Then I check if
        # decrypting with that specific shift list had more valid words than the last best shift list. At the end of
        # searching I decode the string with the best shift list that I found and return both the shift list and the
        # decoded string
        for i in range(26):
            for j in range(26):
                try_shift = [i, j]
                shift_dicts = self.build_shift_dicts(try_shift)
                decrypted = self.apply_shift(shift_dicts)
                words = decrypted.split(' ')
                count_words = 0
                for word in words:
                    if is_word(self.valid_words, word):
                        count_words += 1
                if count_words > max_word_count:
                    best_shift = try_shift
                    max_word_count = count_words
        final_best = best_shift
        shifted_dicts = self.build_shift_dicts(final_best)
        decrypted_message = self.apply_shift(shifted_dicts)
        return final_best, decrypted_message


def test_plaintext_message():
    '''
    Write two test cases for the PlaintextMessage class here. 
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what 
    case(s) it is testing. 
    '''

#    #### Example test case (PlaintextMessage) ##### 

#    # This test is checking encoding a lowercase string with punctuation in it. 
#    plaintext = PlaintextMessage('hello!', [2,3])
#    print('Expected Output: jhnoq!')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
    # Checking for encoding with spaces, capitals, and punctuations
    print('Testing plaintext_message')
    plaintext_1 = PlaintextMessage('My Name is Ellie!!!!!', [0, 1])
    print('Input: "My Name is Ellie!!!!!" and shift list is [0,1]')
    print('Expected Output: Mz Oane it Flmif!!!!!')
    print('Actual output: ', plaintext_1.get_encrypted_message_text())
    # Checking for encoding all capitals
    plaintext_2 = PlaintextMessage('I LOVE CODE', [10, 25])
    print('Input "I LOVE CODE" and shift list is [10,25]')
    print('Expected Output: S VNFD BYCO')
    print('Actual output: ', plaintext_2.get_encrypted_message_text())


def test_ciphertext_message():
    '''
    Write two test cases for the CiphertextMessage class here. 
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what 
    case(s) it is testing. 
    '''

#    #### Example test case (CiphertextMessage) ##### 
    
#   # This test is checking decoding a lowercase string with punctuation in it.
#    ciphertext = CiphertextMessage('fbjim!')
#    print('Expected Output:', ([2, 3], 'hello!'))
#    print('Actual Output:', ciphertext.decrypt_message())
    # This test is checking for a simple one word all lowercase string.
    print('Testing ciphertext_message')
    ciphertext_1 = CiphertextMessage('fjnf')
    print('Input: "fjnf"')
    print('Expected Output:', ([0,25], 'fine'))
    print('Actual Output:', ciphertext_1.decrypt_message())
    # This test is checking for words with capital and lower and punctuation
    ciphertext_2 = CiphertextMessage('Moqvt Bywvi? Zddmys')
    print('Input: "Moqvt Bywvi? Zddmys"')
    print('Expected Output:', ([21, 16], 'Hello World? Python'))
    print('Actual Output:', ciphertext_2.decrypt_message())


def decode_story():
    '''
    Write your code here to decode the story contained in the file story.txt.
    Hint: use the helper function get_story_string and your CiphertextMessage class.

    Returns: a tuple containing (best_shift, decoded_story)

    '''
    story = get_story_string()
    decoding_stroy = CiphertextMessage(story)
    best_shift, decoded_story = decoding_stroy.decrypt_message()
    return best_shift, decoded_story




if __name__ == '__main__':

    # Uncomment these lines to try running your test cases 
    # test_plaintext_message()
    # test_ciphertext_message()

    # Uncomment these lines to try running decode_story_string()
    best_shift, story = decode_story()
    print("Best shift:", best_shift)
    print("Decoded story: ", story)
    # text = 'hey'
    # shifts = [0,1]
    # msg = Message(text)
    # shift_docs = msg.build_shift_dicts(shifts)
    # result = msg.apply_shift(shift_docs)
    # print(result)
    # c = PlaintextMessage(text,shifts)
    # print(c.get_encrypted_message_text)
