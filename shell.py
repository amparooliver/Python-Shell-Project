#!/usr/bin/env python3
import crypt
import datetime
import difflib
import ftplib
import getpass
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

# CONSTANTS
SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1

# Loggers
from logger import (sysError_logger, usuario_logger, usuComandos_logger,
                    usuTransfer_logger)

# FUNCTIONS #
# Function to register user login
def userLogin():
    user = getpass.getuser()
    ip = str(socket.gethostbyname(socket.gethostname()))
    str1 =' LOGIN REGISTER: username: ' + user + ' IP:' + ip + ' date:' + '\n'  
    usuario_logger.info(str1)

# Function to register user logout
def userLogout():
    user = getpass.getuser()
    ip = str(socket.gethostbyname(socket.gethostname()))
    str1 =' LOGOUT REGISTER: username: ' + user + ' IP:' + ip + ' date:' + '\n'  
    usuario_logger.info(str1)

# Function to register user transfers (ftp / scp)
def userTransfer(args):
    user = getpass.getuser()
    str1 =' USER TRANSFER REGISTER (ftp/scp): username: ' + user + ' date:' + ' command:' + args + '\n'  
    usuTransfer_logger.info(str1)

# Function to register user commands
def userCommands(args):
    user = getpass.getuser()
    currentDate = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    str2 = currentDate + ' command: ' + args + ' username: ' + user + '\n'  
    usuComandos_logger.info(str2)

# Function that returns hashed password (for useradd command)
def hash_password(password):
    salt = ''.join([random.choice(string.ascii_letters + string.digits)
            for _ in range(16)])
    prefix = '$6$'
    return crypt.crypt(password, prefix + salt)

# Function that reads File line by line into a list
def readFile(filename):
    with open(filename) as file:
        lines = file.readlines() 
        lines = [line.rstrip() for line in lines] # removes all whitespace characters
    return lines

# Function that splits file string into a list by : parameter.
def splitText(file):
    listFile = list(file)
    for i in range(len(listFile)):
        listFile[i] = listFile[i].split(':')
    return listFile

# Function that generates a new User Id (Linux starts at 1000)
def generateuserId():
    userId = 1000
    file = readFile("/etc/passwd")  
    for i in range(len(file)):
        file[i] = file[i].split(':')
    for i in range(len(file)):
        if userId < int(file[i][2]):
            userId = int(file[i][2])
    userId = userId + 1
    return userId

# COMMANDS #
# exit command: Stops the Shell from running
def exits(args):
    userLogout()
    userCommands('exit')
    output = os.popen('exit').read()
    print (output)
    return SHELL_STATUS_STOP

# 6. ir command: Changes the current working directory to path.
def ir(args):
    # Argument verifications
    if len(args) > 1:
        print("ir: Too many arguments")
        sysError_logger.error("ir: Too many arguments")
        return SHELL_STATUS_RUN
    elif len(args) == 0:
        os.chdir(os.getenv('HOME'))
        userCommands('ir')
    elif len(args) == 1:
        try:
            os.chdir(os.path.abspath(args[0])) # args[0] --> path
            userCommands(" ".join(['ir', args[0]]))
        except OSError as error: 
            print(error)
            sysError_logger.exception(error)
    return SHELL_STATUS_RUN

# 5. creardir command: Creates a directory named path.
def creardir(args):
    try: 
        os.mkdir(args[0]) # args[0] --> path
        userCommands(" ".join(['creardir', args[0]]))
    except OSError as error: 
        print(error)  
        sysError_logger.exception(error)
    return SHELL_STATUS_RUN

# 4. listar command: Prints a list containing the names of the entries in path.
def listar(args):
    # Argument verifications
    if len(args) < 1:
        path = os.getcwd() # If no path was provided, get cwd
    elif len(args) > 1:
        print("listar: Too many arguments")
        sysError_logger.error("listar: Too many arguments")
        return SHELL_STATUS_RUN
    else:
        # Check if path exists
        if os.path.isdir(os.path.abspath(args[0])):
            if len(args) == 1:
                path = os.path.abspath(args[0]) # args[0] --> path
        else:
            print("listar: Path does not exist")
            sysError_logger.error("listar: Path does not exist")
            return SHELL_STATUS_RUN
    try: 
        dir_list = os.listdir(path) 
        userCommands(" ".join(['listar', path]))
        print(dir_list)
    except OSError as error: 
        print(error)
        sysError_logger.exception(error)  
    return SHELL_STATUS_RUN

# 3. renombrar command: Rename the file or directory src to dst.
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
        os.rename(os.path.abspath(args[0]), os.path.abspath(args[1])) # args[0] --> src ; args[1] --> dst
        userCommands('renombrar '+args[0]+' '+args[1])
    except OSError as error: 
        print(error)
        sysError_logger.exception(error)  
    return SHELL_STATUS_RUN

# 2. mover command: moves a file or directory src to dst.
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
        shutil.move(os.path.abspath(args[0]), os.path.abspath(args[1])) # args[0] --> src ; args[1] --> dst
        userCommands('mover '+args[0]+' '+args[1])
    except Exception as er:       
        sysError_logger.exception(er)
        print(er)
    return SHELL_STATUS_RUN

# copiar command: Copies the file src to the file or directory dst. 
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
        shutil.copy(os.path.abspath(args[0]), os.path.abspath(args[1])) # args[0] --> src ; args[1] --> dst
        userCommands('copiar '+args[0]+' '+args[1])
    except Exception as er:       
        sysError_logger.exception(er)
        print(er)
    return SHELL_STATUS_RUN

# 15. grupos command: Prints list of group ids that user belongs to.
def grupos(args):
    if len(args) == 1: 
        user = args[0]
        try:
            pwd.getpwnam(user) 
        except KeyError:
            print("grupos: User does not exist")
            sysError_logger.error("grupos: User does not exist")
            return SHELL_STATUS_RUN
        gid = pwd.getpwnam(user).pw_gid 
    elif len(args) == 2: 
        user = args[0]
        try:
            pwd.getpwnam(user) 
        except KeyError:
            print("grupos: User does not exist")
            sysError_logger.error("grupos: User does not exist")
            return SHELL_STATUS_RUN
        gid = int(args[1])
    elif len(args) == 0:
        user = getpass.getuser()
        gid = pwd.getpwnam(user).pw_gid
    elif len(args) > 2:
        print("grupos: Too many arguments")
        sysError_logger.error("grupos: Too many arguments")
        return SHELL_STATUS_RUN
    try: 
        group_list = os.getgrouplist(user, gid) 
        userCommands('grupos '+user)
        print(group_list)
    except OSError as error: 
        print(error)  
        sysError_logger.exception(error)
    return SHELL_STATUS_RUN

# permisos command: Changes the mode of path to the numeric mode.
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
            userCommands('permisos '+args[0]+' '+args[1])
        except OSError as error: 
            print(error)  
            sysError_logger.exception(error)
    return SHELL_STATUS_RUN

# 15. difer command: displays the differences in the files by comparing the files line by line.
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
            userCommands('difer '+args[0]+' '+args[1])
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

# 10. usuario command: adds user to system with personal info
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
            files = []
            files.append(readFile("/etc/shadow"))
            files.append(readFile("/etc/passwd"))
            files.append(readFile("/etc/group"))
            for i in range(3):
                files[i] = splitText(files[i])
            # Check if username already exists
            for i in range(len(files[1])):
                # 1 --> "/etc/passwd" // i --> to check line by line // 0 --> position of username 
                if files[1][i][0] == username:
                    sysError_logger.error(username + " already exists")
                    return SHELL_STATUS_RUN
            # Get new user ID group ID
            userId = generateuserId()
            groupId = userId # By default, it usually is the same
            # New home directory for User
            homePath = "/home/" + username 
            if(os.path.exists("/home/" + username) == 0):
                os.mkdir(homePath,int('755',8))
            # Ask for password
            password = getpass.getpass()
            # Crypt password
            newHash = hash_password(password)
            # Ask Personal information
            fullname=input("Fullname: ")
            ip = str(socket.gethostbyname(socket.gethostname()))
            sWork=input("Start work time HH:MM: ")
            sWork=sWork.replace(":","")
            oWork=input("Off-work time HH:MM: ")
            oWork=oWork.replace(":","")
            # Append to files
            files[0] = open("/etc/shadow","a+")
            files[1] = open("/etc/passwd","a+")
            files[2] = open("/etc/group","a+")
            epoch = int(time.time())
            # The information is written in the corresponding files
            # username: login name // newHash: password // epoch: last passwd change // 0: minimum // 99999: maximum // 7: warn
            files[0].write(f"{username}:{newHash}:{epoch}:0:99999:7:::\n")
            # username: login name // x: passw // userId: UID// groupId: GID // User ID Info GECOS // Home directory // Command/shell
            files[1].write(f"{username}:x:{userId}:{groupId}:{fullname},{ip},{sWork},{oWork}:{homePath}:/bin/bash\n")
            # username: group name // x: passw // groupId: GID 
            files[2].write(f"{username}:x:{groupId}:\n")
            userCommands('usuario '+args[0])
            files[0].close()
            files[1].close()
            files[2].close()
        else:
            print("usuario: User does not have root privileges")
            sysError_logger.error("usuario: User does not have root privileges")

    return SHELL_STATUS_RUN

# 8. propietario command: Changes the owner and /or group of the specified path. 
def propietario(args):
    if len(args) > 3:
        print("propietario: Too many arguments")
        sysError_logger.error("propietario: Too many arguments")
    elif len(args) < 2:
        print("propietario: Missing arguments")
        sysError_logger.error("propietario: Missing arguments")
    else:
        path = os.path.abspath(args[0]) # args[0] --> path
        user = args[1]
        try:
            pwd.getpwnam(user) # Check if User exists
        except KeyError:
            print("propietario: User does not exist")
            sysError_logger.error("propietario: User does not exist")
            return SHELL_STATUS_RUN
        try: 
            shutil.chown(path, user, user)
            userCommands('propietario '+args[0]+' '+args[1])
        except Exception as er:       
            sysError_logger.exception(er)
            print(er)

    return SHELL_STATUS_RUN   

# 9. contrasenha command: Sets and changes the password of a user.
def contrasenha(args):
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
            userColShadow = 0
            userColPasswd = 0
            fileStrings = [0,0]
            fileAttributes = [0,0]     
            # Read files
            for i in range(2):
                fileStrings[i] = readFile(paths[i])
                fileAttributes[i] = splitText(fileStrings[i])
            # Check if user exists in files
            for i in range(len(fileAttributes[0])):
                if fileAttributes[0][i][0] == username:
                    userColShadow = i
            for i in range(len(fileAttributes[1])):
                if fileAttributes[1][i][0] == username:
                    userColPasswd = i    
            # If user is found in files      
            if userColShadow != 0 or userColPasswd != 0:
                # Ask for password
                password = getpass.getpass()
                # Crypt password
                newHash = hash_password(password)
                # Update arrays 
                fileStrings[0][userColShadow] = f"{username}:{newHash}:{fileAttributes[0][userColShadow][2]}:{fileAttributes[0][userColShadow][3]}:{fileAttributes[0][userColShadow][4]}:{fileAttributes[0][userColShadow][5]}:::"
                fileStrings[1][userColPasswd] = f"{username}:x:{fileAttributes[1][userColPasswd][2]}:{fileAttributes[1][userColPasswd][3]}:{fileAttributes[1][userColPasswd][4]}:{fileAttributes[1][userColPasswd][5]}:{fileAttributes[1][userColPasswd][6]}"
                passwdFake = open("/etc/passwd","w+")
                # Update passwd & shadow files
                for i in range(len(fileStrings[1])):
                    passwdFake.write(fileStrings[1][i])
                    passwdFake.write("\n")
                shadowFake = open("/etc/shadow","w+")
                for i in range(len(fileStrings[0])):    
                    shadowFake.write(fileStrings[0][i])
                    shadowFake.write("\n")
                userCommands('contrasenha '+args[0])
            else:
                print("contrasenha: User does not exist")
                sysError_logger.error("contrasenha: User does not exist")         
        else:
            print("contrasenha: User does not have root privileges")
            sysError_logger.error("contrasenha: User does not have root privileges")

    return SHELL_STATUS_RUN

# help command: Prints list of all built-in commands.
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
    cm13 = """
    doFTP: ftp domain.com
    Transfers files to and from a remote network.
    """
    cm14 = """
    demonio: demonio levantar/apagar pid
    Runs and kills daemons by id.
    """
    cm15 = """
    doShell: doShell unixCommand
    Allows the use of system commands. 
    """
    # Argument verifications
    if len(args) > 1:
        print("help: Too many arguments")
        sysError_logger.error("help: Too many arguments")
    elif len(args) == 0:
        print("AYUDA")
        print(f"{cm1}\n{cm2}\n{cm3}\n{cm4}\n{cm5}\n{cm6}\n{cm7}\n{cm8}\n{cm9}\n{cm10}\n{cm11}\n{cm12}\n")
        userCommands('ayuda ')
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
        if args[0] == "doFTP": print(cm13)  
        if args[0] == "demonios": print(cm14)
        if args[0] == "doShell": print(cm15)     
        userCommands('ayuda '+args[0])   
    return SHELL_STATUS_RUN

# 14. doFTP command: transfers files to and from a remote network.
def doFTP(args):
    if len(args) < 1:
        print("doFTP: Missing arguments")
        sysError_logger.error("doFTP: Missing arguments")
    else:
        try:
            str1 = ' '.join(map(str, args)) 
            os.system(str1)
            userTransfer(str1)
            userCommands('ftp '+str1)
        except Exception as e:
            print(e)
            sysError_logger.error(e)
    return SHELL_STATUS_RUN

# 11. demonio command: runs and kills daemons by id.
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
                userCommands('demonio '+args[0]+' '+args[1])
            except Exception as e:
                print(e)
                sysError_logger.error(e)
                print('Demonio: Non valid argument.')
        elif(args[0]=='apagar'):
            try:
                pid=int(args[1])
                os.kill(pid, signal.SIGTERM)
                os.kill(pid, signal.SIGKILL)
                userCommands('demonio '+args[0]+' '+args[1])
            except Exception as e:
                print(e)
                sysError_logger.error(e)
                print('Demonio: Non valid argument.')
    return SHELL_STATUS_RUN

# 12. doShell command: allows to use system commands. 
def doShell(args):
    if len(args) < 1:
        print("doShell: Missing arguments")
        sysError_logger.error("doShell: Missing arguments")
    else:
        str1 = ' '.join(map(str, args)) 
        output = os.popen(str1).read()
        print (output)
        str1 = ' '.join(map(str, args))
        userCommands('doShell '+ str1)

    return SHELL_STATUS_RUN

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
    register_command("doFTP", doFTP)
    register_command("demonio", demonio)
    register_command("doShell", doShell)

def main():
    # Init shell before starting the main loop
    init()
    shell_loop()

if __name__ == "__main__":
    userLogin()
    main()
