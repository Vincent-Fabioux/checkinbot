#!/usr/bin/env python3
#coding: utf-8

"""
Generates a list of random flights into flights.txt using the list of cities
from cities.txt. Increasing the number of cities will increase the file size
exponentially ; see binomial coefficient calculation for more informations
about 2 lists combinations count. You can also set the number of flights per
city to city pair ; increasing such number will increase the file size in a
linear way.

Format:
City1|City2|flight1_id|departure1_timestamp|arrival1_timestamp|flight2_id|...\n
City1|City3|flight1_id|...

Timestamps are counted in minutes.
"""

__authors__ = "Vincent Fabioux, Nicolas Montoro, Olivier Nappert"
__version__ = "0.1-dev"
__contact__ = "Vincent Fabioux <vincent.fabioux@u-psud.fr>"

import argparse
from datetime import datetime
from itertools import product
from os import path, stat
from random import randint
from sys import stdout


def main():
  # Mandatory command line arguments recovery
  parser = argparse.ArgumentParser()
  parser.add_argument("start", type = str,
      help = "starting date of flights (DD-MM-YYYY)")
  parser.add_argument("end", type = str,
      help = "ending date of flights (DD-MM-YYYY")
  parser.add_argument("number", type = int,
      help = "number of flights per pair of cities")
  args = parser.parse_args()

  number = args.number
  start = int(datetime.strptime(args.start, "%d-%m-%Y").timestamp()/60)
  end = int(datetime.strptime(args.end, "%d-%m-%Y").timestamp()/60)
  interval = end - start
  if interval < 0:
    raise ValueError("Please set a starting date prior to the ending date.")

  print("Generating a list of flights:")

  # Paths of files to use
  citiesPath = path.join(path.dirname(__file__), "cities.txt")
  flightsPath = path.join(path.dirname(__file__), "flights.txt")

  # Loads list of cities from file
  cities = []
  with open(citiesPath, "r") as data:
    for line in data.readlines():
      if line.strip() != "":
        cities.append(line.strip())

  # Generates all combinations of two cities
  cities = [x + "|" + y for x, y in product(cities, cities) if x != y]
  citiesNumber = len(cities)
  
  # Generates wanted flights
  count = 0
  dates = [0, 0]
  with open(flightsPath, "w+") as data:
    for i, city in enumerate(cities):
      data.write(city)
      for j in range(0, number):
        randomDate(start, interval, dates)
        data.write("|" + str(count) + "|" + str(dates[0]) + "|" + str(dates[1]))
        count += 1
      data.write("\n")
      printProgress(i / citiesNumber * 100)
  print("\n\"" + flightsPath + "\" file generated with a size of "
      + "{:,}".format(stat(flightsPath).st_size) + " Bytes.")
  

# Generate two random timestamps between two dates
def randomDate(start, interval, dates):
  rand = randint(0, interval)
  dates[0] = start + rand
  dates[1] = dates[0] + randint(0, interval - rand)


# Prints or update a progression bar with a certain percentage
def printProgress(n):
  sharps = round(n/5)
  stdout.write("\r> [" + "#"*sharps + "-"*(20-sharps) + "] "
      + str(round(n)) + "%")


# Calling of main function
if __name__ == "__main__":
  main() 
