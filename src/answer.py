
import re
import random

answers = {}

answers["HI"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["BYE"] = ["Good bye !", "Bye !"]

answers["YES"] = ["Ok very nice.", "Understood.", "Perfect."]

answers["NO"] = ["", "Nice to meet you !", "Hi !"]

answers["MISTAKE"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["HIBOOL"] = False


def answer(data,modified = None):

#Data can contain a key named 'special' with values hi,bye,yes,no,mistake

  answer = ""

  if "special" in data:
    if data["special"] == "hi" and answers["HIBOOL"] == False:
      answer += random.choice(answers["HI"]) + ' '
      answers["HIBOOL"] = True

    elif data["special"] == "bye":
      answer += random.choice(answers["BYE"]) + ' '
      return False;


  if modified != None:
    answer += "You changed your "
    if modified == "dep_loc":
      answer += "departure location"
    elif modified == "arr_loc":
      answer += "arrival location"
    elif modified == "dep_hour":
      answer += "departure hour"
    elif modified == "arr_hour":
      answer += "arrival hour"

    answer += ", is that correct ?"

  print(answer)
  return True


def answerDebug():
  data = {"dep_loc": None, "dep_hour": None,
    "arr_loc": None, "arr_hour": None, "special":"hi"}
  Res = answer(data,"dep_loc")

answerDebug()