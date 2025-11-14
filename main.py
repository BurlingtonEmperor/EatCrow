import sys
import os
import webbrowser
import pickle
import serial
import subprocess
import socket

from troubleshoot import *

which_os = "";
installation_var = 1;
is_setup = 0;
current_dir = "";
user_choice_init = 0;
COM_PORT = "COM3"; # use python -m pip install

def clearScreen ():
  os.system('cls' if os.name == 'nt' else 'clear');

def clearIDLE ():
  print('\n' * 100);

def checkWhichPlatform ():
  global which_os;
  global COM_PORT;
  
  which_os = sys.platform;
  if (which_os == 'win32' or which_os == 'win64' or which_os.includes('win')):
    which_os = 'win';
    COM_PORT = "COM3";
  elif (which_os == 'linux'):
    which_os = 'linux';
    COM_PORT = "/dev/ttyUSB0";
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
        os.system("winget install --id=ArduinoSA.CLI -e");
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
    if (which_os == "win"):
      print("Please restart this terminal window.");
    else:
      loopThroughInterface();
  else:
    print("Please come back to these settings.");
    loopThroughInterface();
    
def runThroughCLI (inoDIR):
  os.system("arduino-cli compile --fqbn arduino:avr:uno " + inoDIR);

def oneLinerCommands (commandText):
  csv_liner = commandText.split(";");
  for x in csv_liner:
    runCommand(x);

def findIfFileExists (fileDIR):
  match (current_dir):
    case (""):
      print("Current directory has not been set. Please use the 'find_dir' command.");
    case _:
      newFilePath = current_dir + "\\" + fileDIR;
      if (os.path.exists(newFilePath)):
        return (fileDIR + " exists.");
      else:
        return (fileDIR + " does not exist.");

def saveMacro (macroLines, macroName): #should be in the form of a list to be kosher.
  if (findIfFileExists(macroName + ".pkl").includes("exists.")):
    print("There is already a macro file that exists at that path.");
  else:
    with open(macroName + ".pkl", "wb") as f:
      pickle.dump(macroLines, f);
      print("Saved macro at " + current_dir + "\\" + macroName + ".pkl");

def loadMacro (macroName):
  macro_contents = "";
  if (findIfFileExists(macroName + ".pkl").includes("exists.")):
    with open(macroName + ".pkl", "rb") as f:
      macro_contents = pickle.load(f);
    return macro_contents;
  else:
    print("A macro file does not exist at that path.");

def editMacro (macroName):
  print();

def check_internet_socket():
  try:
    socket.create_connection(("8.8.8.8", 53), timeout=5);
    return True;
  except OSError:
    return False;
    
def runParameterCommand (commandText):
  csv_liner = commandText.split();
  match (csv_liner[0]):
    case ("run_cli"):
      runThroughCLI(csv_liner[1]);
    case ("find_file"):
      print(findIfFileExists(csv_liner[1]));
    case ("echo"):
      csv_liner.pop(0);
      # print(csv_liner);
      echo_liner = "";
      echo_line_space = " ";
      for x in csv_liner:
        match (echo_liner):
          case "":
            echo_line_space = "";
          case _:
            echo_line_space = " ";
        echo_liner += (echo_line_space + x);
      print(echo_liner);
    
def runCommand (commandText):
  global current_dir;
  global user_choice_init;

  potentialParameters = commandText.split();
  match (commandText):
    case ("help"):
      print("update_cores: update all board cores");
      print("echo: ex. 'echo test' outputs test");
      print("oneliner: run a series of commands");
      print("clear: clear screen");
      print("clear_idle: clears IDLE screen (if running on IDLE)");
      print("find_dir: find and set current directory");
      print("run_cli: ex. 'run_cli test' runs a test program.");
      print("find_file: find if a file exists; ex. 'find_file main.py'");
      print("em_stop: stop current arduino program");
      print("end_prgm: ends program");
      print("restart: restarts program");
      print("os_input: input direct shell commands");
      print("check_web_conn: check internet connection");
    case ("update_cores"):
      updateCORES();
    case ("oneliner"):
      print("Please seperate commands by the semicolon character ';'.");
      oneliner_input = input("Commands: ");
      oneLinerCommands(oneliner_input);
    case ("clear"):
      clearScreen();
    case ("clear_idle"):
      clearIDLE();
    case ("find_dir"):
      current_dir = os.path.dirname(os.path.realpath(__file__));
      print(current_dir);
    case ("end_prgm"):
      sys.exit();
    case ("restart"):
      user_choice_init = 0;
    case ("os_input"):
      os_input = input("Shell commands: ");
      os.system(os_input);
    case ("check_web_conn"):
      print("Connected to internet?: " + str(check_internet_socket()));
    case _:
      match (potentialParameters[0]):
        case ("echo"):
          runParameterCommand(commandText);
        case ("run_cli"):
          runParameterCommand(commandText);
        case ("find_file"):
          runParameterCommand(commandText);
        case _:
          print("Not a valid command.");
      #P.S. you can simply turn these print statements into return statements for a more advanced UI in the future.

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
        print("Type HELP for a list of commands.");
        user_choice_ask = input("?: ");
        runCommand(user_choice_ask.lower());
        loopThroughInterface();

#test
runParameterCommand("echo Eat Crow");
#end test
loopThroughInterface();
        
