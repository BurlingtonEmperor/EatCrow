import sys
import os
import webbrowser

from troubleshoot import *

which_os = "";
installation_var = 1;
is_setup = 0;

def clearScreen ():
  os.system('cls' if os.name == 'nt' else 'clear');

def checkWhichPlatform ():
  global which_os;
  which_os = sys.platform;
  if (which_os == 'win32' or which_os == 'win64' or which_os.includes('win')):
    which_os = 'win';
  elif (which_os == 'linux'):
    which_os = 'linux';
  else:
    installation_var = 0;
    return 'This operating system is incompatible with the Autoclave Program. Eat crow.';
  return which_os;

def installArduinoCLI ():
  match (which_os):
    case ('win'):
      print('Please install the Arduino CLI program from the Github Repository.');
      yes_or_no = input('Y/N: ').lower();
      if (yes_or_no == 'y'):
        webbrowser.open('https://docs.arduino.cc/arduino-cli/installation/');
      else:
        installation_var = 0;
        print('Installation has been stopped. ');
    case ('linux'):
      os.system('brew update');
      os.system('brew install arduino-cli');
      print('Installing Arduino CLI. ');
    case _:
      print('Invalid operating system. ');
      installation_var = 0;
      
def updateCORES ():
  print("Updating Cores...");
  os.system("arduino-cli core update-index");
  is_setup = 1;
      
program_installation_order = [checkWhichPlatform, installArduinoCLI]; #not useful now but may be in the future.

def installProgram ():
  checkWhichPlatform();
  installArduinoCLI();
  print("You can always change these settings later.");
  confirmSetup = input("Confirm installation Y/N?: ").lower();
  
  if (confirmSetup == "y"):
    is_setup = 1;
  else:
    print("Please come back to these settings.");
  loopThroughInterface();
    
def runThroughCLI (inoDIR):
  os.system("arduino-cli compile --fqbn arduino:avr:uno " + inoDIR);
    
def runCommand (commandText):
  match (commandText):
    case ("help"):
      print("update_cores: update all board cores");
    case ("update_cores"):
      updateCORES();
    case _:
      print("Not a valid command."); #P.S. you can simply turn these print statements into return statements for a more advanced UI in the future.
      
user_choice_init = 0;
def loopThroughInterface ():
    global user_choice_init
    # I don't like using classes.
    match (user_choice_init):
      case 0:
        print("""
Would you like to...
1: Install/Reset this program
2: Use commands
        """);
        user_choice_ask = input("Choose a number: ");
        match (user_choice_ask):
          case "1":
            installProgram();
          case "2":
            user_choice_init = 1;
            loopThroughInterface();
          case _:
            clearScreen();
            loopThroughInterface();
      case 1:
        clearScreen();
        print("Type HELP for a list of commands.");
        user_choice_ask = input("?: ");
        runCommand(user_choice_ask.lower());
        loopThroughInterface();

loopThroughInterface();
