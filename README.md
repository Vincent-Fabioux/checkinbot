# checkinbot
This program intends to simulate a flight booking bot. Its goal is to interact
with an user to get all informations about where he wants to go and when, and
to suggest him a flight.

This is a very short project, and as such a lot of improvements could be made.
For example, prices are not taken into account, nor connections or flight class.

## Dependencies
To run this program, you will need
[Python 3](https://www.python.org/)
and a command-line interface. According to how you have setup Python 3's path,
you may need to write `python` instead of `python3` for the commands described
here.

All libraries used are included in the base installation of Python 3.

Data needed to run this program properly is described in the following section.

## Data generation
This program uses a set of cities (which should be near an airport) located in
the `data/cities.txt` file. Names of those cities are separed with newlines and
should only contain alphanumeric characters and spaces.

A flight list is also required in a file named `data/flights.txt`. This file can
be randomly generated using the command `python3 data/generate.py {start}
{end} {number}` where:
* {start} is the earliest possible date for the departure of a flight
* {end} is the latest possible date for the arrival of a flight
* dates should be given in a DD-MM-YYYY format
* {number} is the number of flights generated for each pair of cities
If you test this program with dates outside of dates used for generating
flights, the bot will not be able to find any suitable flight.

The number of flights grows exponentially as you expand the list of cities,
which can make the generation process very long. A good CPU will not make it
quicker, but a faster hard drive will surely help.

## Usage
Navigate to the root of the cloned repository and execute the command `python3
checkinbot`.

You can append -h or --help to see the full list of available commands.

When the program is launched, you will be able to interact with the bot with no
delay. Once you told the bot all required informations, he will give you a
suited fight - if possible - with it's id, dates and hour of departure and
arrival. If you wish to quit the program, just tell it to the bot. If you can't
quit, you can in last ressort hold the Control key and press C.

## Debugging
Appending the -d or --debug option along with a step name (each step has one
file in src/) will launch a debug version of that particular step. This allows
the testing of a particular function with particular data without the need of
proper functionning of other functions.

For example, `python3 checkinbot -d tokenise` will execute tokeniseDebug() from
`src/tokenise.py`.
