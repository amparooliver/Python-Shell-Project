import logging

from logging import FileHandler
from logging import Formatter

LOG_FORMAT = ("%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
LOG_LEVEL = logging.INFO

# Sistema Error logger 
SYSTEM_ERROR_LOG_FILE = "/var/log/shell/sistema_error.log"
sysError_logger = logging.getLogger("var.log.shell.sistema_error")
sysError_logger.setLevel(LOG_LEVEL)
sysError_logger_file_handler = FileHandler(SYSTEM_ERROR_LOG_FILE)
sysError_logger_file_handler.setLevel(LOG_LEVEL)
sysError_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
sysError_logger.addHandler(sysError_logger_file_handler)

# Usuario Horarios logger 
USUARIO_HORARIOS_LOG_FILE = "/var/log/shell/usuario_horarios_log.log"
usuario_logger = logging.getLogger("var.log.shell.usuario_horarios_log")
usuario_logger.setLevel(LOG_LEVEL)
usuario_logger_file_handler = FileHandler(USUARIO_HORARIOS_LOG_FILE)
usuario_logger_file_handler.setLevel(LOG_LEVEL)
usuario_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
usuario_logger.addHandler(usuario_logger_file_handler)

# Usuario Transferencias logger
USUARIO_TRANSFERENCIAS_LOG_FILE = "/var/log/shell/Shell_transferencias.log"
usuTransfer_logger = logging.getLogger("var.log.shell.Shell_transferencias")
usuTransfer_logger.setLevel(LOG_LEVEL)
usuTransfer_logger_file_handler = FileHandler(USUARIO_TRANSFERENCIAS_LOG_FILE)
usuTransfer_logger_file_handler.setLevel(LOG_LEVEL)
usuTransfer_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
usuTransfer_logger.addHandler(usuTransfer_logger_file_handler)

# Usuario Registro Comandos logger 
USUARIO_COMANDOS_LOG_FILE = "/var/log/shell/Shell_registro.log"
usuComandos_logger = logging.getLogger("var.log.shell.Shell_registro")
usuComandos_logger.setLevel(LOG_LEVEL)
usuComandos_logger_file_handler = FileHandler(USUARIO_COMANDOS_LOG_FILE)
usuComandos_logger_file_handler.setLevel(LOG_LEVEL)
usuComandos_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
usuComandos_logger.addHandler(usuComandos_logger_file_handler)