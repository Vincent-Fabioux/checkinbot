"""
This function guesses which type of informations (date of departure, location
of departure, date of arrival, etc) the user wants to communicate to the bot
according to previously obtained informations (namely 'data') and the previous
question (namely 'question') the bot asked to that user.
"""


import re


# Dictionary mapping keywords to their meaning
keywords = {}

# Because a bot shouldn't ask to repeat when greeted
keywords["HI"] = ["hi", "hello", "good morning", "good afternoon",
    "welcome", "greetings", "nice to meet you"]

# To know when the user wants to end the conversation
keywords["BYE"] = ["goodbye", "good bye", "bye", "exit", "quit"]

# To confirm informations or to confirm quitting the app
keywords["YES"] = ["yes", "sure", "yeah", "yep","exactly","absolutely"]

# To express disapproval
keywords["NO"] = ["no", "nope", "never", "not"]

# To express a mistake
keywords["MISTAKE"] = ["sorry", "mean", "meant","oups"]

# To highlight the following words (increase their weight)
keywords["ADVERB"] = ["certainly", "absolutely"]

# To trigger a generic answer "I'm here to help you..."
keywords["GENERIC"] = ["book", "order", "flight", "flights"]

# Small keywords to be ignored
keywords["SM"] = ["the", "a"]

# Keywords related to departure
keywords["DEP"] = ["from", "departure"]

# Keywords related to arrival
keywords["ARR"] = ["to","arrival","arrive","land"]

#keywords that express thanks
keywords["THANKS"] = ["thanks", "thank you"]


def guess(sent, data, question):
  # Replacement of known keywords with their defined key
  for key, values in keywords.items():
    for value in values:
      sent = re.sub(r"\b"+value+r"\b", key, sent)

  # Unknown words become "UNK"
  sent = re.sub(r"\b[^A-Z ]+\b", "UNK", sent)

  # Global multiplier for certain words 
  oddsMult = {}
  for key, value in data.items():
    if value == None:
      oddsMult[key] = 1
    else:
      oddsMult[key] = 2
  if question != None:
    oddsMult[question] = oddsMult[question] * 2

  print(sent)

def guessDebug():
  data = {"dep_loc": None, "dep_hour": None,
      "arr_loc": None, "arr_hour": None}
  testSentences = ["hello ! i would like to book a flight this MO_050000120000 . are there any flights left at H_100000 for P_Paris ?"]
  for values in testSentences:
    print(values)
    print(guess(values, data, "dep_loc"))

guessDebug()