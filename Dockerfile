# Imagen base con Python 3.11
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Maverik Team <maverik@example.com>"
LABEL version="0.1.0"
LABEL description="Maverik Vector Store - Sistema de almacenamiento vectorial para documentos financieros"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Crear usuario no-root para seguridad
RUN groupadd -r maverik && useradd -r -g maverik maverik

# Copiar archivos de dependencias
COPY requirements.txt pyproject.toml ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY files/ ./files/

# Crear directorios necesarios
RUN mkdir -p ./embedding_cache ./logs

# Cambiar propietario de archivos
RUN chown -R maverik:maverik /app

# Cambiar a usuario no-root
USER maverik

# Comando por defecto
CMD ["python", "scripts/ingest.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.vectorstore.mongodb_vectorstore import MongoDBVectorStore; from src.embedding.openai_embeddings import OpenAIEmbeddingManager; vs = MongoDBVectorStore(OpenAIEmbeddingManager()); print('OK' if vs.test_connection() else exit(1))"