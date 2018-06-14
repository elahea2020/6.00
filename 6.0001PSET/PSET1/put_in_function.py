#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:55:06 2017

@author: lauragustafson, knjohnso, carlosh
"""
def put_in_functions_a():

    FUNCTION_NAME = 'part_a'
    #change FUNCTION_NAME to be the name of the function that you want their code
    #to be wrapped in

    FUNCTION_HEADER = 'def %s(annual_salary, portion_saved, total_cost):' % (FUNCTION_NAME)

    STUDENT_FILE_NAME = 'ps1a.py'
    #change STUDENT_FILE_NAME to be the name of the file that their code will be in


    RETURN_VARIABLE = 'months'
    #change RETURN_VARIABLE to be the name of the variable you want the fucntion
    #to return

    RETURN_STATEMENT = '\treturn %s' % (RETURN_VARIABLE)

    NEW_FILE_NAME = 'ps1a_in_function.py'
    #change NEW_FILE_NAME to be the name of the output file

    LAST_INPUT_VARIABLE = "total_cost" 
    #The last variable that we should be getting from user input, everything else below this should be fine to copy

    new_lines = []
    lines = [line.rstrip('\n') for line in open('ps1a.py')]
    # look for first instance of first variable we expect (i.e. annual_salary)
    START_INDEX = [line.startswith(LAST_INPUT_VARIABLE) for line in lines].index(True)
    lines = lines[START_INDEX+1:]
 
    new_lines.append(FUNCTION_HEADER)
    for line in lines:
        new_lines.append('\t'+line)
    new_lines.append(RETURN_STATEMENT)

    with open(NEW_FILE_NAME, 'w') as new_file:
        print(new_lines)
        new_file.write('\n'.join(new_lines))

def put_in_functions_b():

    FUNCTION_NAME = 'part_b'
    #change FUNCTION_NAME to be the name of the function that you want their code
    #to be wrapped in

    FUNCTION_HEADER = 'def %s(annual_salary, portion_saved, total_cost, semi_annual_raise):' % (FUNCTION_NAME)

    STUDENT_FILE_NAME = 'ps1b.py'
    #change STUDENT_FILE_NAME to be the name of the file that their code will be in


    RETURN_VARIABLE = 'months'
    #change RETURN_VARIABLE to be the name of the variable you want the fucntion
    #to return

    RETURN_STATEMENT = '\treturn %s' % (RETURN_VARIABLE)

    NEW_FILE_NAME = 'ps1b_in_function.py'
    #change NEW_FILE_NAME to be the name of the output file

    LAST_INPUT_VARIABLE = "semi_annual_raise" 
    #The last variable that we should be getting from user input, everything else below this should be fine to copy

    new_lines = []
    lines = [line.rstrip('\n') for line in open('ps1b.py')]
    # look for first instance of first variable we expect (i.e. annual_salary)
    START_INDEX = [line.startswith(LAST_INPUT_VARIABLE) for line in lines].index(True)
    lines = lines[START_INDEX+1:]
    
    new_lines.append(FUNCTION_HEADER)
    for line in lines:
        new_lines.append('\t'+line)
    new_lines.append(RETURN_STATEMENT)

    with open(NEW_FILE_NAME, 'w') as new_file:
        print(new_lines)
        new_file.write('\n'.join(new_lines))


def put_in_functions_c():

    FUNCTION_NAME = 'part_c'
    #change FUNCTION_NAME to be the name of the function that you want their code
    #to be wrapped in

    FUNCTION_HEADER = 'def %s(initial_deposit):' % (FUNCTION_NAME)

    STUDENT_FILE_NAME = 'ps1c.py'
    #change STUDENT_FILE_NAME to be the name of the file that their code will be in


    RETURN_VARIABLE = 'best_r, steps'
    #change RETURN_VARIABLE to be the name of the variable you want the fucntion
    #to return

    RETURN_STATEMENT = '\treturn %s' % (RETURN_VARIABLE)

    NEW_FILE_NAME = 'ps1c_in_function.py'
    #change NEW_FILE_NAME to be the name of the output file

    LAST_INPUT_VARIABLE = "initial_deposit" 
    #The last variable that we should be getting from user input, everything else below this should be fine to copy

    new_lines = []
    lines = [line.rstrip('\n') for line in open('ps1c.py')]
    # look for first instance of first variable we expect (i.e. annual_salary)
    START_INDEX = [line.startswith(LAST_INPUT_VARIABLE) for line in lines].index(True)
    lines = lines[START_INDEX+1:]

    new_lines.append(FUNCTION_HEADER)
    for line in lines:
        new_lines.append('\t'+line)
    new_lines.append(RETURN_STATEMENT)

    with open(NEW_FILE_NAME, 'w') as new_file:
        print(new_lines)
        new_file.write('\n'.join(new_lines))
