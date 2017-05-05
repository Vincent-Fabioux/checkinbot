
import re
import random

answers = {}

answers["HI"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["BYE"] = ["Good bye !", "Bye !"]

answers["YES"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["NO"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["MISTAKE"] = ["Hello !", "Nice to meet you !", "Hi !"]

answers["HIBOOL"] = [False]


def answer(data,modified = None):

""" Possible que data contienne une clé "special" contenant :
hi,bye,yes,no,mistake
"""
	answer = ""

	if "special" in data:
		if data["special"] == "bye":
			answer += random.choice(answers["BYE"].values())
			return False;
		if data["special"] == "hi" and answers["HIBOOL"] == False:
			answer += random.choice(answers["HI"].values())
			answers["HIBOOL"] = True


	return True
