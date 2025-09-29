"""
Script principal para la ingesta de documentos.
"""
import sys
from pathlib import Path
from typing import List

from langchain_core.documents import Document

from src.config import get_settings
from src.embedding.openai_embeddings import OpenAIEmbeddingManager
from src.loaders.json_loader import JSONDocumentLoader
from src.loaders.pdf_loader import PDFDocumentLoader
from src.utils.logger import get_logger, measure_time
from src.utils.splitter import DocumentSplitter
from src.vectorstore.mongodb_vectorstore import MongoDBVectorStore

# Configuración global
settings = get_settings()
logger = get_logger()


class DocumentProcessor:
    """Procesador principal de documentos."""
    
    def __init__(self):
        """Inicializa el procesador de documentos."""
        self.pdf_loader = PDFDocumentLoader()
        self.json_loader = JSONDocumentLoader()
        self.splitter = DocumentSplitter()
        self.embedding_manager = OpenAIEmbeddingManager()
        self.vector_store = MongoDBVectorStore(self.embedding_manager)
        
        logger.log_event('document_processor_initialized')
    
    @measure_time
    def process_all_files(self) -> List[Document]:
        """Procesa todos los archivos PDF del directorio files principal."""
        logger.log_event('processing_all_files_started')
        
        metadata = {
            "idioma": "mixed",
            "description": "Documentos de finanzas y estrategias de inversión (conjunto simplificado para pruebas)"
        }
        
        return self.pdf_loader.load_pdfs_from_directory(
            settings.files_path,
            metadata
        )
    
    # Métodos originales comentados para referencia futura
    # @measure_time
    # def process_books(self) -> List[Document]:
    #     """Procesa libros en inglés."""
    #     logger.log_event('processing_books_started')
    #     
    #     metadata = {
    #         "idioma": "en",
    #         "description": "Libros de finanzas en ingles para obtener conocimientos financieros."
    #     }
    #     
    #     return self.pdf_loader.load_pdfs_from_directory(
    #         settings.books_path,
    #         metadata
    #     )
    # 
    # @measure_time
    # def process_finanzas_personales(self) -> List[Document]:
    #     """Procesa documentos de finanzas personales."""
    #     logger.log_event('processing_finanzas_personales_started')
    #     
    #     metadata = {
    #         "idioma": "es",
    #         "description": "Documentos en español para obtener conocimientos de finanzas personales."
    #     }
    #     
    #     return self.pdf_loader.load_pdfs_from_directory(
    #         settings.finanzas_personales_path,
    #         metadata
    #     )
    # 
    # @measure_time
    # def process_warren_buffet_books(self) -> List[Document]:
    #     """Procesa libros sobre Warren Buffet."""
    #     logger.log_event('processing_warren_buffet_books_started')
    #     
    #     metadata = {
    #         "idioma": "en",
    #         "description": "Libros en ingles sobre warren buffett y sus estrategias financieras."
    #     }
    #     
    #     return self.pdf_loader.load_pdfs_from_directory(
    #         settings.warren_buffet_path,
    #         metadata
    #     )
    
    @measure_time
    def process_warren_buffet_faq(self) -> List[Document]:
        """Procesa FAQ de Warren Buffet."""
        logger.log_event('processing_warren_buffet_faq_started')
        
        return self.json_loader.load_warren_buffet_faq(
            settings.warren_buffet_faq_path
        )
    
    @measure_time
    def run_full_ingestion(self) -> None:
        """Ejecuta la ingesta completa de documentos."""
        logger.log_event('full_ingestion_started')
        
        try:
            # Verificar conexión a MongoDB
            if not self.vector_store.test_connection():
                error_msg = "No se pudo conectar a MongoDB Atlas. Verificar credenciales y conectividad."
                logger.log_critical_error(
                    error_type="ConnectionError",
                    error_message=error_msg,
                    context={
                        "mongodb_uri": settings.mongodb_uri[:50] + "..." if len(settings.mongodb_uri) > 50 else settings.mongodb_uri,
                        "db_name": settings.db_name,
                        "collection_name": settings.collection_name
                    }
                )
                raise ConnectionError(error_msg)
            
            # 1. Procesar PDFs desde directorio files principal (simplificado)
            logger.log_event('processing_pdfs_started')
            all_documents = []
            
            try:
                # Procesar todos los archivos PDF del directorio files
                all_docs = self.process_all_files()
                all_documents.extend(all_docs)
                
                logger.log_event(
                    'pdf_processing_complete',
                    total_documents=len(all_documents),
                    files_processed=len(all_docs)
                )
                
                print(f"Procesados {len(all_documents)} documentos PDF desde {settings.files_path}")
                
            except Exception as e:
                logger.log_critical_error(
                    error_type="DocumentProcessingError",
                    error_message=f"Error procesando documentos PDF: {str(e)}",
                    context={
                        "files_path": str(settings.files_path),
                        "documents_processed": len(all_documents)
                    }
                )
                raise
            
            # 2. Dividir documentos
            if all_documents:
                logger.log_event('splitting_documents_started')
                try:
                    split_docs = self.splitter.split_documents(all_documents)
                    
                    # 3. Añadir documentos divididos al vector store
                    logger.log_event('adding_split_documents_started')
                    self.vector_store.add_documents(
                        split_docs, 
                        batch_size=settings.batch_size
                    )
                    
                except Exception as e:
                    logger.log_critical_error(
                        error_type="VectorStoreError",
                        error_message=f"Error añadiendo documentos al vector store: {str(e)}",
                        context={
                            "total_documents": len(all_documents),
                            "split_documents": len(split_docs) if 'split_docs' in locals() else 0,
                            "batch_size": settings.batch_size
                        }
                    )
                    raise
            
            # 4. Procesar JSON (Warren Buffet FAQ) - COMENTADO PARA SIMPLIFICAR PRUEBAS
            # logger.log_event('processing_json_started')
            # 
            # # Importar función de monitoreo de espacio
            # try:
            #     from scripts.check_space import monitor_during_ingestion
            #     space_monitor_available = True
            #     logger.log_event('space_monitor_enabled')
            # except ImportError:
            #     logger.log_error("No se puede importar monitor de espacio, continuando sin monitoreo")
            #     space_monitor_available = False
            # 
            # try:
            #     faq_docs = self.process_warren_buffet_faq()
            #     
            #     if faq_docs:
            #         # Verificar espacio antes de procesar JSON
            #         if space_monitor_available:
            #             logger.log_event('space_check_before_json')
            #             if not monitor_during_ingestion():
            #                 error_msg = "Espacio insuficiente para procesar documentos JSON"
            #                 logger.log_critical_error(
            #                     error_type="SpaceQuotaExceeded", 
            #                     error_message=error_msg,
            #                     context={"phase": "before_json_processing", "docs_count": len(faq_docs)}
            #                 )
            #                 print(f"\n🚨 {error_msg}")
            #                 print(f"🧹 Ejecutar: run.bat cleanup")
            #                 print(f"📊 Verificar espacio: run.bat check-space")
            #                 return
            #         
            #         logger.log_event('adding_json_documents_started')
            #         self.vector_store.add_documents(
            #             faq_docs, 
            #             batch_size=settings.json_batch_size
            #         )
            #         
            # except Exception as e:
            #     logger.log_critical_error(
            #         error_type="JSONProcessingError",
            #         error_message=f"Error procesando FAQ JSON: {str(e)}",
            #         context={
            #             "faq_path": str(settings.warren_buffet_faq_path),
            #             "json_batch_size": settings.json_batch_size
            #         }
            #     )
            #     raise
            
            print(f"Procesamiento JSON omitido para simplificar pruebas")
            logger.log_event('json_processing_skipped', reason='simplified_testing')
            
            # 5. Estadísticas finales
            try:
                collection_stats = self.vector_store.get_collection_stats()
                cache_stats = self.embedding_manager.get_cache_stats()
                
                logger.log_event(
                    'full_ingestion_complete',
                    **collection_stats,
                    **cache_stats
                )
                
            except Exception as e:
                logger.log_event(
                    'stats_error',
                    level='WARNING',
                    error=str(e)
                )
                # No es crítico si las estadísticas fallan
                pass
            
        except Exception as e:
            logger.log_event(
                'full_ingestion_error',
                level='ERROR',
                error=str(e)
            )
            
            # Si es un error no manejado específicamente, loggearlo como crítico
            if not isinstance(e, ConnectionError):
                logger.log_critical_error(
                    error_type="UnhandledError",
                    error_message=f"Error no manejado en ingesta: {str(e)}",
                    context={
                        "function": "run_full_ingestion",
                        "error_class": type(e).__name__
                    }
                )
            
            raise
        
        finally:
            # Cerrar conexiones
            try:
                self.vector_store.close_connection()
                logger.log_event('connections_closed')
            except Exception as e:
                logger.log_event(
                    'connection_close_error',
                    level='WARNING',
                    error=str(e)
                )
    
    @measure_time
    def test_search(self, query: str = "quien es warren buffet", k: int = 2) -> None:
        """Prueba de búsqueda."""
        logger.log_event('test_search_started', query=query, k=k)
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            
            print(f"\nResultados de búsqueda para: '{query}'")
            print("=" * 60)
            
            for i, result in enumerate(results, 1):
                print(f"\nResultado {i}:")
                print(f"Contenido: {result.page_content[:200]}...")
                print(f"Metadatos: {result.metadata}")
            
            logger.log_event(
                'test_search_complete',
                query=query,
                results_count=len(results)
            )
            
        except Exception as e:
            logger.log_event(
                'test_search_error',
                level='ERROR',
                query=query,
                error=str(e)
            )
            raise


def main():
    """Función principal."""
    try:
        processor = DocumentProcessor()
        
        # Verificar argumentos de línea de comandos
        if len(sys.argv) > 1:
            if sys.argv[1] == "--test-search":
                query = sys.argv[2] if len(sys.argv) > 2 else "quien es warren buffet"
                processor.test_search(query)
                return
            
            elif sys.argv[1] == "--stats":
                try:
                    collection_stats = processor.vector_store.get_collection_stats()
                    cache_stats = processor.embedding_manager.get_cache_stats()
                    
                    print("\nEstadísticas de la colección:")
                    for key, value in collection_stats.items():
                        print(f"  {key}: {value}")
                    
                    print("\nEstadísticas del caché:")
                    for key, value in cache_stats.items():
                        print(f"  {key}: {value}")
                        
                except Exception as e:
                    logger.log_critical_error(
                        error_type="StatsError",
                        error_message=f"Error obteniendo estadísticas: {str(e)}",
                        context={"command": "--stats"}
                    )
                    print(f"Error obteniendo estadísticas: {e}")
                    sys.exit(1)
                return
        
        # Ejecutar ingesta completa por defecto
        print("Procesando archivos desde el directorio files...")
        print(f"Directorio de archivos: {settings.project_root / 'files'}")
        print(f"Caché de embeddings: {settings.project_root / 'embedding_cache'}")
        print(f"Logs: {settings.project_root / 'logs'}")
        print("-" * 60)
        
        processor.run_full_ingestion()
        print("Ingesta completada exitosamente!")
        print(f"Revisa los logs en: {settings.project_root / 'logs'}")
        
    except KeyboardInterrupt:
        logger.log_event('process_interrupted', level='WARNING')
        print("\nProceso interrumpido por el usuario")
        sys.exit(1)
        
    except ConnectionError as e:
        logger.log_critical_error(
            error_type="ConnectionError",
            error_message=str(e),
            context={
                "main_function": True,
                "mongodb_config": {
                    "uri_provided": bool(settings.mongodb_uri),
                    "db_name": settings.db_name
                }
            }
        )
        print(f"\nError de conexión: {e}")
        print("Soluciones:")
        print("   1. Verificar credenciales en .env")
        print("   2. Verificar conectividad a MongoDB Atlas")
        print("   3. Verificar whitelist de IPs en MongoDB Atlas")
        sys.exit(1)
        
    except Exception as e:
        logger.log_critical_error(
            error_type="MainError",
            error_message=f"Error crítico en función principal: {str(e)}",
            context={
                "main_function": True,
                "error_class": type(e).__name__,
                "argv": sys.argv
            }
        )
        print(f"\nError crítico en el proceso: {e}")
        print(f"Revisa los logs de errores en: {settings.project_root / 'logs' / 'critical_errors.log'}")
        sys.exit(1)


if __name__ == "__main__":
    main()