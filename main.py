import sqlite3
import os
from functools import lru_cache

database = sqlite3.connect("test.db")
databaseCursor = database.cursor()
databaseCursor.execute('''CREATE TABLE IF NOT EXISTS users(
														id INTEGER PRIMARY KEY ASC, 
														username TEXT, 
														password TEXT)''')

database.commit()

clear = lambda: os.system('clear')

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def userCount():
	rowsQuery = "SELECT Count(*) FROM users"
	result = databaseCursor.execute(rowsQuery)
	return result.fetchone()[0]

def dbEmpty():
	if (userCount() == 0):
		return True
	else:
		return False


def dbFull():
	if (userCount() == 5):
		return True
	else:
		return False


def unique(username):
	lookup = databaseCursor.execute("SELECT COUNT(*) FROM users where username IS ?", (username,))
	return lookup.fetchone()[0] == 0


def checkExistingAccts(username, password):
  databaseCursor.execute("SELECT * FROM users WHERE username= ? and password= ?",
    (username, password))
  found = databaseCursor.fetchone()
  if found:
    return True
  else:
    return False

def passwordValidator(password):
  c, d, s = 0, 0, 0
  length = len(password)
  if length > 7 and length < 13:
    for i in password:
      if i.isupper():
        c += 1
      if i.isdigit():
        d += 1
      if i=='!' or i=='@' or i=='#' or i=='$' or i=='%' or i=='^' or i=='&' or i=='*':
        s += 1

  if c > 0 and d > 0 and s > 0:
    return True
  else:
    return False


@lru_cache
def menuValidatorBuilder(validOptions):
	"""
	Generates a validator from a list of valid options

 	:param validOptions: A list of valid inputs from a menu
	:return a function f(x) that returns if x is in validOptions
	"""
	return lambda menuInput: (menuInput in validOptions and menuInput != '')


def gatherInput(prompt, failResponse, validator):
  """
  Continuously prompts the user for input, validates the input it gets are returns it if its fine or    gives an error message if its bad
  
  :param prompt: A string the user recieves when being prompted for input, used in a input(prompt)      call
  :param failResponse: A message the user recieves if they give bad input
  :param validator: A function f(x) = x is a valid string for a given prompt
  """
  userInput = input(prompt)
  
  while (not validator(userInput)):
    clear()
    print(failResponse)
    userInput = input(prompt)
  
  return userInput



def login():
  if dbEmpty():
    print("No existing accounts. Please create a new account.\n")
    return applicationEntry
  else:
    username = input("Username: ")
    password = input("Password: ")
  
    exist = checkExistingAccts(username, password)
    if exist:
      clear()
      print("You have successfully logged in\n")
      return mainInterface
    else:
      clear()
      print("Incorrect username/password. Please try again.\n")
      return login


def newAcct():
  if dbFull():
    print("\nAll permitted accounts have been created, please come back later.\n")
    return exitState
  username = gatherInput(
            "Enter a username: ",
            "Username already exists. Please try again.",
            unique)

  password = gatherInput(
            "\nPassword must meet the following requirements:\n"\
            "\t-Length of 8-12 characters\n"\
            "\t-Contain one capital letter\n"\
            "\t-Contain one digit\n"\
            "\t-Contain one of the following special characters: !, @, #, $, %, ^, &, *\n"\
            "\nPassword: ",
            "Password does not meet security requirements",
            passwordValidator)

  databaseCursor.execute("""
                 INSERT INTO users (username, password) VALUES
                     (?, ?)
                 """, (username, password))
  database.commit()

  clear()
  return mainInterface


def applicationEntry():
  prompt = "Please select an option below:\n"\
           "\t1. Log in to an existing account\n"\
           "\t2. Create a new account\n"\
           "Selection: "
  sel = int(gatherInput(prompt, "\nInvalid input. Please try again.\n",
                    menuValidatorBuilder('1,2')))

  if sel == 1:
    clear()
    return login
  elif sel == 2:
    clear()
    return newAcct


def mainInterface():
  prompt = "Please select an option below:\n"\
          "\t1. Search for a job\n"\
          "\t2. Find someone you know\n"\
          "\t3. Learn a new skill\n"\
          "\t4. Return to login\n"\
          "Selection: "
  sel = int(
        gatherInput(prompt, "Invalid input. Please try again.\n",
                    menuValidatorBuilder('1,2,3,4')))

  if sel == 1 or sel == 2:
    clear()
    return underConstruction
  elif sel == 3:
    clear()
    return listSkills
  else:
    clear()
    return applicationEntry


def listSkills():
  prompt = "Please select a skill below:\n"\
          "\t1. Setup a database\n"\
          "\t2. Setup access roles\n"\
          "\t3. Use a microservice from the marketplace\n"\
          "\t4. Create budget alerts\n"\
          "\t5. Calculate OPEX costs\n"\
          "Selection: "
  gatherInput(prompt, "Invalid input. Please try again.\n",
                  menuValidatorBuilder('1,2,3,4,5'))
  clear()
  return underConstruction


def underConstruction():
  print("Under construction.\n")
  input("Press ENTER to continue.\n")
  clear()
  return mainInterface
    


def exitState():
  clear()
  print("Goodbye")
  exit()

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

print("Welcome to InCollege!\n")

def stateLoop(state):

	while (state is not exitState):
		state = state()
	
stateLoop(applicationEntry)