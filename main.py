# Joseph Accurso

import tkinter as tk
import requests
import random
import pandas as pd

from stateText import us_state_abbrev
from STATETEXT import us_state_abbrev2

#https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv


# makes the window with dimensions
window = tk.Tk()
window.title('CORONAVIRUS STAT-O-MAKER 3000')
window.geometry('600x600')

#-----------------formatting----------------------

# error classs to throw errors
class errorHandle:
  """
  takes a string statement

  uses functions labeler and printer
  """
  def __init__(self, statement):
    self.statement = statement

  def labeler(entry):
    """
    creates a label with the entered string
    """
    random_Label = tk.Label(window,bd = 10, bg = 'white', text = entry)
    random_Label.place(relx=.5, rely=.292,relwidth = .45, relheight= .05, anchor='center')  

  def printer(statement, window):
    """
    takes a statement and shoots it to the labeler()

    statement comes from class
    """
    error = statement

    errorHandle.labeler(error)


def format_responseState(stateData):
  """
  Formats information given from stateData

  found from URLilizerSt
  """
  try:
    # goes through dictionary and turns abbreviation to full name
    for n in range(len(us_state_abbrev2)):
      st = stateData['state'].lower()
      if us_state_abbrev2[st]:
        state = us_state_abbrev2[st]

    # total data
    # takes information from keys of the json
    totalTests = stateData['totalTestResults']
    totalPositive = stateData['positive']
    totalNegative = stateData['negative']
    totalDeaths = stateData['death']
    totalRecovered = stateData['recovered']

    # new data
    # takes information from keys of the json
    newPosCases = stateData['positiveIncrease']
    newNegCases = stateData['negativeIncrease']
    newDeaths = stateData['deathIncrease']

    # creates a string with defined variables
    total_str = 'State: %s \n\nTotal Tests: %s \nTotal Positive Cases: %s \nTotal Negative Cases: %s \nTotal Deaths: %s \nTotal Recovered: %s \n\n' % (state,totalTests, totalPositive, totalNegative, totalDeaths, totalRecovered)
    
    # creates a string with defined variables
    new_str = 'New Positive Cases: %s \nNew Negative Cases: %s \nNew Deaths: %s' % (newPosCases, newNegCases, newDeaths)

    # combines the strings
    final_str = total_str + new_str
  except:
    # if something fails, this prints
    final_str = 'There was a problem retreiving information.'
  # returns this to the label
  return final_str
  
def format_responseUSA(usaData):
  """
  Formats information given from usaData

  found from URLilizerUSA
  """
  try:
    # set name, no name var in dict
    name = 'United States of America'

    # usa is a dictionary, so [0] is required to work
    # total data
    # takes information from keys of the json of the 1st dict
    usaTotalTests = usaData[0]['totalTestResults']
    usaTotalPositive = usaData[0]['positive']
    usaTotalNegative = usaData[0]['negative']
    usaTotalRecovered = usaData[0]['recovered']
    usaTotalDeaths = usaData[0]['death']

    # new data
    # takes information from keys of the json
    usaNewPosCases = usaData[0]['positiveIncrease']
    usaNewNegCases = usaData[0]['negativeIncrease']
    usaNewDeaths = usaData[0]['deathIncrease']

    # creates a string with defined variables
    usaTotalStr = 'Region: %s \n\nTotal Tests: %s \nTotal Positive Cases: %s \nTotal Negative Cases: %s \nTotal Deaths: %s \nTotal Recovered: %s \n\n' % (name, usaTotalTests, usaTotalPositive, usaTotalNegative, usaTotalDeaths, usaTotalRecovered)

    # creates a string with defined variables
    usaNewStr = 'New Positive Cases: %s \nNew Negative Cases: %s \nNew Deaths: %s' % (usaNewPosCases, usaNewNegCases, usaNewDeaths)

    # combines the strings
    finalUsaStr = usaTotalStr + usaNewStr
  except:
    # if something fails, this is printed
    finalUsaStr = 'There was a problem retreiving information.'
  # returns this to the label
  return finalUsaStr


def format_responseCounty(countyInfo,n):
  """
  From get_county

  Takes the countyInfo and the n of the county
  """
  # keys: date,county,state,fips,cases,deaths,confirmed_cases,confirmed_deaths,probable_cases,probable_deaths

  try:
  
    # turns found information into usable variables
    name = countyInfo['county'][n]
    cases = countyInfo['cases'][n]
    deaths = (countyInfo['deaths'][n])
    confirmed_cases = (countyInfo['confirmed_cases'][n])
    confirmed_deaths = (countyInfo['confirmed_deaths'][n])
    probable_cases = (countyInfo['probable_cases'][n])
    probable_deaths = (countyInfo['probable_deaths'][n])

    # creates the string seen in the gui
    countyTotalStr = 'County: %s \n\nTotal Cases: %s \nTotal Deaths: %s \nTotal Confirmed Cases: %s \nTotal Confirmed Deaths: %s \n\nProbable Cases: %s \nProbable Deaths: %s' % (name, cases, deaths, confirmed_cases, confirmed_deaths, probable_cases, probable_deaths)
  except:
    # if problem with information, it returns this
    countyTotalStr = 'There was a problem retreiving information.'
  # return whichever string is formed, goes to label
  return countyTotalStr


#-----------------grabbing--info------------------

# takes the determined URL and translates it into usable data
def URLilizerSt(URL):
  """
  Takes a URL for states

  obtains values from json and puts into variables

  Found from get_state()
  """
  # gets the info and turns it to reponse
  response = requests.get(URL)

  #print(response)
  # makes the response a json and into a var
  stateData = response.json()

  # makes the text of state label the response from the format_responseState function
  state_Label['text'] = format_responseState(stateData)


def URLilizerUSA(URL):
  """
  Takes a URL for USA

  obtains values from json dict and puts into variables

  Found from get_state()
  """
  # gets the info and turns it to reponse
  response = requests.get(URL)

  # makes usaData var the json of the response
  usaData = response.json()

  # makes the text of state label the response from the format_responseUSA function
  state_Label['text'] = format_responseUSA(usaData)


def get_state(entry):
  """
  takes the entry of the state entry box

  checks if entry is cooperative with the stateText dictionary

  creates a URL for the state

  calls the URLilizer functions
  """

  # make en a lowercase
  en = entry.lower()

  
  # for some reason, this one MUST come first in order for both to work
  # if they enetered an abbrev, make it equal to state var
  if en in us_state_abbrev.values():
    st = en
    URL = "https://api.covidtracking.com/v1/states/"+ st + "/current.json"
    URLilizerSt(URL)
  # if they enetered the full name of a state, then make st equal to the abbrev
  elif en in us_state_abbrev.keys():
    st = us_state_abbrev[en]
    URL = "https://api.covidtracking.com/v1/states/"+ st + "/current.json"
    URLilizerSt(URL)
  # if nothing is entered, return the USA url
  elif en == '':
    URL = "https://api.covidtracking.com/v1/us/current.json"
    URLilizerUSA(URL)
  # if something random is entered, return this as error
  else:
    errorHandle.printer('Please enter a valid state', window)

  # checks if entry is an abbreviation. If it is, then it turns it into full name
  # creates a global unabbreviated variable that is the state's name
  def unabbreviator():
    """
    inside get_state()

    Takes the entry of the state and makes sure that it is the full state name

    has the global unabbreviated var

    allows for matching state and county check
    """
    # this global is used to check that the entered count is in the right state
    global unabbreviated

    # if the entry is abbreviated...
    if en in us_state_abbrev.values():
        # this line turns the value into the key
        unabbreviated = (list(us_state_abbrev.keys())[list(us_state_abbrev.values()).index(en)])
    else:
      # if it isn't abbreviated, then we already have our goal
      unabbreviated = en
    #print(unabbreviated)
  # calls the function to unabbreviate the entry
  unabbreviator()


def get_county(entry):
  """
  takes entry from Enter county Entry Box

  reads from countyDataFrame.json

  takes a csv and converts to json with pd

  checks if county is in state -> state must be entered
  """

  # keys: date,county,state,fips,cases,deaths,confirmed_cases,confirmed_deaths,probable_cases,probable_deaths

  # redefine entry as string
  en = str(entry)

  # url of csv file
  uRl = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv"

  # reads the csv file from uRl
  countyInfo = pd.read_csv(uRl)

  # places it in json data frame
  countyInfo.to_json('countyDataFrame.json')

  # for loop through the number of counties
  for n in range(len(countyInfo['county'])):
    # if entered value is equal to the name of a county
    if en == countyInfo["county"][n].lower():
      #print(countyInfo['state'][n].lower())
      # try matching it with the state
        try:
          # if the full state name == full state name of the n county...
          if unabbreviated == countyInfo['state'][n].lower():
            print('Matched!')

            # make the county label text the return of format_responseCounty
            county_Label['text'] = format_responseCounty(countyInfo, n)

            # prints that the county is valid with the state
            errorHandle.printer('That is a valid county.', window)
            break
        except:
          # if try fails, print this as error
          errorHandle.printer('This county is not in this state!', window)
      #print(countyInfo["state"][224])
    # if nothing is entered, as well as no state entered, return this error
    elif en == '':
      errorHandle.printer('You may enter a county.', window)
      break
    # otherwise, return this as error
    else:
      errorHandle.printer('Please enter a valid county or state!', window)


#-----------------Gui-Design-------------------//

#-------------------frames--------------------//

# creates the background image
background = tk.PhotoImage(file="westback.png")
image_label = tk.Label(window, image=background)
# puts it right in the middle
image_label.place(relx=.5, rely=.5, anchor='center')

# creates the frame for the entries
enterFrame = tk.Frame(window, bg = '#d47057', bd = 5)
enterFrame.place(relx = 0.1,rely = 0.03, relwidth = 0.80, relheight = 0.225)

# creates the frame for the returns
midFrame = tk.Frame(window, bg = '#d47057', bd = 5)
midFrame.place(relx = 0.05,rely = 0.33, relwidth = 0.9, relheight = 0.40)

# creates the frame for the random county and state
lowFrame = tk.Frame(window, bg = '#d47057', bd = 5)
lowFrame.place(relx=.155, rely=.83,relwidth = .69, relheight= .14)

#------------------Labels----------------------//

# state label for state entry
state_Label = tk.Label(enterFrame, text = 'Enter a state:', bg = 'white', bd = 4)
state_Label.place(relx=.25, rely=.15, anchor='center')

# creates the entry box for state
stateEntry = tk.Entry(enterFrame, width = 20, bd = 5)
stateEntry.place(relx=.25, rely=.5, anchor='center')

# creates a label to enter a county
county_Label = tk.Label(enterFrame, text = 'Enter a county:', bg = 'white', bd = 4)
county_Label.place(relx=.75, rely=.15, anchor='center')

# creates the entry box for county
countyEntry = tk.Entry(enterFrame, width = 20, bd = 5)
countyEntry.place(relx=.75, rely=.5, anchor='center')

#--------------------Buttons--------------------//


def findLocation(countyInfo, sta):
  """
  takes county information and a state

  comes from calculate()

  this returns the string of the county and state
  """
  # for the amount of states
  for q in range(len(countyInfo['state'])):
    # if given state is one of the states
    if sta == countyInfo['state'][q]:
      # make n that state
      n = countyInfo['county'][q]
      # return this formatted string
      res = f'Try {n} County in {sta}!'
      return res


def calculate():
  """
  uses the county URL

  reads the URL and assigns text to random_Label

  creates sta variable
  """
  # needed urL
  urL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv"

  # reads the csv file from uRl
  countyInfo = pd.read_csv(urL)

  # places it in json data frame
  countyInfo.to_json('countyDataFrame.json')

  # takes the name and state of a random item from the us_state_abbrev2 dict
  abb, sta = random.choice(list(us_state_abbrev2.items()))

  # makes the text of random_Label the return of findLocation
  random_Label['text'] = findLocation(countyInfo, sta)

# creates the randomizer button
randomButton = tk.Button(window, bg = 'white',text='Randomizer', command=calculate)
randomButton.place(relx=.5, rely=.78, anchor='center')

# creates the state button
stateButton = tk.Button(enterFrame, bg = 'white', text='State', command= lambda: get_state(stateEntry.get()))
stateButton.place(relx=.25, rely=.82, anchor='center')

# creates the county button
countyButton = tk.Button(enterFrame, bg = 'white',text='County', command= lambda: get_county(countyEntry.get()))
countyButton.place(relx=.75, rely=.82, anchor='center')

#-------------------Results---------------------

# creates the state result label
state_Label = tk.Label(midFrame, bd = 10, bg = 'white', justify = 'left')
state_Label.place(relx=.25, rely=.5,relwidth = .45, relheight= .9, anchor='center')

# creates the county result label
county_Label = tk.Label(midFrame,bd = 10, bg = 'white',justify = 'left')
county_Label.place(relx=.75, rely=.5,relwidth = .45, relheight= .9, anchor='center')

# creates the random result label
random_Label = tk.Label(window,bd = 10, bg = 'white')
random_Label.place(relx=.5, rely=.90,relwidth = .65, relheight= .1, anchor='center')

# closes and loops the gui
window.mainloop()