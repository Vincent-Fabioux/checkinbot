#!/usr/bin/env python3
#coding: utf-8

"""
checkinbot is a chatbot which mission is to help users book a flight.
This program can understand basic informations about a flight such as
the departure date and location and the arrival date and location.
It then give the user corresponding flights according to a textfile
database.


Homepage and documentation: https://github.com/Vincent-Fabioux/checkinbot
"""

__authors__ = "Vincent Fabioux, Nicolas Montoro, Olivier Nappert"
__version__ = "0.1-dev"
__contact__ = "Vincent Fabioux <vincent.fabioux@u-psud.fr>"

import argparse

from src.normalize import normalize, normalizeDebug
from src.extract import extract, extractDebug
from src.guess import guess, guessDebug
from src.answer import answer, answerDebug

def main():
  # Command line arguments recovery for debug mode
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--debug", type=str,
      choices = ["normalize", "extract", "guess", "answer"],
      help = "enter debug mode for one of the user input analyse steps")
  args = parser.parse_args()

  if args.debug: # Launch debug mode if specified
    if args.debug == "normalize":
      normalizeDebug()
    elif args.debug == "extract":
      extractDebug()
    elif args.debug == "guess":
      guessDebug()
    elif args.debug == "answer":
      answerDebug()
  else: # Launch program as usual
    checkinbot()


# Main program function
def checkinbot():
  data = {"dep_loc": None, "dep_date": None, "dep_hour": None,
      "arr_loc": None, "arr_date": None, "arr_hour": None,
      "special": None}
  
  print("Hi! My name is Checkinbot, I am here to help you book a flight\n"
      + "from any capital city in western Europe to any capital city in\n"
      + "the same zone.\n"
      + "To start things off, could you tell me what is your travel plan?")

  run = True
  while(run):
    userInput = input("> ")
    modified = guess(extract(normalize(userInput)), data)
    run = answer(data)


# Calling of main function
if __name__ == "__main__":
  main() 
