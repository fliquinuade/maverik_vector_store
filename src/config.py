"""
Configuración central del proyecto Maverik Vector Store.
"""
import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API Key")
    
    # MongoDB Configuration
    mongodb_uri: str = Field(..., description="MongoDB Atlas connection URI")
    db_name: str = Field(default="langchain_db", description="Database name")
    collection_name: str = Field(default="langchain_vectorstores", description="Collection name")
    atlas_vector_search_index_name: str = Field(default="vector_index", description="Vector search index name")
    
    # Embedding Configuration
    embedding_model: str = Field(default="text-embedding-3-small", description="OpenAI embedding model")
    embedding_dimensions: int = Field(default=1024, description="Embedding dimensions")
    
    # Processing Configuration (optimizada para espacio y monitoreo)
    chunk_size: int = Field(default=512, description="Text chunk size for splitting (reducido para optimizar espacio)")
    chunk_overlap: int = Field(default=100, description="Text chunk overlap (reducido para optimizar espacio)")
    batch_size: int = Field(default=25, description="Batch size for processing documents (reducido para mejor monitoreo)")
    json_batch_size: int = Field(default=1, description="Batch size for JSON documents")
    
    # Space Management Configuration (nueva configuración)
    space_check_interval: int = Field(default=100, description="Intervalo de documentos para verificar espacio")
    max_space_usage_mb: float = Field(default=480.0, description="Máximo uso de espacio antes de alertar (MB)")
    critical_space_threshold_mb: float = Field(default=500.0, description="Umbral crítico de espacio (MB)")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    
    # File Paths
    files_dir: str = Field(default="files", description="Base files directory")
    books_dir: str = Field(default="files/books", description="Books directory")
    finanzas_personales_dir: str = Field(default="files/finanzasPersonales", description="Personal finance directory")
    warren_buffet_dir: str = Field(default="files/aboutWarrenBuffet", description="Warren Buffet directory")
    warren_buffet_faq_file: str = Field(default="files/aboutWarrenBuffet/buffett_faq.json", description="Warren Buffet FAQ file")
    
    # Project root
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    
    def get_absolute_path(self, relative_path: str) -> Path:
        """Convierte una ruta relativa en absoluta basada en project_root."""
        return self.project_root / relative_path
    
    @property
    def files_path(self) -> Path:
        """Ruta absoluta al directorio base de archivos."""
        return self.get_absolute_path(self.files_dir)
    
    @property
    def books_path(self) -> Path:
        """Ruta absoluta al directorio de libros."""
        return self.get_absolute_path(self.books_dir)
    
    @property
    def finanzas_personales_path(self) -> Path:
        """Ruta absoluta al directorio de finanzas personales."""
        return self.get_absolute_path(self.finanzas_personales_dir)
    
    @property
    def warren_buffet_path(self) -> Path:
        """Ruta absoluta al directorio de Warren Buffet."""
        return self.get_absolute_path(self.warren_buffet_dir)
    
    @property
    def warren_buffet_faq_path(self) -> Path:
        """Ruta absoluta al archivo FAQ de Warren Buffet."""
        return self.get_absolute_path(self.warren_buffet_faq_file)


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """Obtiene la configuración de la aplicación."""
    return settings