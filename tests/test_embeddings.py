"""
Tests unitarios para el sistema de embeddings.
"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.embedding.openai_embeddings import OpenAIEmbeddingManager


class TestOpenAIEmbeddingManager(unittest.TestCase):
    """Tests para el manejador de embeddings de OpenAI."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        # Usar directorio temporal para caché
        self.temp_dir = tempfile.mkdtemp()
        
        with patch('src.config.get_settings') as mock_settings:
            mock_settings.return_value.openai_api_key = "test_key"
            mock_settings.return_value.embedding_model = "text-embedding-3-small"
            mock_settings.return_value.embedding_dimensions = 1024
            
            self.manager = OpenAIEmbeddingManager(cache_dir=self.temp_dir)
    
    def test_embedding_manager_initialization(self):
        """Test de inicialización del manejador."""
        self.assertIsInstance(self.manager, OpenAIEmbeddingManager)
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_get_cache_key(self):
        """Test de generación de clave de caché."""
        text = "Este es un texto de prueba"
        cache_key = self.manager._get_cache_key(text)
        
        self.assertIsInstance(cache_key, str)
        self.assertEqual(len(cache_key), 64)  # SHA256 hash length
    
    def test_get_cache_file(self):
        """Test de obtención de archivo de caché."""
        cache_key = "test_key_123"
        cache_file = self.manager._get_cache_file(cache_key)
        
        self.assertEqual(cache_file.name, "test_key_123.pkl")
        self.assertEqual(cache_file.parent, Path(self.temp_dir))
    
    @patch.object(OpenAIEmbeddingManager, '_save_to_cache')
    @patch.object(OpenAIEmbeddingManager, '_load_from_cache')
    def test_embed_query_with_cache_hit(self, mock_load_cache, mock_save_cache):
        """Test de embed_query con hit en caché."""
        # Mock cache hit
        mock_embedding = [0.1, 0.2, 0.3]
        mock_load_cache.return_value = mock_embedding
        
        text = "texto de prueba"
        result = self.manager.embed_query(text)
        
        self.assertEqual(result, mock_embedding)
        mock_load_cache.assert_called_once_with(text)
        mock_save_cache.assert_not_called()
    
    @patch.object(OpenAIEmbeddingManager, '_save_to_cache')
    @patch.object(OpenAIEmbeddingManager, '_load_from_cache')
    def test_embed_query_with_cache_miss(self, mock_load_cache, mock_save_cache):
        """Test de embed_query con miss en caché."""
        # Mock cache miss
        mock_load_cache.return_value = None
        
        # Mock OpenAI embeddings
        mock_embedding = [0.1, 0.2, 0.3]
        with patch.object(self.manager.embeddings, 'embed_query', return_value=mock_embedding):
            text = "texto de prueba"
            result = self.manager.embed_query(text)
            
            self.assertEqual(result, mock_embedding)
            mock_load_cache.assert_called_once_with(text)
            mock_save_cache.assert_called_once_with(text, mock_embedding)
    
    def test_clear_cache(self):
        """Test de limpieza de caché."""
        # Crear algunos archivos de caché falsos
        cache_dir = Path(self.temp_dir)
        for i in range(3):
            cache_file = cache_dir / f"test_cache_{i}.pkl"
            cache_file.write_text("fake cache data")
        
        # Verificar que existen
        cache_files = list(cache_dir.glob("*.pkl"))
        self.assertEqual(len(cache_files), 3)
        
        # Limpiar caché
        self.manager.clear_cache()
        
        # Verificar que se eliminaron
        cache_files = list(cache_dir.glob("*.pkl"))
        self.assertEqual(len(cache_files), 0)
    
    def test_get_cache_stats(self):
        """Test de obtención de estadísticas de caché."""
        # Crear algunos archivos de caché falsos
        cache_dir = Path(self.temp_dir)
        for i in range(2):
            cache_file = cache_dir / f"test_cache_{i}.pkl"
            cache_file.write_text("fake cache data" * 100)
        
        # Obtener estadísticas
        stats = self.manager.get_cache_stats()
        
        self.assertIn('cache_files', stats)
        self.assertIn('total_size_bytes', stats)
        self.assertIn('total_size_mb', stats)
        self.assertIn('cache_dir', stats)
        
        self.assertEqual(stats['cache_files'], 2)
        self.assertGreater(stats['total_size_bytes'], 0)
    
    def tearDown(self):
        """Limpieza después de cada test."""
        # Limpiar directorio temporal
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()