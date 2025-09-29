"""
Utilidades para división de texto.
"""
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import get_settings
from src.utils.logger import get_logger, measure_time

settings = get_settings()
logger = get_logger()


class DocumentSplitter:
    """Clase para dividir documentos en chunks."""
    
    def __init__(
        self, 
        chunk_size: int = None, 
        chunk_overlap: int = None
    ):
        """Inicializa el divisor de documentos."""
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        logger.log_event(
            'document_splitter_initialized',
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    @measure_time
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Divide una lista de documentos en chunks."""
        try:
            split_docs = self.text_splitter.split_documents(documents)
            
            logger.log_event(
                'documents_split',
                input_count=len(documents),
                output_count=len(split_docs),
                status='success'
            )
            
            return split_docs
            
        except Exception as e:
            logger.log_event(
                'documents_split',
                level='ERROR',
                input_count=len(documents),
                status='error',
                error=str(e)
            )
            raise
    
    @measure_time
    def split_text(self, text: str) -> List[str]:
        """Divide un texto en chunks."""
        try:
            chunks = self.text_splitter.split_text(text)
            
            logger.log_event(
                'text_split',
                input_length=len(text),
                output_count=len(chunks),
                status='success'
            )
            
            return chunks
            
        except Exception as e:
            logger.log_event(
                'text_split',
                level='ERROR',
                input_length=len(text),
                status='error',
                error=str(e)
            )
            raise