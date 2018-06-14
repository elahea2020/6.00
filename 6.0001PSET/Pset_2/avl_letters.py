import string
def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which
      letters have not yet been guessed.
    '''
    letters_not_guessed = string.ascii_lowercase
    for i in letters_guessed:
        letters_not_guessed = letters_not_guessed.replace(i, '')
    return letters_not_guessed
