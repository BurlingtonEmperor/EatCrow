import sys
import webbrowser

which_os = sys.platform;
installation_var = 1;
is_setup = 0;

def checkWhichPlatform ():
  if (which_os == 'win32' or which_os == 'win64' or which_os.includes('win')):
    which_os = 'win';
  else if (which_os == 'linux'):
    which_os = 'linux';
  else:
    installation_var = 0;
    return 'This operating system is incompatible with the Autoclave Program. Eat crow.';

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
    
def runCommand (commandText):
  match (commandText):
    case ("help"):
      print("");
    case ("update_cores"):
      updateCORES();