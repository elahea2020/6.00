#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:08:52 2017

@author: lauragustafson
"""

import ps3
import unittest
from unittest import mock
import sys
from io import StringIO
STOP_ITER_MSG = """For the given list of user commands executed in order %s,
when your hand is %s your code did not complete the game. You might want to check that you no longer prompt the user if they want to replay a hand/substitute a letter after they do it once.
        """
STOP_ITER_MSG_GAME = """For the given list of user commands executed in order %s,
when your hands are %s your code did not complete the game. You might want to check that you no longer prompt the user if they want to replay a hand/substitute a letter after they do it once.
        """
STOP_ITER_MSG_GAME_REPLACE = """For the given list of use commands executed in order %s,
when your hands are %s and replace letter yeilds '%s' your code did not complete the game. You might want to check that you no longer prompt the user if they want to replay a hand/substitute a letter after they do it once.
        """
WRONG_SCORE_GAME = """For the given list of use commands executed in order %s,
when your hands are %s your code returns score %s instead of the correct score %s.  
        """
WRONG_SCORE_GAME_REPLACE = """For the given list of use commands executed in order %s,
when your hands are %s and replace letter yeilds '%s' your code return score %s instead of the correct score %s.  
        """

NOT_IMPLEMENTED = """You have not implemented this function yet."""

CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VOWELS = 'aeiou'

class TestPlayHandAndGame(unittest.TestCase):

    def test_get_word_score(self):
        """
        Unit test for get_word_score
        """
        # dictionary of words and scores
        words = {("", 7):0, ("it", 7):4, ("was", 7):12, ("weed", 6):32,
                 ("scored", 7):198, ("WaYbILl", 7):525, ("Outgnaw", 7):385,
                 ("fork", 7):22, ("FORK", 4):220}
        try:
            for (word, n) in words.keys():
                score = ps3.get_word_score(word, n)
                error_msg = "Expected "+ str(words[(word, n)])+ " points but got '"  + str(score) + "' for word '" + word + "', n=" + str(n)
                self.assertEqual(score, words[(word, n)],  error_msg)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)

    def test_update_hand_1(self):
        """
        Unit test for update_hand
        """
        # test 1
        handOrig = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
        handCopy = handOrig.copy()
        word = "quail"
        msg_part1 = "Failed when updating hand '%s' with word '%s'. " %(str(handOrig), word)
        try:
            hand2 = ps3.update_hand(handCopy, word)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
        expected_hand1 = {'l':1, 'm':1}
        expected_hand2 = {'a':0, 'q':0, 'l':1, 'm':1, 'u':0, 'i':0}
        error_msg = msg_part1 + "Returned: " + str(hand2) + "\n-- but expected: "+ str(expected_hand1)+ " or "+ str(expected_hand2)
        self.assertTrue(hand2 == expected_hand1 or hand2 == expected_hand2, error_msg)
        error_msg = msg_part1 + "Original hand was "+ str(handOrig) + " but implementation of update_hand mutated the original hand! Now the hand looks like this:" + str(handCopy)
        self.assertEqual(handCopy, handOrig, error_msg)
        
    def test_update_hand_2(self):  
        #test 1
        handOrig = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
        handCopy = handOrig.copy()
        word = "Evil"
        msg_part1 = "Failed when updating hand '%s' with word '%s'. " %(str(handOrig), word)
        try:
            hand2 = ps3.update_hand(handCopy, word)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
        expected_hand1 = {'v':1, 'n':1, 'l':1}
        expected_hand2 = {'e':0, 'v':1, 'n':1, 'i':0, 'l':1}
        error_msg = msg_part1 + "Returned: " + str(hand2) + "\n-- but expected: "+ str(expected_hand1)+ " or "+ str(expected_hand2)
        self.assertTrue(hand2 == expected_hand1 or hand2 == expected_hand2, error_msg)
        error_msg = msg_part1 + "Original hand was "+ str(handOrig) + " but implementation of update_hand mutated the original hand! Now the hand looks like this:" + str(handCopy)
        self.assertEqual(handCopy, handOrig, error_msg)
        
    def test_update_hand_3(self): 
        # test 3
        handOrig = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
        handCopy = handOrig.copy()
        word = "HELLO"
        msg_part1 = "Failed when updating hand '%s' with word '%s'. " %(str(handOrig), word)
        try:
            hand2 = ps3.update_hand(handCopy, word)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
        expected_hand1 = {}
        expected_hand2 = {'h': 0, 'e': 0, 'l': 0, 'o': 0}
        error_msg = msg_part1 + "Returned: " + str(hand2) + "\n-- but expected: "+ str(expected_hand1)+ " or "+ str(expected_hand2)
        self.assertTrue(hand2 == expected_hand1 or hand2 == expected_hand2, error_msg)
        error_msg = msg_part1 + "Original hand was "+ str(handOrig) + " but implementation of update_hand mutated the original hand! Now the hand looks like this:" + str(handCopy)
        self.assertEqual(handCopy, handOrig, error_msg)
# end of test_update_hand

    def test_is_valid_word_hello_valid(self):
        """
        Unit test for is_valid_word
        """
        # test 1
        word = "hello"
        handOrig = ps3.get_frequency_dict(word)
        handCopy = handOrig.copy()
        try:
            result = ps3.is_valid_word(word, handCopy, word_list)
            self.assertTrue(result, "\tExpected True, but got False from is_valid_word for word: '" + word + "' and hand: "+ str(handOrig))
            if not ps3.is_valid_word(word, handCopy, word_list):
                self.assertEquals(handCopy, handOrig, "\tTesting word " + word + " for a second time for is_valid_word - be sure you're not modifying hand. \nAt this point, hand ought to be " + str(handOrig)+ " but it is "+ str(handCopy))
                wordInWL = word in word_list
                self.assertTrue(wordInWL, "The word " + word + " should be in word_list - is it? " +str(wordInWL))
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
    def test_is_valid_word_rapture_invalid(self):   
        # test 2
        hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u':1}
        word = "Rapture"
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
            self.assertFalse(result, message)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
    # test 3
    def test_is_valid_word_honey_valid(self):
        hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
        word = "honey"
        message = "Expected True, but got False from is_valid_word for word: '"+ word +"' and hand: "+ str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
            self.assertTrue(result, message)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
    # test 4
    def test_is_valid_word_honey_invalid(self):
        hand = {'r': 1, 'a': 3, 'p': 2, 't': 1, 'u':2}
        word = "honey"
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " +str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
            self.assertFalse(result, message)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
    def test_is_valid_word_evil_valid(self):
        # test 5
        hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
        word = "EVIL"
        message = "Expected True, but got False from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
            self.assertTrue(result, message)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)

    def test_is_valid_word_even_invalid(self):
        # test 5
        hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
        # test 6
        word = "Even"
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
            self.assertFalse(result,message)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)    
        
    def test_is_valid_word_hello_invalid(self):
        # test 7
        hand = {'n': 1, 'h': 1, 'o': 1, 'l': 1, 'd':1, 'w':1, 'e': 2}
        word = "hello"
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
            self.assertFalse(result, message)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)  
# end of test_is_valid_word

    def test_wildcard_1(self):
        """
        Unit test for is_valid_word
        """
    
        # test 1
        hand = {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '@': 1}
        word = "c@t"
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        try:
            result = ps3.is_valid_word(word, hand, word_list)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
        self.assertFalse(result, message)
        
    def test_wildcard_2(self):
        # test 2
        hand = {'n': 1, 'h': 1, '@': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
        word = "honey"
        try:
            result = ps3.is_valid_word(word, hand, word_list)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        self.assertFalse(result, message)
        
    def test_wildcard_3(self):
        # test 3
        hand = {'n': 1, 'o': 1, '@': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
        word = "@oney"
        try:
            result= ps3.is_valid_word(word, hand, word_list)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)  
        message = "Expected True, but got False from is_valid_word for word: '"+ word +"' and hand: " + str(hand)
        self.assertTrue(result, message)

    def test_wildcard_4(self):
        # test 4
        hand = {'c': 1, 'o': 1, '@': 1, 'w': 1, 's':1, 'z':1, 'y': 2}
        word = "c@wz"
        try:
            result = ps3.is_valid_word(word, hand, word_list)
        except NotImplementedError as e:
            self.fail(NOT_IMPLEMENTED)  
        message = "Expected False, but got True from is_valid_word for word: '" + word + "' and hand: " + str(hand)
        self.assertFalse(result, message)

    def test_deal_hand_wildcard(self):
        hand = ps3.deal_hand(9)
        num_vowels = 3
        vowels_sum =0
        for v in VOWELS:
            vowels_sum += hand.get(v, 0)
        self.assertIn('@', hand, "Users should be dealt exactly one wildcard. Your hand from deal_hand is: " + str(hand))
        self.assertEqual(hand['@'], 1, "Users should be dealt exactly one wildcard. Your hand from deal_hand is: " + str(hand))
        self.assertEqual(vowels_sum, num_vowels,"The wildcard in deal_hand should replace a consonant. The number of vowels %s =int(math.ceil(%s / 3)) should remain unchanged. Your dealt hand is : %s" %(num_vowels,9,str(hand)))
    def test_wilcard_score(self):
        # dictionary of words and scores WITH wildcards
        words = {("@oney", 7):63, ("@ows", 6):24, ("@ails", 7):36}
        for (word, n) in words.keys():
            try:
                score = ps3.get_word_score(word, n)
                message = "Expected "+ str(words[(word, n)]) +" points for get_word_score but got '" + str(score) + "' for word '" + word + "', n=" + str(n)
                self.assertEqual(score, words[(word, n)], message)
            except NotImplementedError as e:
                self.fail(NOT_IMPLEMENTED)  


    def test_substitute_hand_vowel(self):
        """
        Unit test for substitute_hand
        """
        for i in range(20):
            # test 1
            hand = {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '@': 1}
            letter = "a"
            try:
                new_hand = ps3.substitute_hand(hand, letter)

                result = 'o' in new_hand or 'i' in new_hand or 'u' in new_hand
                self.assertTrue(result, "In substitute_hand you should only be able to subsitute a vowel for a vowel and should not be able to get back a letter already in the hand")
            except NotImplementedError as e:
                self.fail(NOT_IMPLEMENTED)  
                
    def test_substitute_hand_not_same_letter(self):        
        # test 2
        hand = {'a': 1, 'r': 1, 'e': 1, 'j': 2, 'm': 1, '@': 1}
        letter = "r"
        try:
            new_hand = ps3.substitute_hand(hand, letter)
            self.assertFalse('r' in new_hand and new_hand['r'] !=0, "In substitute_hand you should not get back a letter already in the hand (or the letter you are substituting)")
        except NotImplementedError as e:
                        self.fail(NOT_IMPLEMENTED)  
    
    def test_substitute_hand_constonant(self):        
        # test 2
        #do multiple times to make sure they arent passing by chance
        for i in range(100):
            hand = {'r': 1}
            letter = "r"
            try:
                new_hand = ps3.substitute_hand(hand, letter)
                hand_keys = list(new_hand.keys())
                try:
                    hand_keys.remove(letter)
                except ValueError:
                    pass  # do nothing!
                self.assertTrue(len(hand_keys)>0, "In substitute_hand your new letter should not be your old letter")
                new_letter = hand_keys[0]
                self.assertIn(new_letter, CONSONANTS, "In substitute_hand you should only be able to substitute constant for a constant")
            except NotImplementedError as e:
                self.fail(NOT_IMPLEMENTED)
    def test_play_hand_basic(self):
        #create place to save output
        student_deal_hand=ps3.deal_hand
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        hand = {'a':1, 'j':1, 'e':1, 'f':1, '@':1, 'r':1, 'x':1, 'd':1}
        error = "Expected %s, received %s as score for hand '%s' when user input is %s"
        user_input = ['jar', '*END*']
        e_result = 20
        result = -1
        try:
            with mock.patch('builtins.input', side_effect=user_input):
                result = ps3.play_hand(hand, word_list)  
            ps3.deal_hand = student_deal_hand
            self.assertEqual(result, e_result, error %(e_result, result, hand, user_input))
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(user_input, hand))
        except NotImplementedError as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(NOT_IMPLEMENTED)
        except:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            raise
            
        sys.stdout = saved_stdout
    def test_play_hand_1(self):
        #create place to save output
        student_deal_hand=ps3.deal_hand
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        hand = {'a':1, 'j':1, 'e':1, 'f':1, '@':1, 'r':1, 'x':1, 'd':1}
        error = "Expected %s, received %s as score for hand '%s' when user input is %s"
        user_input = ['jar', 'fe@', '*END*']
        e_result = 30
        result = -1
        try:
            with mock.patch('builtins.input', side_effect=user_input):
                result = ps3.play_hand(hand, word_list)  
            self.assertEqual(result, e_result, error %(e_result, result, hand, user_input))
            ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(user_input, hand))
        except NotImplementedError as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(NOT_IMPLEMENTED)
        except:
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout
            raise
            
        sys.stdout = saved_stdout
        
    
    def test_play_hand_2(self):
        #create place to save output
        student_deal_hand  = ps3.deal_hand
        saved_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        hand = {'a':1, 'c':1, 'f':1, 'i':1, '@':1, 't':1, 'x':1 }
        error = "Expected %s, received %s as score for hand '%s' when user input is %s"
        user_input = ['fix', 'tc', 'a@']
        e_result = 36
        result = -1
        try:
            with mock.patch('builtins.input', side_effect=user_input):
                result = ps3.play_hand(hand, word_list) 
            self.assertEqual(result, e_result, error %(e_result, result, hand, user_input))
            ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(user_input, hand))
        except NotImplementedError as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(NOT_IMPLEMENTED)
        except:
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout
            raise
        ps3.deal_hand = student_deal_hand
        sys.stdout = saved_stdout
        
    def test_play_hand_with_invalid_word(self):
        student_deal_hand  = ps3.deal_hand
        saved_stdout = sys.stdout
        #create place to save output
        out = StringIO()
        sys.stdout = out
        
        hand = {'a':1, 'c':1, 'i':1, 'p':1, 'r':1, 't':1, '@':1}
        error = "Expected %s, received %s as score for hand '%s' when user input is %s"
        #mock input for game
        try:
            inputs = [['part', 'ict','*END*']]
            results = [12]
            for i in range(len(results)):
                with mock.patch('builtins.input', side_effect=inputs[i]):
                    result = ps3.play_hand(hand, word_list)  
                self.assertEqual(result, results[i], error %(results[i], result, hand, inputs[i]))
                ps3.deal_hand = student_deal_hand
        except StopIteration as e:    
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(inputs[i], hand))
        except NotImplementedError as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(NOT_IMPLEMENTED)
        except:
            #restore saved output
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout
            raise
        #restore saved output
        ps3.deal_hand = student_deal_hand
        sys.stdout = saved_stdout
        
    def test_play_hand_correct_handlen(self):
        student_deal_hand  = ps3.deal_hand
        saved_stdout = sys.stdout
        #create place to save output
        out = StringIO()
        sys.stdout = out
        
        hand = {'d':2, 'a':1, 'o':1, 'u':1, 't':1, '@':1}
        error = "Expected %s, received %s as score for hand '%s' when user input is %s"
        #mock input for game
        try:
            inputs = [['dad','*END*']]
            results = [10]
            for i in range(len(results)):
                with mock.patch('builtins.input', side_effect=inputs[i]):
                    result = ps3.play_hand(hand, word_list)  
                self.assertEqual(result, results[i], error %(results[i], result, hand, inputs[i]))
                ps3.deal_hand = student_deal_hand
        except StopIteration as e:    
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(inputs[i], hand))
        except NotImplementedError as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(NOT_IMPLEMENTED)
        except:
            #restore saved output
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            raise
        #restore saved output
        sys.stdout = saved_stdout
        
    def test_play_hand_wildcard(self):
        #redirect output to silence print statements during running of tests
        saved_stdout = sys.stdout
        student_deal_hand = ps3.deal_hand
        #create place to save output
        out = StringIO()
        sys.stdout = out
        
        hand = {'c':1, 'o':1, 'w':1, 's':1, '@':1, 'z':1}
        error = "Expected %s, received %s as score for hand '%s' when user input is %s."
        #mock input for game
        try:
            inputs = [['cows', '*END*'], ['@ows', '*END*'], ['co@z', '*END*'], ['c@ws', '*END*']]
            results = [36, 24, 0,0]
            for i in range(len(results)):
                with mock.patch('builtins.input', side_effect=inputs[i]):
                    result = ps3.play_hand(hand, word_list)  
                self.assertEqual(result, results[i], error %(results[i], result, hand, inputs[i]))
                ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(inputs[i], hand))
        except NotImplementedError as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(NOT_IMPLEMENTED)
        except:
            #restore saved output
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout
            raise
        sys.stdout = saved_stdout
        
    def test_play_game_basic(self):
        #redirect output to silence print statements during running of tests
        student_deal_hand = ps3.deal_hand
        saved_stdout = sys.stdout
        #create place to save output
        out = StringIO()
        sys.stdout = out
        #save previous standard ouptut
        h1 = {'a':1, 'c':1, 'i':1, 'p':1, 'r':1, 't':1, '@':1}
        
        ps3.deal_hand = mock.Mock(side_effect=[h1])
        #ps3.substitute_leter = mock.Mock(side_effect=['a'])
        inputs = ['1', 'no', 'car', 'pit', '*END*', 'no']
        result = -1    
        try:
            #mock input for game
            with mock.patch('builtins.input', side_effect=inputs):
                result = ps3.play_game(word_list)
                if result == None:
                    sys.stdout = saved_stdout
                    self.fail(NOT_IMPLEMENTED)
            self.assertEqual(result, 45, WRONG_SCORE_GAME %(inputs, h1, result, 45))
            ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout
            self.fail(STOP_ITER_MSG %(inputs, h1))
        except:
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout 
            raise
        #change standard output to be saved
        ps3.deal_hand = student_deal_hand
        sys.stdout = saved_stdout 
        
    def test_play_game_with_replay(self):
        #redirect output to silence print statements during running of tests
        saved_stdout = sys.stdout
        student_deal_hand = ps3.deal_hand
        #create place to save output
        out = StringIO()
        sys.stdout = out
        #save previous standard ouptut
        h1 = {'a':1, 'c':1, 'i':1, 'p':1, 'r':1, 't':1, '@':1}
        
        ps3.deal_hand = mock.Mock(side_effect=[h1])
        inputs = ['1', 'no', 'car', 'pit', '*END*', 'yes', 'ca@', 'tip', '*END*']
        result = -1    
        try:
            #mock input for game
            with mock.patch('builtins.input', side_effect=inputs):
                result = ps3.play_game(word_list)
                if result == None:
                    sys.stdout = saved_stdout
                    self.fail(NOT_IMPLEMENTED)     
            
            self.assertEqual(result, 45, WRONG_SCORE_GAME %(inputs, h1, result, 45))
            ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG %(inputs, h1))
        except:
            ps3.deal_hand = student_deal_hand
            sys.stdout = saved_stdout 
            raise
        #change standard output to be saved
        ps3.deal_hand = student_deal_hand
        sys.stdout = saved_stdout 
        
    def test_play_game_with_substitution_and_replay(self):
        #redirect output to silence print statements during running of tests
        saved_stdout = sys.stdout
        student_deal_hand = ps3.deal_hand
        #create place to save output
        out = StringIO()
        sys.stdout = out
        #save previous standard ouptut
        h1 = {'a':1, 'c':1, 'i':1, 'p':1, 'r':1, 't':1, '@':1}
        h2 = {'f':2, 'a':1, 'o':1, 'u':1, 't':1, '@':1}
        replaced_letter = {'d':2, 'a':1, 'o':1, 'u':1, 't':1, '@':1}
        old_substitute = ps3.substitute_hand
        ps3.deal_hand = mock.Mock(side_effect=[h1, h2])
        ps3.substitute_hand = mock.Mock(side_effect=[replaced_letter])
        inputs = ['2', 'no', 'part', '@ic', 'no', 'yes', 'f', 'out', '*END*', 'yes', 'dad', 'out', '*END*']
            

        try: #mock input for game
            with mock.patch('builtins.input', side_effect=inputs):
                result = ps3.play_game(word_list)
                if result == None:
                    sys.stdout = saved_stdout
                    self.fail(NOT_IMPLEMENTED)
            self.assertEqual(result, 103, WRONG_SCORE_GAME_REPLACE %(inputs, [h1,h2], 'd', result, 103))   
            ps3.substitute_hand = old_substitute
            ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            ps3.substitute_hand = old_substitute
            self.fail(STOP_ITER_MSG_GAME %(inputs, [h1,h2]))
        except:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            ps3.substitute_hand = old_substitute
            raise
        sys.stdout = saved_stdout 
        ps3.deal_hand = student_deal_hand
        ps3.substitute_hand = old_substitute
        
    def test_play_game_2_hands(self):
        #redirect output to silence print statements during running of tests
        student_deal_hand = ps3.deal_hand
        
        saved_stdout = sys.stdout
        #create place to save output
        out = StringIO()
        sys.stdout = out
        #save previous standard ouptut
        h1 = {'s':1, 'c':1, 'i':1, 'p':1, 'r':1, 'k':1, '@':1}
        h2 = {'d':1, 'a':1, 'e':1, 'l':1, 'f':1, 'z':1, '@':1}
        
        ps3.deal_hand = mock.Mock(side_effect=[h1, h2])
        inputs = ['2', 'no', 'sick', '*END*', 'no', 'no', 'deal', '*END*', 'no']
        correct_answer = 30
        
        try: #mock input for game
            with mock.patch('builtins.input', side_effect=inputs):
                result = ps3.play_game(word_list)
                if result == None:
                    sys.stdout = saved_stdout
                    self.fail(NOT_IMPLEMENTED)
            self.assertEqual(result, correct_answer, WRONG_SCORE_GAME %(inputs, [h1,h2], result, correct_answer))    
            ps3.deal_hand = student_deal_hand
        except StopIteration as e:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            self.fail(STOP_ITER_MSG_GAME %(inputs, [h1,h2]))
        except:
            sys.stdout = saved_stdout
            ps3.deal_hand = student_deal_hand
            raise
        ps3.deal_hand = student_deal_hand
        sys.stdout = saved_stdout 
if __name__ == '__main__':
    print('Hello')
    word_list = ps3.load_words()
    print('Hello')
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayHandAndGame)
    unittest.TextTestRunner(verbosity=2).run(suite)
