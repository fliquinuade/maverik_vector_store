"""
Manejador de MongoDB Atlas Vector Store.
"""
from typing import List, Optional

from langchain_core.documents import Document
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from src.config import get_settings
from src.embedding.openai_embeddings import OpenAIEmbeddingManager
from src.utils.logger import get_logger, measure_time

settings = get_settings()
logger = get_logger()


class MongoDBVectorStore:
    """Manejador del vector store de MongoDB Atlas."""
    
    def __init__(self, embedding_manager: Optional[OpenAIEmbeddingManager] = None):
        """Inicializa el vector store de MongoDB."""
        self.embedding_manager = embedding_manager or OpenAIEmbeddingManager()
        
        # Configurar cliente MongoDB
        try:
            self.client = MongoClient(
                settings.mongodb_uri,
                connectTimeoutMS=3600000,  # 1 hora
                serverSelectionTimeoutMS=5000  # 5 segundos
            )
            
            # Verificar conexión
            self.client.admin.command('ping')
            logger.log_event('mongodb_connected')
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.log_event(
                'mongodb_connection_error',
                level='ERROR',
                error=str(e)
            )
            raise
        
        # Configurar colección
        self.db = self.client[settings.db_name]
        self.collection = self.db[settings.collection_name]
        
        # Inicializar vector store
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embedding_manager.embeddings,
            index_name=settings.atlas_vector_search_index_name,
            relevance_score_fn="cosine",
        )
        
        logger.log_event(
            'vector_store_initialized',
            db_name=settings.db_name,
            collection_name=settings.collection_name,
            index_name=settings.atlas_vector_search_index_name
        )
    
    @measure_time
    def add_documents(
        self, 
        documents: List[Document], 
        batch_size: Optional[int] = None
    ) -> List[str]:
        """Añade documentos al vector store."""
        if not documents:
            logger.log_event('no_documents_to_add', level='WARNING')
            return []
        
        batch_size = batch_size or settings.batch_size
        
        try:
            # Procesar en lotes
            all_ids = []
            total_batches = (len(documents) + batch_size - 1) // batch_size
            
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                
                logger.log_event(
                    'processing_batch',
                    batch_number=batch_num,
                    total_batches=total_batches,
                    batch_size=len(batch)
                )
                
                try:
                    ids = self.vector_store.add_documents(
                        documents=batch,
                        batch_size=len(batch)
                    )
                    all_ids.extend(ids)
                    
                    logger.log_database_operation(
                        operation='add_documents_batch',
                        status='success',
                        doc_count=len(batch)
                    )
                    
                except Exception as e:
                    logger.log_database_operation(
                        operation='add_documents_batch',
                        status='error',
                        doc_count=len(batch),
                        error=str(e)
                    )
                    raise
            
            logger.log_database_operation(
                operation='add_documents_complete',
                status='success',
                doc_count=len(documents)
            )
            
            return all_ids
            
        except Exception as e:
            logger.log_database_operation(
                operation='add_documents',
                status='error',
                doc_count=len(documents),
                error=str(e)
            )
            raise
    
    @measure_time
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[Document]:
        """Realiza búsqueda por similitud."""
        try:
            # Configurar filtros si se proporcionan
            search_kwargs = {}
            if filter_dict:
                search_kwargs['filter'] = filter_dict
            
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                **search_kwargs
            )
            
            logger.log_event(
                'similarity_search_complete',
                query_length=len(query),
                k=k,
                results_count=len(results),
                filter_applied=filter_dict is not None
            )
            
            return results
            
        except Exception as e:
            logger.log_event(
                'similarity_search_error',
                level='ERROR',
                query_length=len(query),
                k=k,
                error=str(e)
            )
            raise
    
    @measure_time
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Optional[dict] = None
    ) -> List[tuple]:
        """Realiza búsqueda por similitud con scores."""
        try:
            search_kwargs = {}
            if filter_dict:
                search_kwargs['filter'] = filter_dict
            
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                **search_kwargs
            )
            
            logger.log_event(
                'similarity_search_with_score_complete',
                query_length=len(query),
                k=k,
                results_count=len(results),
                filter_applied=filter_dict is not None
            )
            
            return results
            
        except Exception as e:
            logger.log_event(
                'similarity_search_with_score_error',
                level='ERROR',
                query_length=len(query),
                k=k,
                error=str(e)
            )
            raise
    
    def get_collection_stats(self) -> dict:
        """Obtiene estadísticas de la colección."""
        try:
            stats = self.db.command("collStats", settings.collection_name)
            
            collection_stats = {
                'document_count': stats.get('count', 0),
                'size_bytes': stats.get('size', 0),
                'size_mb': stats.get('size', 0) / (1024 * 1024),
                'index_count': stats.get('nindexes', 0),
                'avg_obj_size': stats.get('avgObjSize', 0)
            }
            
            logger.log_event('collection_stats_retrieved', **collection_stats)
            
            return collection_stats
            
        except Exception as e:
            logger.log_event(
                'collection_stats_error',
                level='ERROR',
                error=str(e)
            )
            raise
    
    def test_connection(self) -> bool:
        """Prueba la conexión a MongoDB."""
        try:
            self.client.admin.command('ping')
            logger.log_event('connection_test_success')
            return True
            
        except Exception as e:
            logger.log_event(
                'connection_test_failed',
                level='ERROR',
                error=str(e)
            )
            return False
    
    def close_connection(self) -> None:
        """Cierra la conexión a MongoDB."""
        try:
            self.client.close()
            logger.log_event('mongodb_connection_closed')
            
        except Exception as e:
            logger.log_event(
                'mongodb_close_error',
                level='ERROR',
                error=str(e)
            )