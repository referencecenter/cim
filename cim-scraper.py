#! python3
# cim-clipboard_csv.py

"""
This program visits webpages listed in a CSV file and attempts to
    determine which pages are more likely to include references to
    AAMC's Careers in Medicine program (CiM). It does this by looking
    for text strings that could explain why the webpage appeared in the
    search results, then determining which of them are more likely to
    refer to CiM, which may or may not refer to CiM, and which probably
    do not refer to CiM. It takes a CSV file as input and outputs
    another CSV file that adds these findings to what was in the
    original CSV file.

Note that if the output lists 0 matches for a page, it does not
    necessarily mean there were actually no matches. It can also mean
    that the program was unable to scrape the full text. This can be the
    case even with a response code of 200. For full accuracy, each page
    will still need to be checked manually. The role of this program is
    more to help divide the pages into groups so it's easier to go
    through them manually, or to help you find some matches if full
    accuracy is not needed.

Depending on how many URLs you want to check, this program can take a
    while to run--at least 5 seconds per URL, due to a built-in pause
    to avoid the program being flagged as a bot.

Instructions:
(1) Prepare the CSV file:
    (a) The first row needs to include the field names (column names).
    (b) One of the field names needs to be "URL".
    (c) You do not need any other fields. However, if you do have other
        fields, please do NOT use any of the following as field names.
        (Admittedly, it is unlikely that you were planning to anyway.):
        
            Scraped Title
            Scraped Response
            Number of More Likely Matches
            More Likely Matches
            Number of Possible Matches
            Possible Matches
            Number of Unlikely Matches
            Unlikely Matches
        
    (d) Save as a CSV file with UTF-8 encoding.
    
(2) Edit this script to indicate where the name of the CSV file, where
    it is saved, and where you want the output CSV file to be saved.
    Users will need to edit only three lines of code, all located
    between the long lines of hashes (lines 67-86). Specifically, they
    will need to edit the variables in lines 75, 79, and 85 to reflect
    the correct information."""

# Import libraries.
from bs4 import BeautifulSoup
import csv
import datetime
import glob
import os
import pandas as pd
from pathlib import Path
import re
import requests
import shutil
import time

########################################################################
# Specify variables.
# I recommend using folders on a hard drive. While this program should
    # work on a network drive, it may take longer.

# Specify the source path. This is the folder where the CSV file is
    # saved. Replace only what is between the quotation marks, not the
    # "r" that precedes them.
source_path = r"C:\Users\rastley\Documents"

# Specify the name of the CSV file that has the URLs. Include the .csv
    # extension.
source_csv = "Predictors of Relationship Persistence.csv"

# Specify the destination path. This is the folder to which the output
    # will be saved. It is fine if it is the same folder as the source
    # path. Replace only what is between the quotation marks, not the
    # "r" that precedes them.
destination_path = r"C:\Users\rastley\Documents"
########################################################################

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
        # Add the stripped item to the new list.
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

"""
This function reads a string to find text that could indicate why that
    page came up in the search results, notes whether that text is a
    probable true positive, possible true positive, or probable false
    positive with regard to referencing the AAMC program now called
    Careers in Medicine. It counts the matches and lists them in a
    dictionary."""
def check_matches(text, dictionary):
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

    # Add the lists to the dictionary.
    dictionary["Number of More Likely Matches"] = len(stripped_more_likelies)
    dictionary["More Likely Matches"] = "; ".join(more_likelies_set_list)
    dictionary["Number of Possible Matches"] = len(stripped_possibles)
    dictionary["Possible Matches"] = "; ".join(possibles_set_list)
    dictionary["Number of Unlikely Matches"] = len(stripped_unlikelies)
    dictionary["Unlikely Matches"] = "; ".join(unlikelies_set_list)

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

# Change the working directory to the source path.
os.chdir(source_path)

# Read the search results CSV file as a list of dictionaries.
with open(source_csv, encoding = "utf-8-sig") as file:
    pages = [{k: v for k, v in row.items()}
             for row in csv.DictReader(file, skipinitialspace = True)]

# Create a variable to keep track of how many pages the program has
    # checked.
n = 1

# Create a regular expression for spaces, tabs, and new line characters.
space_re = re.compile(r"\s")

for page in pages:
    try:
        # Scrape the page.
        response = requests.get(page["URL"])
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        # Identify the page title, if possible.
        try:
            title = soup.title.string
            # Polish up the title.
            # Identify space-like characters in the title.
            title_spaces = space_re.findall(title)
            # Replace all space-like characters in the title with
                # spaces.
            for i in title_spaces:
                title = title.replace(i, " ")
            # Replace all double spaces in the title. I am embedding the
                # replace function within a while loop to account for,
                # e.g., quadruple spaces.
            while "  " in title:
                title = title.replace("  ", " ")
            # Remove leading and trailing spaces from the title.
            title = title.strip()
        except:
            title = "N/A"
        # Add a field for the scraped title to the dictionary for the
            # page.
        page["Scraped Title"] = title
        # Add a field to indicate whether the program was able to
            # connect with the site successfully.
        page["Scrape Response"] = response
        check_matches(data, page)
    except:
        continue
    print(str(n) + " out of " + str(len(pages)) + " URLs checked")
    # Add one to the variable counting how many pages the program has
        # checked so far.
    n += 1
    # Wait five seconds to avoid the program being flagged as a bot.
    time.sleep(5)

# Create a new dataframe.
df = pd.DataFrame(pages)
# Create a timestamp for the filename.
timestamp = str(datetime.datetime.today())[:19].replace(
    ":", "").replace(" ", "_")
# Create the filename.
filename = "cim-matches_" + timestamp + ".csv"
# Write the dataframe to a CSV file.
df.to_csv(filename,
          encoding = "utf-8-sig",
          index = False)
