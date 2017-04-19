"""
This function guesses which type of informations (date of departure, location
of departure, date of arrival, etc) the user wants to communicate to the bot
according to previously obtained informations (namely 'data') and the previous
question (namely 'question') the bot asked to that user.
"""


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
keywords["GENERIC"] = ["book", "order", "flight"]

# Keywords related to departure
keywords["DEP"] = ["from", "departure"]

# Keywords related to arrival
keywords["ARR"] = ["to","arrival","arrive","land"]

#keywords that express thanks
keywords["THANKS"] = ["thanks", "thank you"]


def guess(words, data, question):
  oddsMult = {} # Odd multipliers for each type of informations
  for key, value in data.items():
    # If a value has never been told, odds that the user wants to tell it
    # are higher
    if value == None:
      oddsMult[key] = 3
    else:
      oddsMult[key] = 1
  # If the bot specifically asked for a value, odds that the user wants to
  # tell that value are higher
  if question != None:
    oddsMult[question] *= 2
        

def guessDebug():
  data = {"dep_loc": None, "dep_hour": None,
      "arr_loc": None, "arr_hour": None}
  testSentences = [["i'd", "like", "to", "book", "a", "flight"],
      ["from", "paris", "to", "dublin"]]
  for values in testSentences:
    print(values)
    print(guess(values, data, "dep_loc"))
