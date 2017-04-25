import re
import os.path
import datetime
from datetime import date 

def extract(sentence):

    # Initialisation des listes connues
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    indication = {'day' : 1, 'days' : 1, 'week' : 7, 'weeks' : 7, 'months' : 365/12, 'month' : 365/12, 'year' : 365, 'years' :365}
    month = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    regexMonths = r'(january|february|march|april|may|june|july|august|september|october|november|december)'
    
    # Récuperation des lieux depuis les fichiers contenant les villes et les pays
    places = getCountries() + getCities()

    # <----ELEMENTS SIMPLES---->
    
    for element in sentence.split():
      # Ajout des éléments d'heures spécifiques
      if element == "morning":
        sentence = re.sub("morning","MO-050000120000", sentence)
      elif element == "afternoon":
        sentence = re.sub("afternoon","MO-120000170000", sentence)
      elif element == "evening":
        sentence = re.sub("evening","MO-170000210000", sentence)
      elif element == "night":
        sentence = re.sub("night","MO-210000050000", sentence)
      elif element == "midnight":
       sentence = re.sub("midnight","H-000000", sentence)
      elif element == "noon":
        sentence = re.sub("noon","H-120000", sentence)
      elif element == "today":
        sentence = re.sub("today","D-"+ str(date.today().day).zfill(2)  + str(date.today().month).zfill(2)  + str(date.today().year).zfill(4) , sentence)  
      elif element == "tomorrow":
        sentence = re.sub("tomorrow","D-"+ str(int(date.today().day + 1)).zfill(2)  + str(date.today().month).zfill(2)  + str(date.today().year).zfill(4) , sentence)
      # Ajout des éléments de dates concernant les jours de la semaine (du type Monday, Tuesday)
      elif element in days:
        regex = r'((next\s*)?' + element + ')'
        sentence = re.sub(regex,calculateDateDay(regex, element, sentence),sentence)
      # Ajout des éléments de dates spécifiques (du type day, week, months, years)
      elif element in indication.keys():
        regex= r'((next\s*)?\s*(\d)?\s*' + element + ')'
        sentence = re.sub(regex, calculateDateIndication(indication.get(element), regex, element, sentence),sentence)
    
    
    # <----LIEUX---->
    
    # Ajout des éléments de lieux
    for place in places:
      sentence = re.sub(place.lower(), "P-" + place.replace(" ", "-"), sentence)
    
    
    # <----HEURES---->
    
    # Regexs pour les heures
    regexThreeDigits = '(\d{1,2})\s*:(\s*\d{1,2})\s*:(\s*\d{1,2})\s*'
    regexTwoDigits = '(\d{1,2})\s*:(\s*\d{1,2})\s*'
    regexOneDigit = '(\d{1,2})\s*'
    regexFormatHour = r'((H|HPM)-(\d{1,2}) (\d{1,2}) (\d{1,2}))' 
    
    # Heures de la forme 16:00:00 am
    sentence = re.sub(r'(' + regexThreeDigits + 'am)',r'H-\2 \3 \4', sentence)
    sentence = re.sub(r'(' + regexThreeDigits + 'pm)',r'HPM-\2 \3 \4', sentence)
    sentence = re.sub(r'(' + regexThreeDigits + ')',r'H-\2 \3 \4 ', sentence)
    
    # Heures de la forme 16:00 am
    sentence = re.sub(r'(' + regexTwoDigits + 'am)',r'H-\2 \3 00', sentence)
    sentence = re.sub(r'(' + regexTwoDigits + 'pm)',r'HPM-\2 \3 00', sentence)
    sentence = re.sub(r'(' + regexTwoDigits + ')',r'H-\2 \3 00 ', sentence)
    
    # Heures de la forme 16 am
    sentence = re.sub(r'(' + regexOneDigit +'am)',r'H-\2 00 00', sentence)
    sentence = re.sub(r'(' + regexOneDigit +'pm)',r'HPM-\2 00 00', sentence)
    
    # Convertir les heures dans le bon format (c'est à dire mettre deux digits quand il n'y en a pas)
    matchs = re.findall(regexFormatHour, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 4:
          if match[1] == "HPM":
            sentence = re.sub(match[0],'H-' + (str(int(match[2]) + 12)).zfill(2)  + match[3].zfill(2)  + match[4].zfill(2), sentence)
          else:
            sentence = re.sub(match[0],'H-' + match[2].zfill(2)  + match[3].zfill(2)  + match[4].zfill(2), sentence) 
    
    # Intervalles d'heures
    regexInterval = r'H-(\d{1,2}\d{1,2}\d{1,2})\s*-\s*H-(\d{1,2}\d{1,2}\d{1,2})'
    sentence = re.sub(regexInterval,r'IH-\1\2', sentence)
    
    
    #~ # <----DATES---->
    
    # Regexs pour les dates (a finir)
    regexDMY = r'(\d{1,2})\s*\/\s*(\d{1,2})\s*\/\s*(\d{4})'
    regexMY = r'(\d{1,2})\s*\/\s*(\d{4})'
    regexDM = r'(\d{1,2})\s*\/\s*(\d{1,2})'
    regexCompleteDate = r'(\d{1,2})\s*(th)?\s*(of)?\s*' + regexMonths + r'\s*(\d{4})'
    regexMonth = r'(\d{1,2})\s*(th)?\s*(of)?\s*' + regexMonths
    regexFormatDate = r'(D-(\d{1,2})(\d{1,2})(\d{4}))'
    regexFormatDate2 = r'(D-(\d{1,2})-'+ regexMonths + r'-?(\d{4})?)'
        
    # Application des regexs
    sentence = re.sub(regexDMY, r'D-\1\2\3', sentence)
    sentence = re.sub(regexMY, r'D-01\1\2', sentence)
    sentence = re.sub (regexDM, r'D-\1\2 ' + str(date.today().year), sentence)
    sentence = re.sub (r'D-(\d{1,2})(\d{1,2})\s*(\d{1,2})', r'D-\1\2\3', sentence)
    
    # Convertir les dates dans le bon format
    matchs = re.findall(regexFormatDate, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 3:
          sentence = re.sub(match[0],'H-' + match[1].zfill(2)  + match[2].zfill(2)  + match[3].zfill(2), sentence) 
    
    #~ # Applications des regexs avec les mois écris en lettres
    #~ sentence = re.sub(regexCompleteDate, r'D-\1-\4-\5', sentence)
    #~ sentence = re.sub(regexMonth, r'D-\1-\4', sentence)
    #~ matchs = re.findall(regexFormatDate2, sentence)
    #~ if matchs:
      #~ for match in matchs:
        #~ if len(match) > 3:
          #~ if match[3]:
            #~ sentence = re.sub(match[0],'D-' + match[1].zfill(2)  + str(month.index(match[2]) + 1).zfill(2)  + match[3].zfill(4), sentence)
          #~ else:
            #~ sentence = re.sub(match[0],'D-' + match[1].zfill(2)  + str(month.index(match[2]) + 1).zfill(2)  + str(date.today().year).zfill(2), sentence)
    #~ 
    #~ 
    #~ 
    # Retour de la phrase modifiée
    return sentence

def extractDebug():
    print ("A vous de tester des phrases : Rentrez les sous forme d'une liste de tokens")
    print (extract("this morning"))

def calculateDateDay(regex, element, sentence):
  d = datetime.date.today()
  days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
  while d.weekday() != days.index(element):
    d += datetime.timedelta(1)
  day = str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
  match = re.search(regex, sentence)
  if match:
    if match.group(2):
      return "ND-" + day
    else:
      return "D-" + day
  
def calculateDateIndication(typeDate, regex, element, sentence):
  match = re.search(regex, sentence)
  if match:
    if match.group(2):
      if match.group(3):
        d = datetime.date.today() + datetime.timedelta(typeDate * int(match.group(3)))
        return " ND-" + str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
      else:
        d = datetime.date.today() + datetime.timedelta(typeDate)
        return " ND-" + str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
    elif match.group(3):
      d = datetime.date.today() + datetime.timedelta(typeDate * int(match.group(3)))
      return " D-" + str(d.day).zfill(2)  + str(d.month).zfill(2)  + str(d.year).zfill(4) 
  
def getCountries():
  with open(os.path.dirname(__file__) + "/../data/countries.txt") as f:
    countries = f.readlines()
  content = [x.strip() for x in countries]
  return content
    
def getCities():
  with open(os.path.dirname(__file__) + "/../data/cities.txt") as f:
    countries = f.readlines()
  content = [x.strip() for x in countries] 
  return content
