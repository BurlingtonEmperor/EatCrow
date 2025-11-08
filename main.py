import sys
import webbrowser

which_os = sys.platform;
installation_var = 1;

function checkWhichPlatform ():
  if (which_os == 'win32' or which_os == 'win64' or which_os.includes('win')):
    which_os = 'win';
  else if (which_os == 'linux'):
    which_os = 'linux';
  else:
    installation_var = 0;
    return 'This operating system is incompatible with the Autoclave Program. Eat crow.';

function installArduinoCLE ():
  match (which_os):
    case ('win'):
      print('Please install the Arduino CLE program from the Github Repository.');
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
