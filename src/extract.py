import mysql.connector
import re
import datetime
from datetime import date
from datetime import time

def extract(listTokens):
    # Création de la phrase
    sentence = ' '.join(listTokens)

    # Initialisation des listes connues
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    indication = {'day' : 1, 'days' : 1, 'week' : 7, 'weeks' : 7, 'months' : 365/12, 'month' : 365/12, 'year' : 365, 'years' :365}
    month = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    places = getCountries() + getCities()

    for element in sentence.split():
      # Ajout des éléments de lieux
      if element in places:
        sentence = re.sub(element, "P-" + element, sentence)
      # Ajout des éléments d'heures spécifiques
      elif element == "morning":
        sentence = re.sub("morning","MOD- 05:00:0012:00:00", sentence)
      elif element == "afternoon":
        sentence = re.sub("afternoon","MOD- 12:00:00-17:00:00", sentence)
      elif element == "evening":
        sentence = re.sub("evening","MOD- 17:00:00-21:00:00", sentence)
      elif element == "night":
        sentence = re.sub("night","MOD- 21:00:00-05:00:00", sentence)
      elif element == "midnight":
       sentence = re.sub("midnight","H- 00:00:00", sentence)
      elif element == "noon":
        sentence = re.sub("noon","H- 12:00:00", sentence)
      elif element == "today":
        sentence = re.sub("today","D- "+ str(date.today().day) + "/" + str(date.today().month) + "/" + str(date.today().year), sentence)  
      elif element == "tomorrow":
        sentence = re.sub("tomorrow","D- "+ str(int(date.today().day + 1)) + "/" + str(date.today().month) + "/" + str(date.today().year), sentence)
      # Ajout des éléments de dates concernant les jours de la semaine (du type Monday, Tuesday)
      elif element in days:
        regex = r'((next\s*)?' + element + ')'
        sentence = re.sub(regex,calculateDateDay(regex, element, sentence),sentence)
      # Ajout des éléments de dates spécifiques (du type day, week, months, years)
      elif element in indication.keys():
        regex= r'((next\s*)?\s*(\d)?\s*' + element + ')'
        sentence = re.sub(regex, calculateDateIndication(indication.get(element), regex, element, sentence),sentence)
      
    
     # Heures de la forme 16:00:00 a.m
    regex = r'(?:^|\s)(\d{1,2})\s*:(\s*\d{1,2}):(\s*\d{1,2})\s*([.]?(a|p)\s*[.]?\s*m[.]?)?[^\d:]'
    matchs = re.findall(regex, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 3:
          if re.search(r'a', match[3]):
            sentence = re.sub(regex," H-" + match[0] + ":" + match[1] + ":" + match[2]+ " ", sentence)
          elif re.search(r'p', match[3]):
            sentence = re.sub(regex," H-" + str(int(match[0]) + 12) + ":" + match[1] + ":" + match[2]+ " ", sentence)
          else:
            sentence = re.sub(regex," H-" + match[0] + ":" + match[1] + ":" + match[2] + " ", sentence)
    
    # Heures de la forme 16:00 a.m
    regex = r'(?:^|\s)(\d{1,2})\s*:(\s*\d{1,2})[^\d:]\s*([.]?(a|p)\s*[.]?\s*m[.]?)?'
    matchs = re.findall(regex, sentence)
    if matchs:
      for match in matchs:
        if len(match) > 3:
          print (match)
          if re.search(r'a', match[3]):
            sentence = re.sub(regex," H-" + match[0] + ":" + match[1] +":00", sentence)
          elif re.search(r'p', match[3]):
            sentence = re.sub(regex," H-" + str(int(match[0]) + 12) + ":" + match[1] + ":00", sentence)
            print (str(int(match[0]) + 12))
          else:
            sentence = re.sub(regex," H-" + match[0] + ":" + match[1] + ":00", sentence)
    
    
    # Heures de la forme 16 a.m
    regex = r'([0-9]{1,2})\s*([.]?(a|p)\s*[.]?\s*m[.]?)'
    matchs = re.findall(regex, sentence)
    for match in matchs:
      if match:
        if len(match) > 1:
          if re.search(r'a', match[1]):
            sentence = re.sub(regex,"H-" + match[0] + ":00:00", sentence)
          elif re.search(r'p', match[1]):
            sentence = re.sub(regex,"H-" + str(int(match[0]) + 12) + ":00:00", sentence)
    
    return sentence

def extractDebug():
    print ("A vous de tester des phrases : Rentrez les sous forme d'une liste de tokens")

def calculateDateDay(regex, element, sentence):
  d = datetime.date.today()
  days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
  while d.weekday() != days.index(element):
    d += datetime.timedelta(1)
  day = str(d.day) + "/" + str(d.month) + "/" + str(d.year)
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
        return " ND-" + str(d.day) + "/" + str(d.month) + "/" + str(d.year)
      else:
        d = datetime.date.today() + datetime.timedelta(typeDate)
        return " ND-" + str(d.day) + "/" + str(d.month) + "/" + str(d.year)
    elif match.group(3):
      d = datetime.date.today() + datetime.timedelta(typeDate * int(match.group(3)))
      return " D-" + str(d.day) + "/" + str(d.month) + "/" + str(d.year)
  
def getCountries():
    countries = []
    conn = mysql.connector.connect(host="localhost",user="root",password="root", database="flights", unix_socket="/opt/lampp/var/mysql/mysql.sock")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM countries")
    rows = cursor.fetchall()
    for row in rows:
        countries.append(row[0].lower())
    conn.close()
    return countries;
    
def getCities():
    cities = []
    conn = mysql.connector.connect(host="localhost",user="root",password="root", database="flights", unix_socket="/opt/lampp/var/mysql/mysql.sock")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cities")
    rows = cursor.fetchall()
    for row in rows:
        cities.append(row[0].lower())
    conn.close()
    return cities;
