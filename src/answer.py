
import re
import random

answers = {}

answers["HI"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["BYE"] = ["Good bye !", "Bye !"]

answers["YES"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["NO"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["MISTAKE"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["HIBOOL"] = False


def answer(data,modified = None):

#Data can contain a key named 'special' with values hi,bye,yes,no,mistake

  answer = ""

  if "special" in data:
    if data["special"] == "bye":
      answer += random.choice(answers["BYE"])
      return False;
    if data["special"] == "hi" and answers["HIBOOL"] == False:
      answer = random.choice(answers["HI"])
      answers["HIBOOL"] = True

    print(answer)

  return True


def answerDebug():
  data = {"dep_loc": None, "dep_hour": None,
      "arr_loc": None, "arr_hour": None, "special":"hi"}
  Res = answer(data)

answerDebug()