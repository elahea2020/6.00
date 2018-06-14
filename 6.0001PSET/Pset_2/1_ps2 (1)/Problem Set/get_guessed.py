#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 18:04:34 2017

@author: codeWorm
"""

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters and underscores (_) that represents
      which letters in secret_word have been guessed so far.
    '''
    print('Im in function')
    secret_word_size = len(secret_word)
    guessed_words = '_'*secret_word_size
    print(guessed_words)
    for i,j in enumerate(secret_word):
        print('i = %d, j = %c'%(i,j))
        if j in letters_guessed: 
            guessed_words = guessed_words[:i]+ guessed_words[i:i+1].replace('_',j)+guessed_words[i+1:]
        print(guessed_words)
    return guessed_words

secret_word = 'hey'
letters_guessed = ['y', 'r', 'e', 'b']
print('before')
print(get_guessed_word(secret_word, letters_guessed))