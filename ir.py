import os

##################################################
# Command to change directories (ir = cd)
##################################################

def ir(user_input):
    path = user_input
    try:
        # chdir changes the current working directory to the given path
        os.chdir(os.path.abspath(path))
    except Exception:
        print("No such file or directory")

##################################################
