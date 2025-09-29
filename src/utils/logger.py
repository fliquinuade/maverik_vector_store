"""
Utilidades de logging para el proyecto.
"""
import json
import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeVar

from src.config import get_settings

F = TypeVar('F', bound=Callable[..., Any])

settings = get_settings()


class StructuredLogger:
    """Logger estructurado para eventos del sistema."""
    
    def __init__(self, name: str = "maverik_vector_store"):
        """Inicializa el logger estructurado."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.log_level.upper()))
        
        if not self.logger.handlers:
            # Crear directorio de logs si no existe
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # Formatter común
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            # Handler para archivo general
            file_handler = logging.FileHandler(
                log_dir / "maverik_vector_store.log",
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # Handler para errores específicamente
            error_handler = logging.FileHandler(
                log_dir / "errors.log",
                encoding='utf-8'
            )
            error_handler.setFormatter(formatter)
            error_handler.setLevel(logging.ERROR)
            self.logger.addHandler(error_handler)
    
    def log_event(
        self, 
        event: str, 
        level: str = "INFO", 
        **kwargs: Any
    ) -> None:
        """Registra un evento estructurado."""
        log_data = {
            'event': event,
            'timestamp': time.time(),
            **kwargs
        }
        
        log_message = json.dumps(log_data, ensure_ascii=False)
        log_level = getattr(logging, level.upper())
        self.logger.log(log_level, log_message)
    
    def log_document_processing(
        self, 
        filename: str, 
        status: str, 
        doc_count: Optional[int] = None,
        error: Optional[str] = None
    ) -> None:
        """Registra eventos de procesamiento de documentos."""
        kwargs = {
            'filename': filename,
            'status': status
        }
        
        if doc_count is not None:
            kwargs['document_count'] = doc_count
        if error is not None:
            kwargs['error'] = error
            
        level = "ERROR" if error else "INFO"
        self.log_event('document_processing', level, **kwargs)
    
    def log_embedding_generation(
        self, 
        text_length: int, 
        status: str, 
        duration: Optional[float] = None,
        error: Optional[str] = None
    ) -> None:
        """Registra eventos de generación de embeddings."""
        kwargs = {
            'text_length': text_length,
            'status': status
        }
        
        if duration is not None:
            kwargs['duration_seconds'] = duration
        if error is not None:
            kwargs['error'] = error
            
        level = "ERROR" if error else "INFO"
        self.log_event('embedding_generation', level, **kwargs)
    
    def log_database_operation(
        self, 
        operation: str, 
        status: str, 
        doc_count: Optional[int] = None,
        error: Optional[str] = None
    ) -> None:
        """Registra operaciones de base de datos."""
        kwargs = {
            'operation': operation,
            'status': status
        }
        
        if doc_count is not None:
            kwargs['document_count'] = doc_count
        if error is not None:
            kwargs['error'] = error
            
        level = "ERROR" if error else "INFO"
        self.log_event('database_operation', level, **kwargs)
    
    def log_critical_error(
        self, 
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Registra errores críticos con contexto adicional."""
        log_data = {
            'event': 'critical_error',
            'error_type': error_type,
            'error_message': error_message,
            'timestamp': time.time()
        }
        
        if context:
            log_data['context'] = context
            
        log_message = json.dumps(log_data, ensure_ascii=False, indent=2)
        self.logger.critical(log_message)
        
        # También escribir en archivo de errores críticos
        critical_log_path = Path("logs") / "critical_errors.log"
        try:
            with open(critical_log_path, 'a', encoding='utf-8') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - CRITICAL ERROR\n")
                f.write(f"{log_message}\n")
                f.write("-" * 80 + "\n")
        except Exception:
            # Si no podemos escribir al archivo, al menos registramos en consola
            pass


def measure_time(func: F) -> F:
    """Decorador para medir tiempo de ejecución de funciones."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = StructuredLogger()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            logger.log_event(
                'function_execution',
                function_name=func.__name__,
                status='success',
                duration_seconds=duration
            )
            
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            # Log del error normal
            logger.log_event(
                'function_execution',
                level='ERROR',
                function_name=func.__name__,
                status='error',
                duration_seconds=duration,
                error=str(e)
            )
            
            # Log crítico si es un error grave
            if isinstance(e, (ConnectionError, ImportError, PermissionError)):
                logger.log_critical_error(
                    error_type=type(e).__name__,
                    error_message=str(e),
                    context={
                        'function': func.__name__,
                        'duration': duration,
                        'args_count': len(args),
                        'kwargs_keys': list(kwargs.keys()) if kwargs else []
                    }
                )
            
            raise
    
    return wrapper


def get_logger(name: str = "maverik_vector_store") -> StructuredLogger:
    """Obtiene una instancia del logger estructurado."""
    return StructuredLogger(name)