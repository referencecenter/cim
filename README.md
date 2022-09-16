# cim

## Summary

The tools in this repository help filter through search results to identify those more likely to contain references to the AAMC Careers in Medicine® program (CiM). They could be adapted for other projects where case-sensitive searching is useful.

## Background

The [Association of American Medical Colleges](https://www.aamc.org 'Tomorrow\'s Doctors, Tomorrow\'s Cures | AAMC') (AAMC) has a program called [Careers in Medicine®](https://www.aamc.org/cim/ 'Home | Careers in Medicine') (CiM), which used to be called MedCAREERS. The programs in this repository were born out of a need to find references to CiM. Many instances of the phrase \"careers in medicine\" are not in reference to the AAMC program. Case-sensitive searching could weed out many false positives, but most research databases and search engines are not case sensitive. These programs were designed to make it easier to go through search results and to identify which matches of search terms are more likely to be true positives and which are more likely to be false positives. They do so using regular expressions, so these programs could be adapted to locate other case-sensitive terms.

## Prerequsites

You do not need to know Python to use these programs. However, your computer must meet the following requirements:

* Have Python installed. (AAMC staff can do this through the Software Center. Others can do so from [Python's downloads page](https://www.python.org/downloads/ 'Download Python | Python.org').)
* Have the necessary third-party Python modules installed. (For tips on installing third-party modules, see \"[Installing Python Modules](https://docs.python.org/3/installing/index.html 'Installing Python Modules — Python 3.10.6 documentation').\") The needed modules vary by program:
    * _cim-scraper.py_:
        * beautifulsoup4
        * pandas
        * requests
    * _cim-clipboard.py_ and _cim-clipboard_one-doc.py_:
        * pandas
        * pyperclip
        * tabulate

## Programs

### cim-scraper.py

If you are searching many webpages and can list the URLs in a CSV document, consider [__cim-scraper.py__](https://github.com/referencecenter/cim/blob/main/cim-scraper.py 'cim/cim-scraper.py at main • referencecenter/cim'), which attempts to scrape each page to determine which are more likely to include references to CiM. To use it, follow the steps below if you are on a Windows desktop. The steps may need to be adapted for other devices.

1. Make necessary changes to the script (see instructions at the beginning of the script).
2. Run the program.

### cim-clipboard.py

[__cim-clipboard.py__](https://github.com/referencecenter/cim/blob/main/cim-clipboard.py 'cim/cim-clipboard.py at main • referencecenter/cim') is ideal for when you are going through multiple search results in one sitting. To use it, follow the steps below if you are on a Windows desktop. The steps may need to be adapted for other devices.

1. Start the program.
2. Go to the first result you want to check.
3. Highlight the entire document by pressing Ctrl + A or by right-clicking and selecting \"Select All.\"
4. Copy the entire document by pressing Ctrl + C or by right-clicking and selecting \"Copy.\"
5. Return to the cim-clipboard.py window and press \"Enter.\"
6. The program will search the text you copied, tell you what the matches were, and group them into more likely true positives, possible true positives, and probable false positives. Review the output, and if you like, locate it in the document with your browser\'s or your application\'s Find function by pressing Ctrl + F or by right-clicking and selecting \"Find.\"
7. Repeat steps 2–6 for additional results.
8. When you are finished, type anything and press \"Enter.\" The program will tell you how many texts you searched. Press \"Enter\" again to close the program.

### cim-clipboard_one-doc.py

[__cim-clipboard\_one-doc.py__](https://github.com/referencecenter/cim/blob/main/cim-clipboard_one-doc.py 'cim/cim-clipboard_one-doc.py at main • referencecenter/cim') is ideal for when you are just checking a single document. To use it, follow the steps below if you are on a Windows desktop. The steps may need to be adapted for other devices.

1. Highlight the entire document by pressing Ctrl + A or by right-clicking and selecting \"Select All.\"
2. Copy the entire document by pressing Ctrl + C or by right-clicking and selecting \"Copy.\"
3. Start cim-clipboard\_hotkeys.py. It will search the text you copied, tell you what the matches were, and group them into more likely true positives, possible true positives, and probable false positives. Review the output, and if you like, locate it in the document with your browser\'s or your application\'s Find function by pressing Ctrl + F or by right-clicking and selecting \"Find.\"
4. Press \"Enter\" to close the program.

## Limitations

These programs do not search text copied from PDFs very effectively. For PDFs, you may need to use your browser\'s or your application\'s Find function by pressing Ctrl + F or by right-clicking and selecting \"Find," then searching for \"careers in medicine,\" "\cim\" and \"medcareers.\"
