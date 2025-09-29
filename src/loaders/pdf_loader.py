"""
Cargador de documentos PDF.
"""
import os
from pathlib import Path
from typing import Dict, List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from src.utils.logger import get_logger, measure_time

logger = get_logger()


class PDFDocumentLoader:
    """Cargador especializado para documentos PDF."""
    
    def __init__(self):
        """Inicializa el cargador de PDFs."""
        logger.log_event('pdf_loader_initialized')
    
    @measure_time
    def load_pdf(self, file_path: Path, metadata: Dict[str, str] = None) -> List[Document]:
        """Carga un archivo PDF y retorna documentos con metadatos."""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not file_path.suffix.lower() == '.pdf':
                raise ValueError(f"File is not a PDF: {file_path}")
            
            pdf_loader = PyPDFLoader(str(file_path))
            documents = pdf_loader.load()
            
            # Agregar metadatos a cada documento
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
    
    @measure_time
    def load_pdfs_from_directory(
        self, 
        directory: Path, 
        base_metadata: Dict[str, str] = None
    ) -> List[Document]:
        """Carga todos los PDFs de un directorio."""
        try:
            if not directory.exists():
                raise FileNotFoundError(f"Directory not found: {directory}")
            
            pdf_files = list(directory.glob("*.pdf"))
            
            if not pdf_files:
                logger.log_event(
                    'no_pdfs_found',
                    directory=str(directory),
                    level='WARNING'
                )
                return []
            
            all_documents = []
            
            for pdf_file in pdf_files:
                try:
                    # Crear metadatos específicos para cada archivo
                    file_metadata = base_metadata.copy() if base_metadata else {}
                    file_metadata['source'] = pdf_file.name
                    
                    documents = self.load_pdf(pdf_file, file_metadata)
                    all_documents.extend(documents)
                    
                except Exception as e:
                    logger.log_document_processing(
                        filename=pdf_file.name,
                        status='error',
                        error=str(e)
                    )
                    # Continuar con el siguiente archivo
                    continue
            
            logger.log_event(
                'directory_processing_complete',
                directory=str(directory),
                files_processed=len(pdf_files),
                total_documents=len(all_documents)
            )
            
            return all_documents
            
        except Exception as e:
            logger.log_event(
                'directory_processing_error',
                level='ERROR',
                directory=str(directory),
                error=str(e)
            )
            raise