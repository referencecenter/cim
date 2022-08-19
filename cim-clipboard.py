#! python3
# cim-clipboard.py

"""
This program finds possible references to AAMC's Careers in Medicine
    program on the clipboard."""

# Import libraries.
import pandas as pd
import pyperclip
# import random
import re
from tabulate import tabulate

"""
This function goes through all items on a list, and leading and trailing
    whitespace, removes leading and trailing non-letter characters, and
    adds the stripped item to a new list."""
def strip_list(old_list, new_list):
    for i in old_list:
        # Remove leading and trailing whitespace.
        i_1 = i.strip()
        # If the first character is not a letter, remove it.
        if i_1[0].isalpha() == False:
            i_2 = i_1[1:]
        else:
            i_2 = i_1
        # If the last character is not a letter, remove it.
        if i_2[-1].isalpha() == False:
            i_3 = i_2[:-1]
        else:
            i_3 = i_2
        new_list.append(i_3)     

# Create regular expressions to identify more likely, possible, and
    # unlikely true positives. Some groups are split into multiple
    # regular expressions (a) to make it easier to deal with some
    # matches requiring case sensitivity and others not, (b) to conform
    # to PEP 8 guidelines regarding line length, and (c) to make the
    # code easier to read.
more_likely_re_1 = re.compile(r"Careers in Medicine|\WCiM\W")
more_likely_re_2 = re.compile(r"medcar{1,2}e{1,2}rs", re.IGNORECASE)
possible_re = re.compile(
    r"Careers In Medicine|\Wcim\W|\WCIM\W|CAREERS IN MEDICINE")
unlikely_re_1 = re.compile(r"[cC]areers in medicine")
unlikely_re_2 = re.compile(r"career in", re.IGNORECASE)

# Create sample text with which to test the regular expressions.
sample_text = ("AAMC has a program called called Careers in " +
               "Medicine, which is abbreviated \"CiM.\" \"CiM\"" + 
               "sometimes appears between parentheses (CiM). " +
               "Sometimes the name is rendered with a capitalized " +
               "\"I,\" as in \"Careers In Medicine\" (CIM [CIM]). " +
               "Some texts may use all capitals, shouting, " +
               "\"CAREERS IN MEDICINE\"! The program used to be " +
               "called MEDcareers or MedCAREERS or medCAREERS or " +
               "medCareers or MEDCAREERS, or maybe even medcareers. " +
               "One of those iterations was official, but people " +
               "don't always write it that way (similar to how " +
               "people write \"American Association of Medical " +
               "Colleges\" instead of \"Association of American " +
               "Medical Colleges\"). I think I've even seen " +
               "something like \"Medcarrers\" in a non-English " +
               "language text. Also, some search engines try to be " +
               "helpful by including near matches, such as \"career " +
               "in medicine,\" or even \"career in academic " +
               "medicine.\" To be fair, this kind of thing is " +
               "generally helpful--it just so happens that this is " +
               "one of the cases where the near match is almost " +
               "certainly a false positive. Similarly, search engines" +
               "tend to be case insensitive, which is usually " +
               "helpful--with CiM, however, it leads to many false " +
               "positives, as many people talk about careers in " +
               "medicine without referring to the AAMC program.")

# Establish a variable to keep track of how many texts have been
    # checked.
n = 0

# Introduce the program.
print("Welcome. This program checks text you have copied for possible")
print("    references to AAMC's Careers in Medicine program.")

# Print a blank line for readability.
print()

# Provide instructions.
print("Copy the text you want to check. Then, press \"Enter\" in this")
print("    program to check it.")

response = input()

# Start a loop in which every time the user presses "Enter," the program
    # checks the text on the clipboard.

while response == "":
    # Assign text in the clipboard to a variable.
    text = str(pyperclip.paste())

    # Check the text for each of the regular expressions.
    more_likelies_1 = more_likely_re_1.findall(text)
    more_likelies_2 = more_likely_re_2.findall(text)
    possibles = possible_re.findall(text)
    unlikelies_1 = unlikely_re_1.findall(text)
    unlikelies_2 = unlikely_re_2.findall(text)

    # Merge the regular expression match lists where there were multiple
        # regular expressions for the same type of match.
    more_likelies = more_likelies_1 + more_likelies_2
    unlikelies = unlikelies_1 + unlikelies_2

    # Create lists to which to add stripped matches.
    stripped_more_likelies = []
    stripped_possibles = []
    stripped_unlikelies = []

    # Strip each list.
    strip_list(more_likelies, stripped_more_likelies)
    strip_list(possibles, stripped_possibles)
    strip_list(unlikelies, stripped_unlikelies)

    # Remove duplicates from each list.
    more_likelies_set_list = sorted(set(stripped_more_likelies),
                                    key = str.casefold)
    possibles_set_list = sorted(set(stripped_possibles), key = str.casefold)
    unlikelies_set_list = sorted(set(stripped_unlikelies), key = str.casefold)

    # Create a list to which to add dictionaries for the more likely
        # matches. The dictionaries will indicate how many times each
        # term appeared.
    more_likelies_dicts = []
    # Count how many times each term appeared.
    for item in more_likelies_set_list:
        more_likelies_dicts.append({
            "Match": item,
            "Count": stripped_more_likelies.count(item)})
    # Create a dataframe out of the list of dictionaries.
    if len(more_likelies_dicts) > 0:
        more_likelies_df = pd.DataFrame(more_likelies_dicts).sort_values(
            by = ["Count"], ascending = False)

    # Create a list to which to add dictionaries for the possible
        # matches.
    possibles_dicts = []
    # Count how many times each term appeared.
    for item in possibles_set_list:
        possibles_dicts.append({
            "Match": item,
            "Count": stripped_possibles.count(item)})
    # Create a dataframe out of the list of dictionaries.
    if len(possibles_dicts) > 0:
        possibles_df = pd.DataFrame(possibles_dicts)

    # Create a list to which to add dictionaries for the unlikely
        # matches.
    unlikelies_dicts = []
    # Count how many times each term appeared.
    for item in unlikelies_set_list:
        unlikelies_dicts.append({
            "Match": item,
            "Count": stripped_unlikelies.count(item)})
    # Create a dataframe out of the list of dictionaries.
    if len(unlikelies_dicts) > 0:
        unlikelies_df = pd.DataFrame(unlikelies_dicts)

    # Display the existing dataframes.
    print("More Likely True Positives: " +
          str(len(more_likelies)).rjust(3))
    if len(more_likelies_dicts) > 0:
        print(tabulate(more_likelies_df, headers = "keys", tablefmt = "psql",
                       showindex = False))
    print()
    print("Possible True Positives: " +
          str(len(possibles)).rjust(6))
    if len(possibles_dicts) > 0:
        print(tabulate(possibles_df, headers = "keys", tablefmt = "psql",
                       showindex = False))
    print()
    print("Probable FALSE Positives: " +
          str(len(unlikelies)).rjust(5))
    if len(unlikelies_dicts) > 0:
        print(tabulate(unlikelies_df, headers = "keys", tablefmt = "psql",
                       showindex = False))

    # Add one to the variable counting how many texts the program has
        # checked.
    n += 1

    # Print a row of asterisks to make it easier to see when a new text
        # has been entered.
    print("*"*72)
    
    # Report how many texts the user has checked.
    if n == 1:
        print("You have checked 1 text.")
    else:
        print("You have checked " + str(n) + " texts.")
    
    # Provide instructions to check more texts or finish the program.
    print("To test more text, copy it, then press \"Enter\" again in this")
    print("    program.")
    print("If you are finished, type anything and press \"Enter.\"")

    # Print a row of asterisks to make it easier to see when a new text
        # has been entered.
    print("*"*72)
    response = input()

print()
print("Thank you for using this program.")
print("You checked " + str(n) + " texts.")
print("Press \"Enter\" to end the program.")

close = input()
