"""
This function answers to the user given inputs. Data is a dictionary that contains
the informations about the flight such as departure location, arrival, etc. while
modified is used to know if a given information has changed in Data.
This function uses guess.py to evaluate the word that is weighting the most,
as a way to try to grab the meaning of the inputed sentence.
"""


import re
import random

# This dictionary contains answers to most things that a user can say as an answer to one of our questions
answers = {}

answers["HI"] = ["Hello !", "Nice to meet you !", "Hi !","Welcome !"]

answers["BYE"] = ["Good bye !", "Bye !","Have a nice day !"]

answers["YES"] = ["Ok very nice.", "Understood.", "Perfect.", "Ok fine."]

answers["NO"] = ["Sorry to hear.", "We can fix that.", "My apologies.","That's embarassing."]

answers["MISTAKE"] = ["No problem.", "It's ok, one more time.", "Don't worry it happens.","Haha no problem."]

answers["HIBOOL"] = False


def answer(data):

#Data can contain a key named 'special' with values hi,bye,yes,no,mistake
  answer = ""

  # If the user says something like "Hello !", special will be set and we will first answer to that.
  if data["special"] != None:
    if data["special"] == "hi" and answers["HIBOOL"] == False:
      answer += random.choice(answers["HI"]) + ' '
      answers["HIBOOL"] = True

    elif data["special"] == "bye":
      answer += random.choice(answers["BYE"]) + ' '
      return False;

    elif data["special"] == "yes":
      answer += random.choice(answers["YES"]) + ' '
      return True;

    elif data["special"] == "no":
      answer += random.choice(answers["NO"]) + ' '
      return True;

    elif data["special"] == "mistake":
      answer += random.choice(answers["MISTAKE"]) + ' '
      return True;

# We give to the user a recap each time if he already inputed something
  if informationsMissing(data) < 6:
    answer += "As a recap, here are the informations you have inputed :\n"
    if data["dep_loc"] != None:
      answer += "- Departure location : " + data["dep_loc"] + "\n"
    if data["dep_date"] != None and data["dep_hour"] == None:
      answer += "- Departure date : " + data["dep_date"] + " at any hour\n"
    elif data["dep_date"] != None and data["dep_hour"] != None:
      answer += "- Departure date : " + data["dep_date"] + " at " + data["dep_hour"] + "\n"
    if data["arr_loc"] != None:
      answer += "- Arrival location : " + data["arr_loc"] + "\n"
    if data["arr_date"] != None and data["arr_hour"] == None:
      answer += "- Arrival date : " + data["arr_date"] + " at any hour\n"
    elif data["arr_date"] != None and data["arr_hour"] != None:
      answer += "- Arrival date : " + data["arr_date"] + " at " + data["arr_hour"] + "\n"

  # If nothing has been modified nor inputed relative to the flight, we give instructions
  if informationsMissing(data) > 0:
    if informationsMissing(data) == 6:
      answer += "Please provide the following informations to book your flight :\n"
    elif informationsMissing(data) > 1 and (data["dep_loc"] == None or data["dep_date"] == None
    or data["arr_loc"] == None or data["arr_date"] == None):
      answer += "The following informations are still missing :\n"
    if data["dep_loc"] == None:
      answer += "- Your departure location\n"
    if data["dep_date"] == None:
      answer += "- The departure date\n"
    if data["dep_hour"] == None:
      answer += "- The departure hour (Optional)\n"
    if data["arr_loc"] == None:
      answer += "- Your arrival location\n"
    if data["arr_date"] == None:
      answer += "- The arrival date\n"
    if data["arr_hour"] == None:
      answer += "- The arrival hour (Optional)\n"

  print(answer)
  return True  


def answerDebug():
  data = {"dep_loc": None, "dep_hour": None,
    "arr_loc": None, "arr_hour": None, "dep_date": None, "arr_date": None, "special":"hi"}
  Res = answer(data)


def informationsMissing(data):
  count = 0
  specials = {"hi","yes","no","mistake","bye"}
  for info in data.values():
    if info == None and info not in specials:
      count = count + 1

  return count
  
def transform(word):
  if re.match(r'^P_(.*)$', word):
    temp = re.search(r'^(P_(.*))$', word).group(0)
    temp = temp.replace("1", " ")
    temp = temp.replace("2", "_")
    temp = temp.replace("3", "'")
    temp = temp.replace("4", ".")
    return (temp[2:])
  elif re.match(r'^MO_(\d{12})$', word):
    temp = re.search(r'^(MO_(\d{12}))$', word).group(0)
    return (temp[3:5] + ":" + temp[5:7] + ":" + temp[7:9] 
        + " - " + temp[9:11] + ":" + temp[11:13] + ":" + temp[13:15])
  elif re.match(r'^D_(\d{8})$', word):
    temp = re.search(r'^(D_(\d{8}))$', word).group(0)
    return (temp[2:4] + "/" + temp[4:6] + "/" + temp[6:10])
  elif re.match(r'^NDATE_(\d{8})$', word):
    temp = re.search(r'^(NDATE_(\d{8}))$', word).group(0)
    return (temp[6:8] + "/" + temp[8:10] + "/" + temp[10:14])
  elif re.match(r'^H_(\d{6})$', word):
    temp = re.search(r'^(H_(\d{6}))$', word).group(0)
    return (temp[2:4] + ":" + temp[4:6] + ":" + temp[6:8])

answerDebug()

if __name__ == "__main__":
	answerDebug()

