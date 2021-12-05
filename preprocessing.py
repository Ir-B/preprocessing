# -*- coding: utf-8 -*-
"""
Function ('proprocessing') for preprocessing the text in a database with class attribute and text attribute.
It can be executed from the Terminal.
A supplementary function ("try_regex") is provided to help you adapt the regex used in the preprocessing function.

@author: Irene
"""

import pandas as pd
import re
import argparse


def preprocessing(fin, fout):
    """
    Function that takes a tsv with two columns (class attribute and text) as input
    and outputs a csv with the preprocessed version of the text. The proprocessing
    steps are explained as comments.
    """
    
    db_spam = pd.read_csv(fin, sep='\t', names=["class_attribute", "text"], index_col=None)
    db_spam = db_spam[["text", "class_attribute"]]
    db_spam["text"] = db_spam["text"].astype(str)
    db_spam["text"] = db_spam["text"].str.replace(r"['\"]", ' ')
    
    # We remove error symbols
    db_spam["text"] = db_spam["text"].str.replace(r'(&lt;#&gt;|&lt;3|&lt;\w+&gt;)', ' ')
    
    
    # We group some words to become a single attribute:
    
    # 1) email addresses
    db_spam["text"] = db_spam["text"].str.replace(r'\b[A-Za-z0-9_]+@\s?[A-Za-z0-9_\.]+($|\s|\.|,|\b|\W)', ' email_address ')    
    
    # 2) url addresses
    db_spam["text"] = db_spam["text"].str.replace(r'(?:(?:https?)?[://]*)?(?:www\.)?[a-zA-Z0-9@:%._\-\+~#=]+\.(com|org|co|net|gr|COM)(\s|$|[^a-zA-Z0-9]\S*)',' url_address ')
    
    # 3) money
    db_spam["text"] = db_spam["text"].str.replace(r'((([£|\$|gbp?|GBP?]?\d+[\.|,]\d+|[£|\$|gbp?|GBP?]\d+:\d+)(ppm|pm|p\/[a-zA-Z]+|per\w+|p|P|\spounds))|(([£|\$|gbp?|GBP?]\d+[\.|,|\s.]\d+))|([£|\$|gbp?|GBP?]?\d+(ppm|p\/[a-zA-Z]+|per\w+|p|P|\spounds|\s?gbp?|\s?GBP?))|([£|\$|gbp?|GBP?]\d+(/[a-zA-Z]*)?))', ' money_expression ')    
    
    # 4) codes
    db_spam["text"] = db_spam["text"].str.replace(r'([A-Z]+[a-zA-Z]*\d+[a-zA-Z0-9]*[A-Z]+\d*|(Code|code|CODE):?\s?\d{4,5}|\d{4,5}(Code|code|CODE))', ' code_expression ')
    
    # 5) phone numbers
    db_spam["text"] = db_spam["text"].str.replace(r'(\b\d{9,12}|\b\d{5}\b|\d{3,4}(\s|(\s?-\s?))?\d{3,4}(\s|(\s?-\s?))?\d{3,4})',' phone_number ')    
    
    # 6) emoticons
    db_spam["text"] = db_spam["text"].str.replace(r':\s\-\sP|:\-D|;\-\)|:\-\)|:\)|;\)|:\(', ' emoji_expression ')
    
    # 7) age_required
    db_spam["text"] = db_spam["text"].str.replace(r'16+|18+', ' age_required ')
    
    
    # We create a space before and after these symbols to (maybe) profit them
    db_spam["text"] = db_spam["text"].str.replace(r"\s*\*\s*", " * ")
    db_spam["text"] = db_spam["text"].str.replace(r"\s*&\s*", " & ")
    db_spam["text"] = db_spam["text"].str.replace(r"\s*\+\s*", " + ")
    db_spam["text"] = db_spam["text"].str.replace(r"\s*\-\s*", " - ")
    db_spam["text"] = db_spam["text"].str.replace(r"\s*\#\s*", " # ")
    
    
    # We remove excessive white spaces
    db_spam["text"] = db_spam["text"].str.replace(r'\s+', ' ')
    db_spam["text"] = db_spam["text"].str.replace(r'^\s+|\s+?$', '')
    
    # We save the csv
    fout = open(fout, "w")
    
    db_spam.to_csv(fout, sep = ',', index=False)

    fout.close()
    
# Parser configuration
parser = argparse.ArgumentParser(description="Given a tsv input file with two columns (class attribute and text), it outputs a preprocessed version of the text. Provide the path for the input and the output.")
parser.add_argument('-i',"--input",help="input file",required=True)
parser.add_argument('-o',"--output",help="output file",required=True)
args = parser.parse_args()

preprocessing(args.input, args.output)



def try_regex(p_words, p_regex):
    for word in p_words:
        clean_word = re.sub(p_regex, "OK", word) 
        print(word, "-->", clean_word)

# Regex to try    
regex = r'(\b\d{9,12}|\b\d{5}\b|\d{3,4}(\s|(\s?-\s?))?\d{3,4}(\s|(\s?-\s?))?\d{3,4})'

# Examples to try on
wep_pages = ["www.areyouunique.co.uk", "Si.como", "www.getzed.co.uk", "www.07781482378.com", "www.smsco.net", "www.100percent-real.com", "lucozade.co.uk/wrc", "sextextuk.com", "www.txt82228.com.", "fullonsms.com", "WAY2SMS.COM"]
email = ["Dorothy@kiefer.com", "yijue@hotmail.com", "tddnewsletter@emc1.co.uk", "info@vipclub4u", "customersqueries@netvision.uk.com", "info@vipclub4u.", "olowoyey@ usc.edu", "info@txt82228.co.uk"]
money = ["20p/min", "£1000", "150p","10p/min","$700","£100","150P","£1.50pm","150ppm", "max£7. 50", "£1250", "$50","150p","£1.50perWKsub","£2,000","25p","£5/month","150p/Msg","150p/meg.","150p/day","20,000 pounds","10ppm","£33:50"]
phone_num = ["82242 Hlp 08712317606 Msg150p", "0871 - 4719 - 523","02073162414","0800 169 6031", "84025", "09061104283","087018728737","0871-872-9758","07821230901"]
emojis = [":-D",";-)",":-)",":)",";)",":("]
codes = ["PoBox75LDNS7","K52","BOX95QU", "M221BP","W111WX","W1J6HL","CR01327BT", "code 3100"]


# Try a regex as in this example: try_regex(phone_num, regex)




