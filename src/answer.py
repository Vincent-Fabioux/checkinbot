
import re
import random

answers = {}

answers["HI"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["BYE"] = ["Good bye !", "Bye !"]

answers["YES"] = ["Ok very nice.", "Understood.", "Perfect.", "Ok fine."]

answers["NO"] = ["Sorry to hear.", "We can fix that.", "My apologies.","That's embarassing."]

answers["MISTAKE"] = ["No problem.", "It's ok, one more time.", "Don't worry it happens.","Haha no problem."]

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

    elif data["special"] == "yes":
      answer += random.choice(answers["YES"]) + ' '
      return False;

    elif data["special"] == "no":
      answer += random.choice(answers["NO"]) + ' '
      return False;

    elif data["special"] == "mistake":
      answer += random.choice(answers["MISTAKE"]) + ' '
      return False;


  if modified != None:
    answer += "You set your "
    if modified == "dep_loc":
      answer += "departure location"
    elif modified == "arr_loc":
      answer += "arrival location"
    elif modified == "dep_hour":
      answer += "departure hour"
    elif modified == "arr_hour":
      answer += "arrival hour"

    answer += " to " + data[modified] + ", is that correct ?"

  elif modified == None and informationsMissing(data) != 0:
    if informationsMissing(data) == 4:
      answer += "Please provide the following informations to book your flight :\n"
    else:
      answer += "The following informations are still missing :\n"
    if data["dep_loc"] == None:
      answer += "- Your departure location\n"
    if data["arr_loc"] == None:
      answer += "- Your arrival location\n"
    if data["dep_hour"] == None:
      answer += "- The departure hour\n"
    if data["arr_hour"] == None:
      answer += "- The arrival hour\n"

  if modified == None and informationsMissing(data) == 0:
    answer += "As a recap, here are the informations you have inputed :\n"
    answer += "- Departure location : " + data["dep_loc"] +"\n"
    answer += "- Arrival location : " + data["arr_loc"] +"\n"
    answer += "- Departure hour : " + data["dep_hour"] +"\n"
    answer += "- Arrival hour : " + data["arr_hour"] +"\n"

  print(answer)
  return True  


def answerDebug():
  data = {"dep_loc": None, "dep_hour": None,
    "arr_loc": None, "arr_hour": None, "special":"hi"}
  Res = answer(data)


def informationsMissing(data):
  count = 0
  infos = data.values()
  for e in infos:
    if e == None:
      count = count + 1

  return count

answerDebug()