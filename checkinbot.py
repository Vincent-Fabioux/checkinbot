#!/usr/bin/env python3
#coding: utf-8

"""
Chatbot which mission is to help book flights.
Long description here.

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


# Main function of the program
def checkinbot():
  data = {"dep_loc": None, "dep_date": None, "dep_hour": None,
      "arr_loc": None, "arr_date": None, "arr_hour": None}
  
  run = True
  while(run):
    userInput = input("> ")
    modified = guess(extract(normalize(userInput)), data)
    run = answer(data, modified)


# Calling of main function
if __name__ == "__main__":
  main() 
