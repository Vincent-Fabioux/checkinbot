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
keywords["YES"] = ["yes", "sure", "yeah", "yep", "exactly", "absolutely"]

# To express disapproval
keywords["NO"] = ["no", "nope", "never", "not"]

# To express a mistake
keywords["MISTAKE"] = ["sorry", "mean", "meant", "oops"]

# To trigger a generic answer "I'm here to help you..."
keywords["GENERIC"] = ["book", "order", "flight", "flights"]

# Small keywords to be ignored
keywords["SM"] = ["the", "a", "of", "'s", "in", "on"]

# Keywords related to departure
keywords["DEP"] = ["from", "departure", "take off", "taking off"]

# Keywords related to arrival
keywords["ARR"] = ["to", "arrival", "arrive", "land", "landing"]

# Keywords that express thanks
keywords["THANKS"] = ["thanks", "thank you"]

# Influence of one word over another is defined by infDecrease^distance
# Only meaningfull words (eg DEP or ARR) are taken into account
infDecrease = 0.5


def guess(sent, data):
  # Replacement of known keywords with their defined key
  for key, values in keywords.items():
    for value in values:
      sent = re.sub(r"\b" + value + r"\b", key, sent)

  # Unknown words become "UNK"
  sent = re.sub(r"\b[^A-Z ]+\b", "UNK", sent)
  print(sent)

  # Some values have higher odds of being defined by the user:
  # - Values not already defined in previous sentences
  # - Value specifically asked by the bot
  oddsMult = {}
  for key, value in data.items():
    if value == None:
      oddsMult[key] = 1
    else:
      oddsMult[key] = 2

  words = sent.split(" ")

  # Odds and position of values
  odds = []
  dataPos = []
  for i in range(0, len(words)):
    if re.match("^[A-Z]+_", words[i]):
      dataPos.append(i)
      odds.append(calculateOdds(words, i, data))


  # Chosing where values goes according to odds
  for i in range(0, len(dataPos)):
    value = words[dataPos[i]]
    start = value.split("_")[0]
    if start == "P":
      data.update(fillMaxOdds(odds[i], value, ["dep_loc", "arr_loc"]))
    elif start == "D" or start == "NDATE":
      data.update(fillMaxOdds(odds[i], value, ["dep_date", "arr_date"]))
    elif start == "H" or start == "MO":
      data.update(fillMaxOdds(odds[i], value, ["dep_hour", "arr_hour"]))

# Calculate odds for the nth word in a sentence according to previous words
def calculateOdds(words, n, oddsModel):
  odds = {}
  result = dict.fromkeys(oddsModel, 0)

  # Local odds multiplier: effect of distance over odds
  oddsMult = 1

  for i in range(n, 0, -1):
    if words[i] == "DEP":
      odds["dep_loc"] = 1
      odds["dep_date"] = 1
      odds["dep_hour"] = 1
      oddsMult *= infDecrease
    elif words[i] == "ARR":
      odds["arr_loc"] = 1
      odds["arr_date"] = 1
      odds["arr_hour"] = 1
      oddsMult *= infDecrease

    for key, value in odds.items():
      result[key] += value * oddsMult

  return result


# Maps a value with one of the possible keys according to the odds of each key
def fillMaxOdds(odds, newValue, possible):
  maxOdds = None
  toFill = None
  for key, value in odds.items():
    if (key in possible) and (maxOdds == None or value > maxOdds):
      maxOdds = value
      toFill = key

  if toFill == None:
    return None
  else:
    return {toFill: newValue}


# Only for debugging purposes
def guessDebug():
  # Data before test
  data = {"dep_loc": None, "dep_date": None, "dep_hour": None,
      "arr_loc": None, "arr_date": None, "arr_hour": None}

  # Dynamic test
  from src.normalize import normalize
  from src.extract import extract
  testSentences = [input("Enter a sentence to test: ")]
  testSentences[0] = extract(normalize(testSentences[0]))

  # If extract() or normalise() are not working properly, it is best to use
  # hand made sentences rather than calling those functions
  # testSentences = ["good morning !",
  #    "i'd like to book a flight",
  #    "from P_Paris to P_Dublin at D_030403"]

  # Prints data after the tests
  for values in testSentences:
    print("=> " + values)
    guess(values, data)
    print(data)
