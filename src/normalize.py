"""
This function normalise the input text to generate tokens and use them later on.
"""

import re

def normalize(sent):
    special = ["m","ms","mr","dr","prof","sgt","lt","ltd","co","etc","i.e","e.g","st","d.c"]
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(special)+"))"
    sent = sent.lower() #lower characters
    sent = re.sub("\'\'",r"\"", sent) #transform double simple quote into a normal quote
    sent = re.sub("[`‘’\"≪≫“”]+", r"", sent) #remove quotes
    sent = re.sub("([a-z]{3,})or", r"\1our", sent) #transform words that end in or by our
    sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) #transform words that end in iz by is
    sent = re.sub("(\d+)\s*\.*a\.*m\.*", r"\1 am", sent) #normalize am
    sent = re.sub("(\d+)\s*\.*p\.*m\.*", r"\1 pm", sent) #normalize pm
    sent = re.sub("[\.\?\!\,\;]*\?[\.\?\!\,\;]*", r"?", sent)  #change ?! !? ???? etc. in a simple ?
    sent = re.sub("([\.\?\!\,\;]+)\s*(\w+)", r"\1 \2", sent) #add a space after a coma if the end of the text has not been reached
    sent = re.sub("("+regex_cannot_precede+")\s*([\.\?\!\,\;]+)", r"\1 \2", sent) #add a whitespace after a coma expect in special cases
    sent = re.sub("(.)^\.$", r"\1 .", sent)
    return sent 


def normalizeDebug():
    print(normalize())
