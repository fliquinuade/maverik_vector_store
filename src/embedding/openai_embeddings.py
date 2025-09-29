"""
Manejador de embeddings de OpenAI.
"""
import hashlib
import pickle
import time
from pathlib import Path
from typing import List, Optional

from langchain_openai import OpenAIEmbeddings

from src.config import get_settings
from src.utils.logger import get_logger, measure_time

settings = get_settings()
logger = get_logger()


class OpenAIEmbeddingManager:
    """Manejador de embeddings de OpenAI con caché local."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Inicializa el manejador de embeddings."""
        self.embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            dimensions=settings.embedding_dimensions,
            openai_api_key=settings.openai_api_key
        )
        
        # Configurar directorio de caché
        self.cache_dir = Path(cache_dir) if cache_dir else Path("./embedding_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        logger.log_event(
            'embedding_manager_initialized',
            model=settings.embedding_model,
            dimensions=settings.embedding_dimensions,
            cache_dir=str(self.cache_dir)
        )
    
    def _get_cache_key(self, text: str) -> str:
        """Genera una clave de caché para el texto."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _get_cache_file(self, cache_key: str) -> Path:
        """Obtiene la ruta del archivo de caché."""
        return self.cache_dir / f"{cache_key}.pkl"
    
    def _load_from_cache(self, text: str) -> Optional[List[float]]:
        """Carga un embedding desde caché."""
        try:
            cache_key = self._get_cache_key(text)
            cache_file = self._get_cache_file(cache_key)
            
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    embedding = pickle.load(f)
                
                logger.log_event(
                    'embedding_cache_hit',
                    text_length=len(text),
                    cache_key=cache_key[:16]
                )
                
                return embedding
            
            return None
            
        except Exception as e:
            logger.log_event(
                'embedding_cache_error',
                level='WARNING',
                text_length=len(text),
                error=str(e)
            )
            return None
    
    def _save_to_cache(self, text: str, embedding: List[float]) -> None:
        """Guarda un embedding en caché."""
        try:
            cache_key = self._get_cache_key(text)
            cache_file = self._get_cache_file(cache_key)
            
            with open(cache_file, 'wb') as f:
                pickle.dump(embedding, f)
            
            logger.log_event(
                'embedding_cached',
                text_length=len(text),
                cache_key=cache_key[:16]
            )
            
        except Exception as e:
            logger.log_event(
                'embedding_cache_save_error',
                level='WARNING',
                text_length=len(text),
                error=str(e)
            )
    
    @measure_time
    def embed_query(self, text: str) -> List[float]:
        """Genera embedding para una consulta."""
        # Intentar cargar desde caché
        cached_embedding = self._load_from_cache(text)
        if cached_embedding is not None:
            return cached_embedding
        
        # Generar nuevo embedding
        try:
            start_time = time.time()
            embedding = self.embeddings.embed_query(text)
            duration = time.time() - start_time
            
            # Guardar en caché
            self._save_to_cache(text, embedding)
            
            logger.log_embedding_generation(
                text_length=len(text),
                status='success',
                duration=duration
            )
            
            return embedding
            
        except Exception as e:
            logger.log_embedding_generation(
                text_length=len(text),
                status='error',
                error=str(e)
            )
            raise
    
    @measure_time
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Genera embeddings para múltiples documentos."""
        embeddings_result = []
        cache_hits = 0
        api_calls = 0
        
        for text in texts:
            # Intentar cargar desde caché
            cached_embedding = self._load_from_cache(text)
            if cached_embedding is not None:
                embeddings_result.append(cached_embedding)
                cache_hits += 1
                continue
            
            # Generar nuevo embedding
            try:
                start_time = time.time()
                embedding = self.embeddings.embed_query(text)
                duration = time.time() - start_time
                
                # Guardar en caché
                self._save_to_cache(text, embedding)
                
                embeddings_result.append(embedding)
                api_calls += 1
                
                logger.log_embedding_generation(
                    text_length=len(text),
                    status='success',
                    duration=duration
                )
                
                # Rate limiting básico
                if api_calls % 100 == 0:
                    time.sleep(1)
                
            except Exception as e:
                logger.log_embedding_generation(
                    text_length=len(text),
                    status='error',
                    error=str(e)
                )
                raise
        
        logger.log_event(
            'batch_embedding_complete',
            total_texts=len(texts),
            cache_hits=cache_hits,
            api_calls=api_calls,
            cache_hit_rate=cache_hits / len(texts) if texts else 0
        )
        
        return embeddings_result
    
    def clear_cache(self) -> None:
        """Limpia el caché de embeddings."""
        try:
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
            
            logger.log_event('cache_cleared')
            
        except Exception as e:
            logger.log_event(
                'cache_clear_error',
                level='ERROR',
                error=str(e)
            )
            raise
    
    def get_cache_stats(self) -> dict:
        """Obtiene estadísticas del caché."""
        try:
            cache_files = list(self.cache_dir.glob("*.pkl"))
            total_size = sum(f.stat().st_size for f in cache_files)
            
            stats = {
                'cache_files': len(cache_files),
                'total_size_bytes': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'cache_dir': str(self.cache_dir)
            }
            
            logger.log_event('cache_stats_retrieved', **stats)
            
            return stats
            
        except Exception as e:
            logger.log_event(
                'cache_stats_error',
                level='ERROR',
                error=str(e)
            )
            raise