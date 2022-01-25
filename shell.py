#!/usr/bin/python3
import binascii
import crypt
import difflib
import ftplib
import getpass
import hashlib
import os
import pwd
import random
import shlex
import shutil
import signal
import socket
import string
import subprocess
import sys
import time
import datetime

# CONSTANTS
SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1

from logger import sysError_logger, usuario_logger, usuTransfer_logger


# FUNCTIONS #
################################################################################
def userLogin():
    user = getpass.getuser()
    ip = str(socket.gethostbyname(socket.gethostname()))
    currentDate = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    str1 =' LOGIN REGISTER: username: ' + user + ' IP:' + ip + ' date:' + currentDate + '\n'  
    usuario_logger.info(str1)
################################################################################
def userLogout():
    user = getpass.getuser()
    ip = str(socket.gethostbyname(socket.gethostname()))
    currentDate = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    str1 =' LOGOUT REGISTER: username: ' + user + ' IP:' + ip + ' date:' + currentDate + '\n'  
    usuario_logger.info(str1)
################################################################################
def userTransfer(args):
    user = getpass.getuser()
    currentDate = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    str1 =' USER TRANSFER REGISTER (ftp/scp): username: ' + user + ' date:' + currentDate + ' command:' + args + '\n'  
    usuTransfer_logger(str1)
################################################################################
################################################################################
def get_size_format(n, suffix="B"):
    # converts bytes to scaled format (e.g KB, MB, etc.)
    for unit in ["", "K", "M", "G", "T", "P"]:
        if n < 1024:
            return f"{n:.2f}{unit}{suffix}"
        n /= 1024
################################################################################
def get_datetime_format(date_time):
    # convert to datetime object
    date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
    # convert to human readable date time string
    return date_time.strftime("%Y/%m/%d %H:%M:%S")
################################################################################
def hash_password(password):
    salt = ''.join([random.choice(string.ascii_letters + string.digits)
            for _ in range(16)])
    prefix = '$6$'
    return crypt.crypt(password, prefix + salt)
################################################################################
def readFile(filename):
    with open(filename) as file:
        lines = file.readlines() 
        lines = [line.rstrip() for line in lines]
    return lines
################################################################################
def processText(text):
    processedText = list(text)
    for i in range(len(processedText)):
        processedText[i] = processedText[i].split(':')
    return processedText
################################################################################
def getNewUserID():
    passwdPath = "/etc/passwd"
    passwd = open(passwdPath,"r")
    userID = 0
    passwd = readFile(passwdPath)  
    for i in range(len(passwd)):
        passwd[i] = passwd[i].split(':')
    for i in range(len(passwd)):
        if userID < int(passwd[i][2]):
            userID = int(passwd[i][2])
    return userID + 1
################################################################################
def getNewGroupID():
    groupPath = "/etc/group"
    groupID = 0
    with open(groupPath) as file:
        group = file.readlines()
        group = [group.rstrip() for group in group]
    for i in range(len(group)):
        group[i] = group[i].split(':')
    for i in range(len(group)):
        if groupID < int(group[i][2]):
            groupID = int(group[i][2])
    return groupID + 1
################################################################################
# COMMANDS #
################################################################################
def exits(args):
    userLogout()
    output = os.popen('exit').read()
    print (output)
    return SHELL_STATUS_STOP
################################################################################
# os.path.abspath(path) Returns normalized and absolute version of path.
# os.chdir Change the current working directory to path.
# os.getenv Return the value of the environment variable key if it exists.
# os.path.isdir Return True if path is an existing directory.

def ir(args):
    # Argument verifications
    if len(args) > 1:
        print("ir: Too many arguments")
        sysError_logger.error("ir: Too many arguments")
        return SHELL_STATUS_RUN
    elif len(args) == 0:
        os.chdir(os.getenv('HOME'))
    elif len(args) == 1:
        try:
            os.chdir(os.path.abspath(args[0]))
        except OSError as error: 
            print(error)
            sysError_logger.exception(error)
    return SHELL_STATUS_RUN

################################################################################
# os.mkdir Create a directory named path.

def creardir(args):
    try: 
        os.mkdir(args[0]) 
    except OSError as error: 
        print(error)  
        sysError_logger.exception(error)
    return SHELL_STATUS_RUN

################################################################################
# os.listdir Return a list containing the names of the entries in path.
# os.path.isdir Return True if path is an existing directory.

def listar(args):
    # Argument verifications
    # If no path was provided, get cwd
    if len(args) < 1:
        path = os.getcwd()
    elif len(args) > 1:
        print("listar: Too many arguments")
        sysError_logger.error("listar: Too many arguments")
        return SHELL_STATUS_RUN
    else:
        # Check if path exists
        if os.path.isdir(os.path.abspath(args[0])):
            if len(args) == 1:
                path = os.path.abspath(args[0])
        else:
            print("listar: Path does not exist")
            sysError_logger.error("listar: Path does not exist")
            return SHELL_STATUS_RUN
    try: 
        dir_list = os.listdir(path) 
        print(dir_list)
    except OSError as error: 
        print(error)
        sysError_logger.exception(error)  
    return SHELL_STATUS_RUN

################################################################################
# os.rename Rename the file or directory src to dst.

def renombrar(args):
    # Argument verifications
    if len(args) < 2:
        print("renombrar: Missing arguments")
        sysError_logger.error("renombrar: Missing arguments")
        return SHELL_STATUS_RUN
    elif len(args) > 2:
        print("renombrar: Too many arguments")
        sysError_logger.error("renombrar: Too many arguments")
        return SHELL_STATUS_RUN
    try: 
        os.rename(os.path.abspath(args[0]), os.path.abspath(args[1]))
    except OSError as error: 
        print(error)
        sysError_logger.exception(error)  
    return SHELL_STATUS_RUN

################################################################################
# shutil.move Recursively move a file or directory src to dst.

def mover(args):
    # Argument verifications
    if len(args) < 2:
        print("mover: Missing arguments")
        sysError_logger.error("mover: Missing arguments")
        return SHELL_STATUS_RUN
    elif len(args) > 2:
        print("mover: Too many arguments")
        sysError_logger.error("mover: Too many arguments")
        return SHELL_STATUS_RUN
    try: 
        shutil.move(os.path.abspath(args[0]), os.path.abspath(args[1]))
    except Exception as er:       
        sysError_logger.exception(er)
        print(er)
    return SHELL_STATUS_RUN

################################################################################
# shutil.copy Copies the file src to the file or directory dst. 

def copiar(args):
    # Argument verifications
    if len(args) < 2:
        print("copiar: Missing arguments")
        sysError_logger.error("copiar: Missing arguments")
        return SHELL_STATUS_RUN
    elif len(args) > 2:
        print("copiar: Too many arguments")
        sysError_logger.error("copiar: Too many arguments")
        return SHELL_STATUS_RUN
    try: 
        shutil.copy(os.path.abspath(args[0]), os.path.abspath(args[1]))
    except Exception as er:       
        sysError_logger.exception(er)
        print(er)
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
            sysError_logger.error("grupos: User does not exist")
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
            sysError_logger.error("grupos: User does not exist")
            return SHELL_STATUS_RUN
        gid = int(args[1])
    # if there are no arguments, gets current user and gid
    elif len(args) == 0:
        user = getpass.getuser()
        gid = pwd.getpwnam(user).pw_gid
    elif len(args) > 2:
        print("grupos: Too many arguments")
        sysError_logger.error("grupos: Too many arguments")
        return SHELL_STATUS_RUN
    try: 
        group_list = os.getgrouplist(user, gid) 
        print(group_list)
    except OSError as error: 
        print(error)  
        sysError_logger.exception(error)
    return SHELL_STATUS_RUN

################################################################################
# os.chmod Change the mode of path to the numeric mode.  os.chmod(path, mode, *, dir_fd=None, follow_symlinks=True)
# $ chmod mode path/to/File 

def permisos(args):
    if len(args) < 2:
        print("permisos: Missing arguments")
        sysError_logger.error("permisos: Missing arguments")
        return SHELL_STATUS_RUN
    elif len(args) > 2:
        print("permisos: Too many arguments")
        sysError_logger.error("permisos: Too many arguments")
        return SHELL_STATUS_RUN
    else:
        mode = int(args[0])
        try: 
            os.chmod(os.path.abspath(args[1]),mode) 
        except OSError as error: 
            print(error)  
            sysError_logger.exception(error)
    return SHELL_STATUS_RUN

################################################################################
# os.path.isfile('file') Checks if file exists

def difer(args):
    if len(args) == 2:
        text1 = os.path.abspath(args[0])
        text2 = os.path.abspath(args[1])
        if(os.path.isfile(text1) and os.path.isfile(text2)):
            with open(text1) as file_1:
                file_1_text = file_1.readlines()
            with open(text2) as file_2:
                file_2_text = file_2.readlines() 
            # Find and print the diff:
            for line in difflib.unified_diff(file_1_text, file_2_text, 
            fromfile= text1, tofile= text2, lineterm=''):
                print(line)
        else:
            print("difer: File does not exist")
            sysError_logger.error("difer: File does not exist")
    elif len(args) < 2:
        print("difer: Missing arguments")
        sysError_logger.error("difer: Missing arguments")
    elif len(args) > 2:
        print("difer: Too many arguments")
        sysError_logger.error("difer: Too many arguments")
    return SHELL_STATUS_RUN

################################################################################

def usuario(args):
    if len(args) > 1:
        print("usuario: Too many arguments")
        sysError_logger.error("usuario: Too many arguments")
    elif len(args) < 1:
        print("usuario: Missing arguments")
        sysError_logger.error("usuario: Missing arguments")
    else:        
        # Check if current user is root
        if os.geteuid() == 0:
            # Set variables
            username = args[0]
            paths = ["/etc/shadow","/etc/passwd","/etc/group"]
            files = []
            for i in paths:
                files.append(readFile(i))
            for i in range(3):
                files[i] = processText(files[i])
            # Check if user already exists
            for i in range(len(files[2])):
                if files[2][i][0] == username:
                    sysError_logger.error(username + " already exists")
                    return SHELL_STATUS_RUN

            # Get new user ID group ID
            userID = getNewUserID()
            groupID = getNewGroupID()

            # New home directory for User
            homePath = "/home/" + username 
            if(os.path.exists(homePath) == False):
                os.mkdir(homePath,int('755',8))

            # Ask Personal information
            fullname=input("Fullname: ")
            workphone=input("Workphone:")
            cellphone=input("Personal Cellphone: ")
            sWork=input("Start work time HH:MM: ")
            sWork=sWork.replace(":","")
            oWork=input("Off-work time HH:MM: ")
            oWork=oWork.replace(":","")
            # Append to files
            for i in range(3):
                files[i] = open(paths[i],"a+")

            epoch = int(time.time())
            # The information is written in the corresponding files
            files[0].write(f"{username}:!:{epoch}:0:99999:7:::\n")
            files[1].write(f"{username}:!:{userID}:{groupID}:{fullname},{workphone},{cellphone},{sWork},{oWork}:{homePath}:/bin/bash\n")
            files[2].write(f"{username}:x:{groupID}:\n")
        else:
            print("usuario: User does not have root privileges")
            sysError_logger.error("usuario: User does not have root privileges")

    return SHELL_STATUS_RUN

################################################################################
# shutil.chown used to change the owner and /or group of the specified path. 

def propietario(args):
    if len(args) > 3:
        print("propietario: Too many arguments")
        sysError_logger.error("propietario: Too many arguments")
    elif len(args) < 2:
        print("propietario: Missing arguments")
        sysError_logger.error("propietario: Missing arguments")
    else:
        path = os.path.abspath(args[0])
        # Check if User exists
        user = args[1]
        try:
            pwd.getpwnam(user)
        except KeyError:
            print("propietario: User does not exist")
            sysError_logger.error("propietario: User does not exist")
            return SHELL_STATUS_RUN
        try: 
            # Make changes
            shutil.chown(path, user, user)
        except Exception as er:       
            sysError_logger.exception(er)
            print(er)

    return SHELL_STATUS_RUN   

################################################################################
def contrasenha(args):
    # Argument verifications
    if len(args) > 1:
        print("contrasenha: Too many arguments")
        sysError_logger.error("contrasenha: Too many arguments")
    elif len(args) < 1:
        print("contrasenha: Missing arguments")
        sysError_logger.error("contrasenha: Missing arguments")
    else:        
        # Check if current user is root
        if os.geteuid() == 0:

            # Set variables
            username = args[0]
            paths = ["/etc/shadow","/etc/passwd"]
            userColumnShadow = 0
            userColumnPasswd = 0
            fileStrings = [0,0]
            fileAttributes = [0,0]     

            # Read files
            for i in range(2):
                fileStrings[i] = readFile(paths[i])
                fileAttributes[i] = processText(fileStrings[i])
            # Check if user exists in files
            for i in range(len(fileAttributes[0])):
                if fileAttributes[0][i][0] == username:
                    userColumnShadow = i
            for i in range(len(fileAttributes[1])):
                if fileAttributes[1][i][0] == username:
                    userColumnPasswd = i    
            # If user is found in files      
            if userColumnShadow != 0 or userColumnPasswd != 0:
                # Ask for password
                password = getpass.getpass()
                # Crypt password
                newHash = hash_password(password)

                # Update arrays 
                fileStrings[0][userColumnShadow] = f"{username}:{newHash}:{fileAttributes[0][userColumnShadow][2]}:{fileAttributes[0][userColumnShadow][3]}:{fileAttributes[0][userColumnShadow][4]}:{fileAttributes[0][userColumnShadow][5]}:::"
                fileStrings[1][userColumnPasswd] = f"{username}:x:{fileAttributes[1][userColumnPasswd][2]}:{fileAttributes[1][userColumnPasswd][3]}:{fileAttributes[1][userColumnPasswd][4]}:{fileAttributes[1][userColumnPasswd][5]}:{fileAttributes[1][userColumnPasswd][6]}"

                passwdFalso = open("/etc/passwd","w+")
                #Actualizamos los archivos passwd y shadow
                for i in range(len(fileStrings[1])):
                    passwdFalso.write(fileStrings[1][i])
                    passwdFalso.write("\n")

                shadowFalso = open("/etc/shadow","w+")
                for i in range(len(fileStrings[0])):    
                    shadowFalso.write(fileStrings[0][i])
                    shadowFalso.write("\n")
                
            else:
                print("contrasenha: User does not exist")
                sysError_logger.error("contrasenha: User does not exist")         
        else:
            print("usuario: User does not have root privileges")
            sysError_logger.error("usuario: User does not have root privileges")

    return SHELL_STATUS_RUN
################################################################################
def ayuda(args):
    cm1 = """
    copiar: copiar /path/to/File /path/to/Destination
    Copies file from origin to path.
    """
    cm2 = """
    mover: mover /path/to/Origin /path/to/Destination
    Moves file/directory to another directory.
    """
    cm3 = """
    renombrar: renombrar /path/to/Original /path/to/Renamed
    Renames file/directory.
    """
    cm4 = """
    listar: listar /path/to/Destination
    Lists all the entries within the provided directory. If argument is empty, lists cwd.
    """
    cm5 = """
    creardir: creardir /path/to/Directory
    Creates a directory.
    """
    cm6 = """
    ir: ir /path/to/Directory
    Changes from cwd to provided directory.
    """
    cm7 = """
    permisos: permisos mode /path/to/Destination
    Manages file system access permissions to files/directories.
    """
    cm8 = """
    propietario: propietario username /path/to/Destination
    Changes ownership of files/directories.
    """
    cm9 = """
    contrasenha: contrasenha username
    Sets or changes password for given username. Must have root privileges.
    """        
    cm10 = """
    usuario: usuario username
    Creates a new user for given username. Must have root privileges.
    """
    cm11 = """
    grupos: grupos username
    Lists the IDs of the primary and any supplementary groups for given username.
    """
    cm12 = """
    difer: difer /path/to/file1 /path/to/file2
    Compares two given files line by line and prints differences.
    """
    # Argument verifications
    if len(args) > 1:
        print("help: Too many arguments")
        sysError_logger.error("help: Too many arguments")
    elif len(args) == 0:
        print("AYUDA")
        print(f"{cm1}\n{cm2}\n{cm3}\n{cm4}\n{cm5}\n{cm6}\n{cm7}\n{cm8}\n{cm9}\n{cm10}\n{cm11}\n{cm12}\n")
    else:  
        print("AYUDA")
        if args[0] == "copiar": print(cm1)
        if args[0] == "mover": print(cm2)  
        if args[0] == "renombrar": print(cm3)  
        if args[0] == "listar": print(cm4)  
        if args[0] == "creardir": print(cm5)  
        if args[0] == "ir": print(cm6)  
        if args[0] == "permisos": print(cm7)  
        if args[0] == "propietario": print(cm8)  
        if args[0] == "contrasenha": print(cm9)  
        if args[0] == "usuario": print(cm10)  
        if args[0] == "grupos": print(cm11)  
        if args[0] == "difer": print(cm12)       
    return SHELL_STATUS_RUN
################################################################################
def doFTP(args):
    try:
        os.system(args)
        userTransfer(args)
    except Exception as e:
        print(e)
        sysError_logger.error(e)
    return SHELL_STATUS_RUN
################################################################################
def demonio(args):
    # Argument verifications
    if len(args) > 3:
        print("demonio: Too many arguments")
        sysError_logger.error("contrasenha: Too many arguments")
    elif len(args) < 2:
        print("demonio: Missing arguments")
        sysError_logger.error("demonio: Missing arguments")
    else:
        if(args[0]=='levantar'):
            try:
                subprocess.Popen(args[1])
            except Exception as e:
                print(e)
                sysError_logger.error(e)
                print('Demonio: Non valid argument.')
        elif(args[0]=='apagar'):
            try:
                pid=int(args[1])
                os.kill(pid, signal.SIGTERM)
                os.kill(pid, signal.SIGKILL)
            except Exception as e:
                print(e)
                sysError_logger.error(e)
                print('Demonio: Non valid argument.')
    return SHELL_STATUS_RUN
################################################################################
# Para ejecutar comandos del sistema 
def doShell(args):
    # Argument verifications
    if len(args) < 1:
        print("doShell: Missing arguments")
        sysError_logger.error("doShell: Missing arguments")
    else:
        # Turn List to String
        # using list comprehension
        str1 = ' '.join(map(str, args))
        output = os.popen(str1).read()
        print (output)

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
    # If preferable, change base_dir = cwd to get the absolute path

    # Use ~ instead if a user is at his/her home directory
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'

    # Print out to console
    sys.stdout.write("[%s@%s: %s]$ " % (user, hostname, base_dir))
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
            sysError_logger.exception(err)


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
    register_command("difer", difer)
    register_command("permisos", permisos)
    register_command("usuario", usuario)
    register_command("propietario", propietario)
    register_command("contrasenha", contrasenha)
    register_command("ayuda", ayuda)
    register_command("DOftp", doFTP)
    register_command("demonio", demonio)
    register_command("doShell", doShell)

def main():
    # Init shell before starting the main loop
    init()
    shell_loop()

if __name__ == "__main__":
    userLogin()
    main()
