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

from src.tokenise import tokenise, tokeniseDebug
from src.guess import guess, guessDebug
from src.extract import extract, extractDebug

def main():
    # Command line arguments recovery for debug mode
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", type=str,
            choices = ["tokenise", "guess", "extract"],
            help = "enter debug mode for one of the user input analyse steps")
    args = parser.parse_args()

    if args.debug: # Launch debug mode if specified
        if args.debug == "tokenise":
            tokeniseDebug()
        elif args.debug == "guess":
            guessDebug()
        elif args.debug == "extract":
            extractDebug()
    else: # Launch program as usual
        print("Main not implemented yet.")


# Calling of main loop
if __name__ == "__main__":
   main() 
