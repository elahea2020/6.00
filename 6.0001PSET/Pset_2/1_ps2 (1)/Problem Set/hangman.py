# Problem Set 2, hangman.py
# Name: Elaheh Ahmadi
# Collaborators: N/A
# Time spent: Whole Saturday

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    for i in secret_word:
        if i not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters and underscores (_) that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_word_size = len(secret_word)
    guessed_words = '_'*secret_word_size
    for i,j in enumerate(secret_word): 
        if j in letters_guessed: 
            guessed_words = guessed_words[:i]+ guessed_words[i:i+1].replace('_',j)+guessed_words[i+1:]
    return guessed_words


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed.
    '''
    letters_not_guessed = string.ascii_lowercase
    for i in letters_guessed:
        letters_not_guessed = letters_not_guessed.replace(i,'')
    return letters_not_guessed


def calc_score(guess_remained, secret_word): 
    uniques = []
    for i in secret_word: 
        if i not in uniques: 
           uniques.append(i)
    score = guess_remained + len(uniques) * len(secret_word)
    return score    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 10 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # print('This is the Hangman game. In each step you need to guess a letter and\
    #       if your letter was in our word, good for you, and if not you have few other \
    #       guesses left that you can use and hopefully win.')
    length_of_secret_word = len(secret_word)
    guess_remained = 10
    game = True
    letters_guessed = []
    letters_not_guessed = get_available_letters(letters_guessed)
    print('Welcome to hangman')
    print('The secret word is %d letters long'%length_of_secret_word)
    print('------')
    # print('The word that you should guess has %d letters and you have %d guesses remained'%(length_of_secret_word, guess_remained))
    # print('Here the game begins.')
    while game:
        if guess_remained > 1:
            print('You have %d guesses remaining'%guess_remained)
        else:
            print('You have %d guess remaining' % guess_remained)
        print('Available letters: %s'%letters_not_guessed)
        letter = input('Please guess a letter:')
        if not letter.isalpha():
            print('This is not a valid input.')
            print('------')
            continue
        if letter not in letters_not_guessed:
            print('The letter has already been guessed before')
            print('------')
            continue
        letter.lower()
        letters_guessed.append(letter)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if letter in secret_word: 
            print('Good guess: %s'%guessed_word)
            print('------')
        else:
            print('Oops! That letter is not in my word: %s'%guessed_word)
            if letter in 'aeiou':
                guess_remained -= 2
            else: 
                guess_remained -= 1
            print('------')
        if is_word_guessed(secret_word, letters_guessed):
            print('Good job you won this game!')
            score = calc_score(guess_remained, secret_word)
            print('Your score is %d'%score)
            game = False
            break
        if guess_remained == 0:
            # print('The secret word was: %s' % secret_word)
            # print('Game Over!')
            print('Sorry, you ran out of guesses. The word was %s'%secret_word)
            game = False
            break
        letters_not_guessed = get_available_letters(letters_guessed)

    return game



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def helper_guess(secret_word, letters_not_guessed):
    choose_from = []
    for i in secret_word:
        if i in letters_not_guessed and i not in choose_from:
            choose_from.append(i)
    return choose_from



def hangman_with_help(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 10 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol #, you should reveal to the user one of the 
      letters missing from the word at the cost of 2 guesses. If the user does 
      not have 2 guesses remaining, print a warning message. Otherwise, add 
      this letter to their guessed word and continue playing normally.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    length_of_secret_word = len(secret_word)
    guess_remained = 10
    game = True
    letters_guessed = []
    letters_not_guessed = get_available_letters(letters_guessed)
    print('Welcome to hangman')
    print('I am thinking of a word that is %d letters long'%length_of_secret_word)
    print('------')
    # print('The word that you should guess has %d letters and you have %d guesses remained'%(length_of_secret_word, guess_remained))
    # print('Here the game begins.')
    while game:
        if guess_remained > 1:
            print('You have %d guesses left'%guess_remained)
        else:
            print('You have %d guess left' % guess_remained)
        print('Available letters: %s'%letters_not_guessed)
        letter = input('Please guess a letter:')
        if letter == '#':
            if guess_remained <=2:
                print('Oops! Not enough guesses left: %s'%guessed_word)
                print('------')
                continue
            choose_from = helper_guess(secret_word, letters_not_guessed)
            new = random.randint(0,len(choose_from)-1)
            exposed_letter = choose_from[new]
            letters_guessed.append(exposed_letter)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            guess_remained -= 2
            print('Letter revealed: %c'%exposed_letter)
            print(guessed_word)
            print('------')
            continue
        elif not letter.isalpha():
            print('This is not a valid input.')
            print('------')
            continue
        if letter not in letters_not_guessed:
            print('The letter has already been guessed before')
            print('------')
            continue
        letter.lower()
        letters_guessed.append(letter)
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        if letter in secret_word:
            print('Good guess: %s'%guessed_word)
            print('------')
        else:
            print('Oops! That letter is not in my word: %s'%guessed_word)
            print('------')
            if letter in 'aeiou':
                guess_remained -= 2
            else:
                guess_remained -= 1
        if is_word_guessed(secret_word, letters_guessed):
            print('Good job you won this game!')
            score = calc_score(guess_remained, secret_word)
            print('Your score is %d'%score)
            game = False
            break
        if guess_remained == 0:
            # print('The secret word was: %s'%secret_word)
            # print('Game Over!')
            print('Sorry, you ran out of guesses. The word was %s' % secret_word)
            game = False
            break
        letters_not_guessed = get_available_letters(letters_guessed)

    pass



# When you've completed your hangman_with_help function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # # # print(secret_word)
    # secret_word = 'hi'
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    # secret_word = 'hi'
    # hangman_with_help(secret_word)
