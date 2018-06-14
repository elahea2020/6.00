# for running unit tests on 6.00/6.0001/6.0002 student code 

import sys
import unittest
import os
import string
from unittest.mock import patch
from unittest import TestCase
import re
import random
import hangman as student

#pulled from http://stackoverflow.com/questions/20567497/overwrite-built-in-function
outputstr=""
class MyStream(object):
    def __init__(self, target):
        self.target = target

    def write(self, s):
        global outputstr
        outputstr+=s
        #self.target.write(s)
        return s
    def flush(self):
        pass
sys.stdout = MyStream(sys.stdout)


input_string = (letter for letter in ["h", "e", "i"])
def make_input(self):
    return next(input_string)

def output_to_file(test_case_name, word_to_guess, guessed_letters, student_output, correct_output):
    with open('run_game_test_results.txt', 'a+') as f:
        f.write("=============================================================\n")
        f.write("RESULTS FOR TEST CASE: %s\n"%test_case_name)
        f.write("WORD USED IN TEST: %s\n"%word_to_guess)
        f.write("GUESSED LETTERS IN ORDER OF GUESS: %s\n"%guessed_letters)
        f.write('************************\n')
        f.write("YOUR OUTPUT:\n")
        f.write('************************\n')
        f.write(student_output+'\n')
        f.write('************************\n')
        f.write("POSSIBLE CORRECT OUTPUT:\n")
        f.write('************************\n')
        f.write(correct_output+'\n')
        f.write("=============================================================\n\n\n")

def compare_results(expected, actual):
    '''
    Used for comparing equality of student answers with staff answers
    '''
    def almost_equal(x,y):
        if x == y or x.replace(' ', '') == y.replace(' ',''):
            return True
        return False

    exp = expected.strip()
    act = actual.strip()
    return almost_equal(exp, act)


# A class that inherits from unittest.TestCase, where each function
# is a test you want to run on the student's code. For a full description
# plus a list of all the possible assert methods you can use, see the
# documentation: https://docs.python.org/3/library/unittest.html#unittest.TestCase 
class TestPS2(unittest.TestCase):

    # TODO Add HangmanOracle tests

    def test_is_word_guessed(self):
        self.assertTrue(student.is_word_guessed('face', ['f','c','a','e']))
        self.assertFalse(student.is_word_guessed('moves', ['o','c','a','v','e']))

    def test_is_word_guessed_repeated_letters(self):
        self.assertTrue(student.is_word_guessed('bass', ['a','s','b','e']),
            "Failed with repeated letters")
        self.assertFalse(student.is_word_guessed('rare', ['f','t','r','e']),
            "Failed with repeated letters")
            
    def test_is_word_guessed_empty_string(self):
        self.assertTrue(student.is_word_guessed('', ['f','c','y','e']), 
            "Failed with the empty string")
            
    def test_is_word_guessed_empty_list(self):
        self.assertFalse(student.is_word_guessed('code', []),
            "Failed with the empty list")

    def test_get_guessed_word(self):
        self.assertTrue(compare_results(student.get_guessed_word('face', ['f','c','a','e']), 'face'))
        self.assertTrue(compare_results(student.get_guessed_word('moves', ['o','c','a','v','e']), '_ove_'))

    def test_get_guessed_word_repeated_letters(self):
        self.assertTrue(compare_results(student.get_guessed_word('bass', ['a','s','b','e']), 'bass'),
            "Failed with repeated letters")
        self.assertTrue(compare_results(student.get_guessed_word('rare', ['f','t','r','e']), 'r_re'),
            "Failed with repeated letters")
            
    def test_get_guessed_word_empty_string(self):
        self.assertTrue(compare_results(student.get_guessed_word('', ['f','c','y','e']), ''),
            "Failed with the empty string")
    
    def test_get_guessed_word_empty_list(self):
        self.assertTrue(compare_results(student.get_guessed_word('code', []),'____'),
            "Failed with the empty list")
        
    def test_get_available_letters(self):
        self.assertEqual(student.get_available_letters(['a','b','c','d']), 'efghijklmnopqrstuvwxyz')
        self.assertEqual(student.get_available_letters(['z','p','x','b', 'b']), 'acdefghijklmnoqrstuvwy')
        self.assertEqual(student.get_available_letters(['a','u','i','o','w']), 'bcdefghjklmnpqrstvxyz')

    def test_get_available_letters_empty_string(self):
        self.assertEqual(student.get_available_letters(list(string.ascii_lowercase)), '',
            "Failed to return the empty string")
    
    def test_get_available_letters_empty_list(self):
        self.assertEqual(student.get_available_letters([]), 'abcdefghijklmnopqrstuvwxyz',
            "Failed with the empty list")


    def test_play_game_short(self):
        correct='''Welcome to hangman!
The secret word is 2 letters long
You have 4 warnings left
--------------
You have 10 guesses remaining
Available Letters: abcdefghijklmnopqrstuvwxyz
Good guess!: h_
--------------
You have 10 guesses remaining
Available Letters: abcdefgijklmnopqrstuvwxyz
Sorry! That letter wasn't in the secret word: h_
--------------
You have 8 guesses remaining
Available Letters: abcdfgijklmnopqrstuvwxyz
Good guess!: hi
-------
Congrats you won!
Your total score for this game is: 12'''
        with unittest.mock.patch('builtins.input',  make_input):
            threw_exception =  False
            try:
                student.hangman("hi")
            except:
                threw_exception = True
            global outputstr
            student_output = outputstr[:]
            lines = re.split('\-+',outputstr)
            outputstr =""
            try:
                self.assertFalse(threw_exception)
                if len(lines) > 4:
                    self.assertTrue("h_" in lines[1])
                    self.assertTrue("10 guesses" in lines[2])
                    self.assertTrue("h_" in lines[2])
                    self.assertTrue("8 guesses" in lines[3])
                    self.assertTrue("hi" in lines[3])
                    self.assertTrue("score" in lines[4])
                    self.assertTrue("12" in lines[4])
                else:
                    self.assertTrue(False)
            except Exception as e:
                output_to_file('test_play_game_short', 'hi', ["h", "e", "i"], student_output, correct)
                raise(e)
    def test_play_game_short_fail(self):
        correct='''Welcome to hangman!
The secret word is 2 letters long
--------------
You have 10 guesses remaining
Available Letters: abcdefghijklmnopqrstuvwxyz
Sorry! That letter wasn't in the secret word: __
--------------
You have 9 guesses remaining
Available Letters: abcdefghijklmopqrstuvwxyz
Sorry! That letter wasn't in the secret word: __
--------------
You have 7 guesses remaining
Available Letters: abcdfghijklmopqrstuvwxyz
Good guess!: _i
--------------
You have 7 guesses remaining
Available Letters: abcdfghjklmopqrstuvwxyz
Sorry! That letter wasn't in the secret word: _i
--------------
You have 6 guesses remaining
Available Letters: abcdfghjklopqrstuvwxyz
Sorry! That letter wasn't in the secret word: _i
--------------
You have 4 guesses remaining
Available Letters: abcdfghjklopqrstvwxyz
Sorry! That letter wasn't in the secret word: _i
--------------
You have 3 guesses remaining
Available Letters: abcdfghjlopqrstvwxyz
Sorry! That letter wasn't in the secret word: _i
--------------
You have 2 guesses remaining
Available Letters: abcdfghjopqrstvwxyz
Sorry! That letter wasn't in the secret word: _i
--------------
You have 1 guess remaining
Available Letters: abcdfghjoqrstvwxyz
Sorry! That letter wasn't in the secret word: _i
-------
Sorry, you ran out of guesses. The word was hi'''
        global input_string
        computer_guesses = ["n", "e", "i", "m","u","k", "l", "p", "s"]
        input_string = (letter for letter in computer_guesses)
        with unittest.mock.patch('builtins.input',  make_input):
            threw_exception =  False
            try:
                student.hangman("hi")
            except:
                threw_exception = True
            global outputstr
            lines = re.split('\-+',outputstr)
            student_output = outputstr[:]
            outputstr =""
            try:
                self.assertFalse(threw_exception)
                if len(lines) > 8:
                    self.assertTrue("10 guesses" in lines[1])
                    self.assertTrue("__" in lines[1])
                    self.assertTrue("9 guesses" in lines[2])
                    self.assertTrue("__" in lines[2])
                    self.assertTrue("7 guesses" in lines[3])
                    self.assertTrue("_i" in lines[3])
                    self.assertTrue("7 guesses" in lines[4])
                    self.assertTrue("_i" in lines[4])
                    self.assertTrue("6 guesses" in lines[5])
                    self.assertTrue("_i" in lines[5])
                    self.assertTrue("4 guesses" in lines[6])
                    self.assertTrue("_i" in lines[6])
                    self.assertTrue("3 guesses" in lines[7])
                    self.assertTrue("_i" in lines[7])
                    self.assertTrue("2 guesses" in lines[8])
                    self.assertTrue("_i" in lines[8])
                    self.assertTrue("1 guess" in lines[9])
                    self.assertTrue("_i" in lines[9])
                    self.assertTrue("abcdfghjoqrstvwxyz" in lines[9])
                    self.assertTrue("hi" in lines[10])
    
                else:
                    self.assertTrue(False)
            except Exception as e:
                output_to_file('test_play_game_short_fail', 'hi', computer_guesses, student_output, correct)
                raise(e)
            
    def test_play_game_wildcard(self):
        correct = '''Welcome to hangman!
The secret word contains 8 letters
------
You currently have 10 guesses left
Available letters: abcdefghijklmnopqrstuvwxyz
Please guess a letter: k
Sorry, that letter wasn't in the secret word: ________
------
You currently have 9 guesses left
Available letters: abcdefghijlmnopqrstuvwxyz
Please guess a letter: w
Good guess! w_______
------
You currently have 9 guesses left
Available letters: abcdefghijlmnopqrstuvxyz
Please guess a letter: i
Good guess! wi______
------
You currently have 9 guesses left
Available letters: abcdefghjlmnopqrstuvxyz
Please guess a letter: l
Good guess! wil_____
------
You currently have 9 guesses left
Available letters: abcdefghjmnopqrstuvxyz
Please guess a letter: d
Good guess! wild___d
------
You currently have 9 guesses left
Available letters: abcefghjmnopqrstuvxyz
Please guess a letter: c
Good guess! wildc__d
------
You currently have 9 guesses left
Available letters: abefghjmnopqrstuvxyz
Please guess a letter: #
Letter revealed: a 
 wildca_d
------
You currently have 7 guesses left
Available letters: befghjmnopqrstuvxyz
Please guess a letter: #
Letter revealed: r 
 wildcard
------
Congratulations, you won!
Your score is 61
'''
        global input_string
        computer_guesses = ["k", "w", "i", "l", "d", "c", "#", "#"]
        input_string = (letter for letter in computer_guesses) 
        with unittest.mock.patch('builtins.input',  make_input):
            threw_exception =  False
            try:
                student.hangman_with_help("wildcard")
            except:
                threw_exception = True
            global outputstr
            lines = re.split('\-+',outputstr)
            student_output = outputstr[:]
            outputstr =""
            try:
                self.assertFalse(threw_exception)
                if len(lines) > 9: 
                    self.assertTrue("10 guesses" in lines[1])
                    self.assertTrue("________" in lines[1])
                    self.assertTrue("9 guesses" in lines[2])
                    self.assertTrue("w_______" in lines[2])
                    self.assertTrue("9 guesses" in lines[3])
                    self.assertTrue("wi______" in lines[3])
                    self.assertTrue("9 guesses" in lines[4])
                    self.assertTrue("wil_____" in lines[4])
                    self.assertTrue("9 guesses" in lines[5])
                    self.assertTrue("wild___d" in lines[5])
                    self.assertTrue("9 guesses" in lines[6])
                    self.assertTrue("wildc__d" in lines[6])
                    self.assertTrue("9 guesses" in lines[7])
                    self.assertTrue("revealed" in lines[7])
                    self.assertTrue("7 guesses" in lines[8])
                    self.assertTrue("revealed" in lines[8])
                    self.assertTrue("score" in lines[9])
                    self.assertTrue("61" in lines[9])
                else:
                    self.assertTrue(False)
            except Exception as e:
                output_to_file('test_play_game_wildcard', 'wildcard', computer_guesses, student_output, correct)
                raise(e)
        
# Dictionary mapping function names from the above TestCase class to 
# messages you'd like the student to see if the test fails.
# TODO Add failure messages for HangmanOracle tests
failure_messages = {
    'test_is_word_guessed' : 'Your function is_word_guessed() does not return the correct result.',
    'test_is_word_guessed_repeated_letters' : 'Your function is_word_guessed() does not return the correct result for repeated letters.',
    'test_is_word_guessed_empty_string': 'Your function is_word_guessed() does not return the correct result for the empty string',
    'test_is_word_guessed_empty_list': 'Your function is_word_guessed() does not return the correct result for the empty list',
    'test_get_guessed_word': 'Your function get_guessed_word() does not return the correct result.',
    'test_get_guessed_word_repeated_letters': 'Your function get_guessed_word() does not return the correct result for repeated letters.',
    'test_get_guessed_word_empty_string': 'Your function get_guessed_word() does not return the correct result for the empty string.',
    'test_get_guessed_word_empty_list': 'Your function get_guessed_word() does not return the correct result for the empty list.',
    'test_get_available_letters': 'Your function get_available_letters() does not return the correct result.',
    'test_get_available_letters_empty_string': 'Your function get_available_letters() does not return the correct result for the empty string.',
    'test_get_available_letters_empty_list': 'Your function get_available_letters() does not return the correct result for the empty list.',
    'test_play_game_short': 'You do not play the game right for a two letter word and correct guesses',
    'test_play_game_short_fail': 'You do not play the game right for a two letter word and incorrect guesses',
    'test_play_game_wildcard': 'You do not play the game correctly with help. '
}

# Dictionary mapping function names from the above TestCase class to 
# messages you'd like the student to see if their code throws an error.
# TODO Add error messages for HangmanOracle tests
error_messages = {
    'test_is_word_guessed' : 'Your function is_word_guessed() produces an error.',
    'test_is_word_guessed_repeated_letters' : 'Your function is_word_guessed() produces an error for repeated letters.',
    'test_is_word_guessed_empty_string': 'Your function is_word_guessed() produces an error for the empty string',
    'test_is_word_guessed_empty_list': 'Your function is_word_guessed() produces an error for the empty list',
    'test_get_guessed_word': 'Your function get_guessed_word() produces an error.',
    'test_get_guessed_word_repeated_letters': 'Your function get_guessed_word() produces an error for repeated letters.',
    'test_get_guessed_word_empty_string': 'Your function get_guessed_word() produces an error for the empty string.',
    'test_get_guessed_word_empty_list': 'Your function get_guessed_word() produces an error for the empty list.',
    'test_get_available_letters': 'Your function get_available_letters() produces an error.',
    'test_get_available_letters_empty_string': 'Your function get_available_letters() produces an error for the empty string.',
    'test_get_available_letters_empty_list': 'Your function get_available_letters() produces an error for the empty list.',
    'test_play_game_short': 'You do not play the game right for a two letter word and correct guesses',
    'test_play_game_short_fail': 'You do not play the game right for a two letter word and incorrect guesses',
    'test_play_game_wildcard': 'You do not play the game correctly with help.'
}

# Dictionary mapping function names from the above TestCase class to 
# the point value each test is worth. Make sure these add up to 5! 
# TODO update values depending on the number of Hangman test cases we use
point_values = {
    'test_is_word_guessed' : .40,
    'test_is_word_guessed_repeated_letters' : .40,
    'test_is_word_guessed_empty_string': .40,
    'test_is_word_guessed_empty_list': .40,
    'test_get_guessed_word': .40,
    'test_get_guessed_word_repeated_letters': .40,
    'test_get_guessed_word_empty_string': .40,
    'test_get_guessed_word_empty_list': .40,
    'test_get_available_letters': .40,
    'test_get_available_letters_empty_string': .40,
    'test_get_available_letters_empty_list': .40,
    'test_play_game_short': .35,
    'test_play_game_short_fail': .35,
    'test_play_game_wildcard': .30
}

# Subclass to track a point score and appropriate
# grade comment for a suit of unit tests
class Results_600(unittest.TextTestResult):

	# We override the init method so that the Result object
	# can store the score and appropriate test output. 
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 5

    def addFailure(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, failure_messages)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, error_messages)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, messages):
        point_value = point_values[test_name]
        message = messages[test_name]
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= round(point_value,2)

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points

if __name__ == '__main__':
    exec("import hangman as student")
    #os.remove("run_game_test_results.txt")
    sys.stdout = sys.__stdout__
    
    print("Running unit tests")
    sys.stdout = MyStream(sys.stdout)
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS2))
    result = unittest.TextTestRunner(verbosity=2, resultclass=Results_600).run(suite)

    output = result.getOutput()
    points = round(result.getPoints(),3)
    if points <=0:
        points=0.0
    sys.stdout = sys.__stdout__
    print("\n\nProblem Set 2 Unit Test Results:")
    print(output)
    print("Points for these tests: %s/5\n (Please note that this is not your final pset score, additional test cases will be run on submissions)" % points)
