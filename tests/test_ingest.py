"""
Tests unitarios para el procesamiento de documentos.
"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.loaders.pdf_loader import PDFDocumentLoader
from src.loaders.json_loader import JSONDocumentLoader
from src.utils.splitter import DocumentSplitter


class TestPDFLoader(unittest.TestCase):
    """Tests para el cargador de PDFs."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.loader = PDFDocumentLoader()
    
    def test_pdf_loader_initialization(self):
        """Test de inicialización del cargador PDF."""
        self.assertIsInstance(self.loader, PDFDocumentLoader)
    
    @patch('src.loaders.pdf_loader.PyPDFLoader')
    def test_load_pdf_success(self, mock_pdf_loader):
        """Test de carga exitosa de PDF."""
        # Mock del loader
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Mock()]
        mock_pdf_loader.return_value = mock_loader_instance
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            # Test
            documents = self.loader.load_pdf(temp_path)
            self.assertTrue(len(documents) > 0)
            mock_pdf_loader.assert_called_once()
            
        finally:
            # Limpiar
            if temp_path.exists():
                temp_path.unlink()
    
    def test_load_pdf_file_not_found(self):
        """Test de error cuando el archivo no existe."""
        non_existent_path = Path("non_existent_file.pdf")
        
        with self.assertRaises(FileNotFoundError):
            self.loader.load_pdf(non_existent_path)
    
    def test_load_pdf_invalid_extension(self):
        """Test de error con extensión de archivo inválida."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            with self.assertRaises(ValueError):
                self.loader.load_pdf(temp_path)
        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestJSONLoader(unittest.TestCase):
    """Tests para el cargador de JSON."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.loader = JSONDocumentLoader()
    
    def test_json_loader_initialization(self):
        """Test de inicialización del cargador JSON."""
        self.assertIsInstance(self.loader, JSONDocumentLoader)
    
    @patch('src.loaders.json_loader.JSONLoader')
    def test_load_warren_buffet_faq_success(self, mock_json_loader):
        """Test de carga exitosa del FAQ de Warren Buffet."""
        # Mock del loader
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [Mock()]
        mock_json_loader.return_value = mock_loader_instance
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            # Test
            documents = self.loader.load_warren_buffet_faq(temp_path)
            self.assertTrue(len(documents) > 0)
            mock_json_loader.assert_called_once()
            
        finally:
            # Limpiar
            if temp_path.exists():
                temp_path.unlink()


class TestDocumentSplitter(unittest.TestCase):
    """Tests para el divisor de documentos."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.splitter = DocumentSplitter(chunk_size=100, chunk_overlap=20)
    
    def test_splitter_initialization(self):
        """Test de inicialización del divisor."""
        self.assertIsInstance(self.splitter, DocumentSplitter)
        self.assertEqual(self.splitter.chunk_size, 100)
        self.assertEqual(self.splitter.chunk_overlap, 20)
    
    def test_split_text(self):
        """Test de división de texto."""
        text = "Este es un texto largo que debería ser dividido en chunks más pequeños. " * 10
        
        chunks = self.splitter.split_text(text)
        
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 120)  # chunk_size + overlap
    
    @patch('src.utils.splitter.RecursiveCharacterTextSplitter')
    def test_split_documents(self, mock_text_splitter):
        """Test de división de documentos."""
        # Mock del text splitter
        mock_splitter_instance = Mock()
        mock_splitter_instance.split_documents.return_value = [Mock(), Mock()]
        mock_text_splitter.return_value = mock_splitter_instance
        
        # Mock documents
        mock_documents = [Mock(), Mock()]
        
        # Test
        result = self.splitter.split_documents(mock_documents)
        
        self.assertEqual(len(result), 2)
        mock_splitter_instance.split_documents.assert_called_once_with(mock_documents)


if __name__ == '__main__':
    unittest.main()