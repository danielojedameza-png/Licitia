"""
Configuración de logging para LicitIA

Configura el sistema de logging con rotación de archivos y diferentes niveles.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Crear directorio de logs si no existe
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Nombre del archivo de log
LOG_FILE = LOGS_DIR / "licitia.log"

# Formato de logs
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logging(
    level=logging.INFO,
    log_to_file=True,
    log_to_console=True,
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5
):
    """
    Configura el sistema de logging.
    
    Args:
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Si True, guarda logs en archivo
        log_to_console: Si True, muestra logs en consola
        max_bytes: Tamaño máximo del archivo de log antes de rotar
        backup_count: Número de archivos de respaldo a mantener
    """
    
    # Crear logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Limpiar handlers existentes
    root_logger.handlers.clear()
    
    # Formato
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    
    # Handler para archivo con rotación
    if log_to_file:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Handler para consola
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # Reducir verbosidad de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    
    return root_logger

def get_logger(name):
    """
    Obtiene un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger (típicamente __name__)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)

# Logger por defecto para la aplicación
logger = get_logger("licitia")
