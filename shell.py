import getpass
import logging
import os
import pwd
import shlex
import shutil
import signal
import socket
import subprocess
import sys
import stat


from constants import SHELL_STATUS_RUN, SHELL_STATUS_STOP

logging.basicConfig(filename='sistema_error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


# COMMANDS #
################################################################################
def exits(args):
    return SHELL_STATUS_STOP
################################################################################
# os.path.abspath(path) Returns normalized and absolute version of path.
# os.chdir Change the current working directory to path.
# os.getenv Return the value of the environment variable key if it exists.
# os.path.isdir Return True if path is an existing directory.

def ir(args):
    # Check if path exists
    if os.path.isdir(os.path.abspath(args[0])):
        if 0 < len(args) < 2:
            try:
                os.chdir(os.path.abspath(args[0]))
            except OSError as error: 
                print(error)
                logging.exception(error)
        else:
            os.chdir(os.getenv('HOME'))
    else:
        print("ir: Path does not exist")
    return SHELL_STATUS_RUN

################################################################################
# os.mkdir Create a directory named path.

def creardir(args):
    try: 
        os.mkdir(args[0]) 
    except OSError as error: 
        print(error)  
        logging.exception(error)
    return SHELL_STATUS_RUN

################################################################################
# os.listdir Return a list containing the names of the entries in path.

def listar(args):
    # If no path was provided, get cwd
    if len(args) < 1:
        path = os.getcwd()
    elif len(args) > 1:
        print("listar: Too many arguments")
        return SHELL_STATUS_RUN
    else:
        # Check if path exists
        if os.path.isdir(os.path.abspath(args[0])):
            if len(args) == 1:
                path = os.path.abspath(args[0])
        else:
            print("listar: Path does not exist")
            return SHELL_STATUS_RUN
    try: 
        dir_list = os.listdir(path) 
        print(dir_list)
    except OSError as error: 
        print(error)
        logging.exception(error)  
    return SHELL_STATUS_RUN

################################################################################
# os.rename Rename the file or directory src to dst.

def renombrar(args):
    if len(args) < 2:
        print("renombrar: Missing arguments")
        return SHELL_STATUS_RUN
    elif len(args) > 2:
        print("renombrar: Too many arguments")
        return SHELL_STATUS_RUN
    # Check if path exists
    if os.path.isdir(os.path.abspath(args[0])):
        try: 
            os.rename(os.path.abspath(args[0]), os.path.abspath(args[1]))
        except OSError as error: 
            print(error)
    else:
        print("renombrar: Path does not exist")
    return SHELL_STATUS_RUN

################################################################################
# shutil.move Recursively move a file or directory src to dst.

def mover(args):
    if len(args) < 2:
        print("mover: Missing arguments")
        return SHELL_STATUS_RUN
    elif len(args) > 2:
        print("mover: Too many arguments")
        return SHELL_STATUS_RUN
    # Check if src path exists
    if os.path.isdir(os.path.abspath(args[0])):
        try: 
            shutil.move(os.path.abspath(args[0]), os.path.abspath(args[1]))
        except OSError as error: 
            print(error) 
            logging.exception(error) 
    else:
        print("mover: Path does not exist")
    return SHELL_STATUS_RUN

################################################################################
# shutil.copy Copies the file src to the file or directory dst. 

def copiar(args):
    try: 
        shutil.copy(os.path.abspath(args[0]), os.path.abspath(args[1]))
    except OSError as error: 
        print(error) 
        logging.exception(error) 
    return SHELL_STATUS_RUN

################################################################################
# os.getgrouplist Return list of group ids that user belongs to.

def grupos(args):
    # if argument is just user
    if len(args) == 1:
        user = args[0]
        # Check if user exists
        try:
            pwd.getpwnam(user)
        except KeyError:
            print("grupos: User does not exist")
            return SHELL_STATUS_RUN
        # Get gid for user
        gid = pwd.getpwnam(user).pw_gid
    # if arguments are user and gid
    elif len(args) == 2:
        user = args[0]
        # Check if user exists
        try:
            pwd.getpwnam(user)
        except KeyError:
            print("grupos: User does not exist")
            return SHELL_STATUS_RUN
        gid = int(args[1])
    # if there are no arguments, gets current user and gid
    elif len(args) == 0:
        user = getpass.getuser()
        gid = pwd.getpwnam(user).pw_gid
    elif len(args) > 2:
        print("grupos: Too many arguments")
        return SHELL_STATUS_RUN
    try: 
        group_list = os.getgrouplist(user, gid) 
        print(group_list)
    except OSError as error: 
        print(error)  
        logging.exception(error)
    return SHELL_STATUS_RUN

################################################################################
#def permisos(args):

################################################################################
def differ(args):
    if args == 2:
        print("Bien")
    elif args < 2:
        print("differ: Missing arguments")
    elif args > 2:
        print("differ: To many arguments")
    return SHELL_STATUS_RUN

################################################################################

# Hash map to store built-in function name and reference as key and value
built_in_cmds = {}

def tokenize(string):
    return shlex.split(string)

def preprocess(tokens):
    processed_token = []
    for token in tokens:
        # Convert $-prefixed token to value of an environment variable
        if token.startswith('$'):
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token


def handler_kill(signum, frame):
    raise OSError("Killed!")

def execute(cmd_tokens):

    if cmd_tokens:
        # Extract command name and arguments from tokens
        cmd_name = cmd_tokens[0]
        cmd_args = cmd_tokens[1:]

        # If the command is a built-in command,
        # invoke its function with arguments
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)

        # Wait for a kill signal
        signal.signal(signal.SIGINT, handler_kill)
        # Spawn a child process
        # Unix support
        p = subprocess.Popen(cmd_tokens)
        # Parent process read data from child process
        # and wait for child process to exit
        p.communicate()

    # Return status indicating to wait for next command in shell_loop
    return SHELL_STATUS_RUN


#Display a command prompt as `[<user>@<hostname> <dir>]$ `
def display_cmd_prompt():
    # Get user and hostname
    user = getpass.getuser()
    hostname = socket.gethostname()

    # Get base directory (last part of the curent working directory path)
    cwd = os.getcwd()
    base_dir = os.path.basename(cwd)

    # Use ~ instead if a user is at his/her home directory
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'

    # Print out to console
    sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
    sys.stdout.flush()

def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        display_cmd_prompt()

        try:
            # Read command input
            cmd = sys.stdin.readline()
            # Tokenize the command input
            cmd_tokens = tokenize(cmd)
            # Preprocess special tokens
            # (e.g. convert $<env> into environment value)
            cmd_tokens = preprocess(cmd_tokens)
            # Execute the command and retrieve new status
            status = execute(cmd_tokens)
        except:
            _, err, _ = sys.exc_info()
            print(err)
            logging.exception(err)


# Register a built-in function to built-in command hash map
def register_command(name, func):
    built_in_cmds[name] = func

# Register all built-in commands here
def init():
    register_command("ir", ir)
    register_command("creardir", creardir)
    register_command("exit", exits)
    register_command("listar", listar)
    register_command("renombrar", renombrar)
    register_command("mover", mover)
    register_command("copiar", copiar)
    register_command("grupos", grupos)

def main():
    # Init shell before starting the main loop
    init()
    shell_loop()

if __name__ == "__main__":
    main()
