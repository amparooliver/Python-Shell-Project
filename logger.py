import logging

from logging import FileHandler
from logging import Formatter

LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
LOG_LEVEL = logging.INFO

# Sistema Error logger NO OLVIDAR CAMBIAR DIRECCION 
SYSTEM_ERROR_LOG_FILE = "/home/aoliver/Documents/sistema_error.log"
sysError_logger = logging.getLogger("home.aoliver.Documents.hola.sistema_error")
sysError_logger.setLevel(LOG_LEVEL)
sysError_logger_file_handler = FileHandler(SYSTEM_ERROR_LOG_FILE)
sysError_logger_file_handler.setLevel(LOG_LEVEL)
sysError_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
sysError_logger.addHandler(sysError_logger_file_handler)

# Usuario Horarios logger NO OLVIDAR CAMBIAR DIRECCION 
USUARIO_HORARIOS_LOG_FILE = "/home/aoliver/Documents/usuario_horarios_log.log"
usuario_logger = logging.getLogger("home.aoliver.Documents.hola.usuario_horarios_log")
usuario_logger.setLevel(LOG_LEVEL)
usuario_logger_file_handler = FileHandler(USUARIO_HORARIOS_LOG_FILE)
usuario_logger_file_handler.setLevel(LOG_LEVEL)
usuario_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
usuario_logger.addHandler(usuario_logger_file_handler)

# Usuario Horarios logger NO OLVIDAR CAMBIAR DIRECCION 
USUARIO_TRANSFERENCIAS_LOG_FILE = "/home/aoliver/Documents/Shell_transferencias.log"
usuTransfer_logger = logging.getLogger("home.aoliver.Documents.hola.Shell_transferencias")
usuTransfer_logger.setLevel(LOG_LEVEL)
usuTransfer_logger_file_handler = FileHandler(USUARIO_TRANSFERENCIAS_LOG_FILE)
usuTransfer_logger_file_handler.setLevel(LOG_LEVEL)
usuTransfer_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
usuTransfer_logger.addHandler(usuTransfer_logger_file_handler)
