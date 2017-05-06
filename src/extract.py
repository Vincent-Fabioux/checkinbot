import re
import os.path
import datetime
from datetime import date 

def extract(sentence):

    # Initialization of known lists
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    indication = {'day' : 1, 'days' : 1, 'week' : 7, 'weeks' : 7, 'months' : 365/12, 'month' : 365/12, 'year' : 365, 'years' :365}
    month = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    regexMonths = r'(january|february|march|april|may|june|july|august|september|october|november|december)'
    
    # Get places from the files of cities
    places = getCities()

    # <----SIMPLE ELEMENTS---->
    
    for element in sentence.split():
      # Adding specific time elements
      if element == "morning":
        sentence = re.sub("morning","MO_050000120000", sentence)
      elif element == "afternoon":
        sentence = re.sub("afternoon","MO_120000170000", sentence)
      elif element == "evening":
        sentence = re.sub("evening","MO_170000210000", sentence)
      elif element == "night":
        sentence = re.sub("night","MO_210000050000", sentence)
      elif element == "midnight":
       sentence = re.sub("midnight","H_000000", sentence)
      elif element == "noon":
        sentence = re.sub("noon","H_120000", sentence)
      elif element == "today":
        sentence = re.sub("today","D_"+ str(date.today().day).zfill(2)  + str(date.today().month).zfill(2)  + str(date.today().year).zfill(4) , sentence)  
      elif element == "tomorrow":
        sentence = re.sub("tomorrow","D_"+ str(int(date.today().day + 1)).zfill(2)  + str(date.today().month).zfill(2)  + str(date.today().year).zfill(4) , sentence)
      # Adding dates elements for days of the week (type Monday, Tuesday)
      elif element in days:
        regex = r'((next\s*)?' + element + ')'
        sentence = re.sub(regex,calculateDateDay(regex, element, sentence),sentence)
      # Adding specific dates elements (du type day, week, months, years)
      elif element in indication.keys():
        regex= r'((next\s*)?\s*(\d)?\s*' + element + ')'
        sentence = re.sub(regex, calculateDateIndication(indication.get(element), regex, element, sentence),sentence)
    
    
    # <----PLACES---->
    
    # Adding places
    for place in places:
      if place.lower() in sentence:
        temp = place.lower()
        temp = temp.replace(" ", "1")
        temp = temp.replace("_", "2")
        temp = temp.replace("'", "3")
        temp = temp.replace(".", "4")
        sentence = re.sub(place.lower(), "P_" + temp, sentence)
    
    # <----HOURS---->
    
    # Regexs for hours
    regexThreeDigits = '(\d{1,2})\s*:(\s*\d{1,2})\s*:(\s*\d{1,2})\s*'
    regexTwoDigits = '(\d{1,2})\s*:(\s*\d{1,2})\s*'
    regexOneDigit = '(\d{1,2})\s*'
    regexFormatHour = r'((H|HPM)_(\d{1,2}) (\d{1,2}) (\d{1,2}))' 
    
    # Hours format 16:00:00 am
    sentence = re.sub(r'(' + regexThreeDigits + 'am)',r'H_\2 \3 \4', sentence)
    sentence = re.sub(r'(' + regexThreeDigits + 'pm)',r'HPM_\2 \3 \4', sentence)
    sentence = re.sub(r'(' + regexThreeDigits + ')',r'H_\2 \3 \4 ', sentence)
    
    # Hours format 16:00 am
    sentence = re.sub(r'(' + regexTwoDigits + 'am)',r'H_\2 \3 00', sentence)
    sentence = re.sub(r'(' + regexTwoDigits + 'pm)',r'HPM_\2 \3 00', sentence)
    sentence = re.sub(r'(' + regexTwoDigits + ')',r'H_\2 \3 00 ', sentence)
    
    # Hours format 16 am
    sentence = re.sub(r'(' + regexOneDigit +'am)',r'H_\2 00 00', sentence)
    sentence = re.sub(r'(' + regexOneDigit +'pm)',r'HPM_\2 00 00', sentence)
    
    # Convert hours in the correct format (i.e when there isn't two digits add them)
    matchs = re.findall(regexFormatHour, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 4:
          if match[1] == "HPM":
            sentence = re.sub(match[0],'H_' + (str(int(match[2]) + 12)).zfill(2)  + match[3].zfill(2)  + match[4].zfill(2), sentence)
          else:
            sentence = re.sub(match[0],'H_' + match[2].zfill(2)  + match[3].zfill(2)  + match[4].zfill(2), sentence) 
    
    # Time Interval
    regexInterval = r'H_(\d{1,2}\d{1,2}\d{1,2})\s*_\s*H_(\d{1,2}\d{1,2}\d{1,2})'
    sentence = re.sub(regexInterval,r'MO_\1\2', sentence)
    
    # <----DATES---->
    
    # Regexs for dates
    regexDMY = r'(\d{1,2})\s*\/\s*(\d{1,2})\s*\/\s*(\d{4})'
    regexMY = r'(\d{1,2})\s*\/\s*(\d{4})'
    regexDM = r'(\d{1,2})\s*\/\s*(\d{1,2})'
    regexCompleteDate = r'(\d{1,2})\s*(th)?\s*(of)?\s*' + regexMonths + r'\s*(\d{4})'
    regexMonth = r'(\d{1,2})\s*(th)?\s*(of)?\s*' + regexMonths
    regexFormatDate = r'(D_(\d{1,2})(\d{1,2})(\d{4}))'
    regexFormatDate2 = r'(D_(\d{1,2})_'+ regexMonths + r'_?(\d{4})?)'
        
    # Application of the regexs
    sentence = re.sub(regexDMY, r'D_\1\2\3', sentence)
    sentence = re.sub(regexMY, r'D_01\1\2', sentence)
    sentence = re.sub (regexDM, r'D_\1\2 ' + str(date.today().year), sentence)
    sentence = re.sub (r'D_(\d{1,2})(\d{1,2})\s*(\d{1,2})', r'D_\1\2\3', sentence)
    
    # Convert dates in the correct format
    matchs = re.findall(regexFormatDate, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 3:
          sentence = re.sub(match[0],'D_' + match[1].zfill(2)  + match[2].zfill(2)  + match[3].zfill(2), sentence) 
    
    # Application of the regexs with months written in letters
    sentence = re.sub(regexCompleteDate, r'D_\1_\4_\5', sentence)
    sentence = re.sub(regexMonth, r'D_\1_\4', sentence)
    matchs = re.findall(regexFormatDate2, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 3:
          if match[3]:
            sentence = re.sub(match[0],'D_' + match[1].zfill(2)  + str(month.index(match[2]) + 1).zfill(2)  + match[3].zfill(4), sentence)
          else:
            sentence = re.sub(match[0],'D_' + match[1].zfill(2)  + str(month.index(match[2]) + 1).zfill(2)  + str(date.today().year).zfill(2), sentence)
    
    
    
    # Return the modified sentence
    return sentence

def extractDebug():
  print("")

# Function that returns a date of day of the week (on Monday, on Friday, etc.)
def calculateDateDay(regex, element, sentence):
  d = datetime.date.today()
  days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
  while d.weekday() != days.index(element):
    d += datetime.timedelta(1)
  day = str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
  match = re.search(regex, sentence)
  if match:
    if match.group(2):
      return "NDATE_" + day
    else:
      return "D_" + day

# Function that returns a date from an user indication (5 days, 2 months, etc.)
def calculateDateIndication(typeDate, regex, element, sentence):
  match = re.search(regex, sentence)
  if match:
    if match.group(2):
      if match.group(3):
        d = datetime.date.today() + datetime.timedelta(typeDate * int(match.group(3)))
        return " NDATE_" + str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
      else:
        d = datetime.date.today() + datetime.timedelta(typeDate)
        return " NDATE_" + str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
    elif match.group(3):
      d = datetime.date.today() + datetime.timedelta(typeDate * int(match.group(3)))
      return " D_" + str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 

# Function that return the list of cities
def getCities():
  with open(os.path.dirname(__file__) + "/../data/cities.txt") as f:
    countries = f.readlines()
  content = [x.strip() for x in countries] 
  return content
  
