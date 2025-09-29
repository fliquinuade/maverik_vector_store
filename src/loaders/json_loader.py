"""
Cargador de documentos JSON.
"""
from pathlib import Path
from typing import Dict, List

from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document

from src.utils.logger import get_logger, measure_time

logger = get_logger()


class JSONDocumentLoader:
    """Cargador especializado para documentos JSON."""
    
    def __init__(self):
        """Inicializa el cargador de JSONs."""
        logger.log_event('json_loader_initialized')
    
    @measure_time
    def load_warren_buffet_faq(self, file_path: Path) -> List[Document]:
        """Carga el archivo FAQ de Warren Buffet."""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not file_path.suffix.lower() == '.json':
                raise ValueError(f"File is not a JSON: {file_path}")
            
            json_loader = JSONLoader(
                file_path=str(file_path),
                jq_schema='.[] | {question: .question, answer: .answer}',
                text_content=False,
            )
            
            documents = json_loader.load()
            
            # Agregar metadatos específicos para Warren Buffet FAQ
            for doc in documents:
                doc.metadata.update({
                    "source": "Warren Buffett FAQ",
                    "idioma": "en",
                    "description": "Preguntas y respuestas sobre warren buffett y sus estrategias financieras."
                })
            
            logger.log_document_processing(
                filename=file_path.name,
                status='success',
                doc_count=len(documents)
            )
            
            return documents
            
        except Exception as e:
            logger.log_document_processing(
                filename=file_path.name,
                status='error',
                error=str(e)
            )
            raise
    
    @measure_time
    def load_json(
        self, 
        file_path: Path, 
        jq_schema: str = None,
        metadata: Dict[str, str] = None
    ) -> List[Document]:
        """Carga un archivo JSON genérico."""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not file_path.suffix.lower() == '.json':
                raise ValueError(f"File is not a JSON: {file_path}")
            
            # Schema por defecto si no se proporciona
            if jq_schema is None:
                jq_schema = '.'
            
            json_loader = JSONLoader(
                file_path=str(file_path),
                jq_schema=jq_schema,
                text_content=False,
            )
            
            documents = json_loader.load()
            
            # Agregar metadatos si se proporcionan
            if metadata:
                for doc in documents:
                    doc.metadata.update(metadata)
                    doc.metadata['source'] = file_path.name
            
            logger.log_document_processing(
                filename=file_path.name,
                status='success',
                doc_count=len(documents)
            )
            
            return documents
            
        except Exception as e:
            logger.log_document_processing(
                filename=file_path.name,
                status='error',
                error=str(e)
            )
            raise