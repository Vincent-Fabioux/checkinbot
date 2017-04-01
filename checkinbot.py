import argparse

from src.tokenise import tokenise, tokeniseDebug
from src.guess import guess, guessDebug
from src.extract import extract, extractDebug

def main():
    # Command line arguments recovery for debug mode
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", type=str,
            choices = ["tokenise", "guess", "extract"],
            help = "enter debug mode for one of the steps")
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
