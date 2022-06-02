#! python3
# cim_clipboard.py

"""
This program finds possible references to AAMC's Careers in Medicine
    program on the clipboard."""

import pyperclip
import random
import re

"""
This function removes duplicates from a list and sorts the list
    alphabetically, without regard for case."""
def del_dupl_and_sort(your_list):
    your_list = list(set(your_list)).sort(key=str.casefold)

"""
This function goes through all items on a list and removes leading and
    trailing whitespaces."""
def strip_list(your_list):
    for i in your_list:
        i = i.strip()

# Create regular expressions to identify probable, possible, and
    # unlikely true positives.
probable_cim_regex = re.compile(
    r"Careers in Medicine|\WCiM\W|[mM][eE][dD][cC][aA][rR][eE][eE][rR][sS]")
possible_cim_regex = re.compile(
    r"Careers In Medicine|\Wcim\W|\WCIM\W|CAREERS IN MEDICINE")
unlikely_cim_regex = re.compile(r"[cC]areers in medicine")

# Establish a variable to keep track of how many texts have been
    # checked.
n = 0

# Introduce the program.
print("Welcome. This program checks text you have copied for possible")
print("\treferences to AAMC's Careers in Medicine program.")
# Print a blank line for readability.
print()

# Provide instructions.
print("Copy the text you want to check.")
print("Press \"Enter\" in this program to check it.")
response = input()

# Start a loop in which every time the user presses "Enter," the program
    # checks the text on the clipboard.
while response == "":
    text = str(pyperclip.paste())
    
    # Find and show probable true positives.
    probables = probable_cim_regex.findall(text)
    print("Probable true positives: " + str(len(probables)))
    strip_list(probables)
    # Remove duplicates.
    probables = list(set(probables))
    for probable in probables:
        print(probable)
    # Print blank line for readability.
    print()
    
    # Find and show possible true positives.
    possibles = possible_cim_regex.findall(text)
    print("Possible true positives: " + str(len(possibles)))
    strip_list(possibles)
    # Remove duplicates.
    possibles = list(set(possibles))
    for possible in possibles:
        print(possible)
    # Print blank line for readability.
    print()

    # Find and show probable false positives.
    unlikelies = unlikely_cim_regex.findall(text)
    print("Probable FALSE positives: " + str(len(unlikelies)))
    strip_list(unlikelies)
    # Remove duplicates.
    unlikelies = list(set(unlikelies))
    for unlikely in unlikelies:
        print(unlikely)
    # Print blank line for readability.

    # Add one to the variable counting how many texts the program has
        # checked.
    n +=1

    # Print a random length string of asterisks to make it easier to see
        # that a new text has been entered.
    print("*"*random.randint(20,72))
    if n == 1:
        print("You have checked 1 text.")
    else:
        print("You have checked " + str(n) + " texts.")
    print("To test more text, copy it, then press \"Enter\" again in this " +
          "program.")
    print("If you are finished, type anything and press \"Enter.\"")
    response = input()

print()
print("Thank you for using this program.")
print("You checked " + str(n) + " texts.")
