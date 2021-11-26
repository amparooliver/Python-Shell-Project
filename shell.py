import os
import getpass 
import ir 

##################################################
# Controls the flow of the program (main)
##################################################

def main():

    # Infinite loop til user input = exit
    while(True):
        username = getpass.getuser() # To obtain the “login name” of the user.
        computer = "@" + os.uname().nodename # To obtain computer name
        current_path = ":" + os.getcwd() + "$ " # To get current path
        user_input = (input( username + computer + current_path )).split() # Read user input
        if(user_input == 'exit'):
            break
        else:
            run_command(user_input)

##################################################
# Searches the right command and executes it
# TIP: Indexing Syntax for Slicing obj[start:stop:step]
##################################################

def run_command(user_input):

    if user_input[:3] == "ir":
        # Verificaciones
        ir(user_input[3:])  

##################################################

