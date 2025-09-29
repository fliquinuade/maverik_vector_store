# Maverik Vector Store - Documentación

## 📚 Índice de Documentación

### 📖 Documentos Principales

| Documento | Descripción | Audiencia |
|-----------|-------------|-----------|
| **[DOCUMENTACION_PROYECTO.md](DOCUMENTACION_PROYECTO.md)** | 📋 **Documentación completa del sistema** - Arquitectura, instalación, configuración y uso detallado | Desarrolladores y administradores |
| **[GUIA_USO_PRACTICO.md](GUIA_USO_PRACTICO.md)** | 🎯 **Ejemplos prácticos paso a paso** - Escenarios reales de uso y resolución de problemas | Usuarios finales |
| **[REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md)** | ⚡ **Referencia rápida de comandos** - Cheatsheet para uso diario | Todos los usuarios |

### 📑 Documentos Técnicos

| Documento | Descripción |
|-----------|-------------|
| **[TECHNICAL_CONSIDERATIONS.md](TECHNICAL_CONSIDERATIONS.md)** | 🔧 Consideraciones técnicas avanzadas |
| **[OPTIMIZACIONES.md](OPTIMIZACIONES.md)** | 🚀 Guías de optimización del sistema |

---

## 🚀 Inicio Rápido

### Para Nuevos Usuarios
1. **Leer primero**: [DOCUMENTACION_PROYECTO.md](DOCUMENTACION_PROYECTO.md) - Secciones 1-5
2. **Configurar**: Seguir la sección "Configuración e Instalación"
3. **Practicar**: [GUIA_USO_PRACTICO.md](GUIA_USO_PRACTICO.md) - Escenario 1

### Para Uso Diario
- **Consulta rápida**: [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md)
- **Comandos básicos**: `run.bat help` o `./run.sh help`

---

## 🎯 Descripción del Proyecto

**Maverik Vector Store** es un sistema de almacenamiento y búsqueda vectorial especializado en documentos financieros, implementado con tecnologías de inteligencia artificial y bases de datos vectoriales. 

### ✨ Características Principales
- 🔍 **Búsqueda semántica** avanzada en documentos PDF y JSON
- 🧠 **Embeddings vectoriales** con OpenAI text-embedding-3-small
- 🗄️ **Almacenamiento** en MongoDB Atlas con Vector Search
- 🐳 **Arquitectura containerizada** con Docker
- 📊 **Sistema de monitoreo** y logging integrado
- 🌐 **Soporte multiidioma** (español e inglés)

### 📁 Contenido Incluido
- **Estrategias de Warren Buffett**: Libros y análisis especializados
- **Educación Financiera**: Guías de finanzas personales
- **Literatura Financiera**: Libros sobre trading, mercados y análisis

---

## 🎯 Audiencias

### 👨‍💻 Desarrolladores
- Revisar [DOCUMENTACION_PROYECTO.md](DOCUMENTACION_PROYECTO.md) para arquitectura completa
- Consultar [TECHNICAL_CONSIDERATIONS.md](TECHNICAL_CONSIDERATIONS.md) para detalles técnicos

### 👤 Usuarios Finales
- Comenzar con [GUIA_USO_PRACTICO.md](GUIA_USO_PRACTICO.md) para ejemplos paso a paso
- Usar [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) como consulta diaria

### 🔧 Administradores
- Leer secciones de "Monitoreo y Mantenimiento" en documentación principal
- Revisar [OPTIMIZACIONES.md](OPTIMIZACIONES.md) para mejores prácticas

---

## ⚡ Comandos Más Utilizados

```bash
# Configuración inicial
run.bat setup           # Crear archivo .env
run.bat build            # Construir imagen Docker

# Operaciones principales  
run.bat ingest          # Procesar documentos
run.bat search           # Búsqueda interactiva
run.bat check-space      # Verificar espacio (IMPORTANTE)

# Mantenimiento
run.bat logs             # Ver logs del sistema
run.bat clean            # Limpiar caché
```

---

## 📊 Estado del Sistema

### Capacidad Actual
- **MongoDB Atlas**: 512MB (tier gratuito)
- **Documentos procesados**: ~95 documentos
- **Categorías**: Warren Buffett, Finanzas Personales, Literatura Financiera

### Últimas Actualizaciones
- ✅ Sistema de limpieza de código completado
- ✅ Documentación completa actualizada
- ✅ Scripts de comando optimizados
- ✅ Sistema de monitoreo mejorado

---

## 🆘 Soporte

### Para Problemas Técnicos
1. Consultar [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) - Sección "Resolución Rápida"
2. Revisar logs: `run.bat log-errors`
3. Consultar documentación técnica detallada

### Para Dudas de Uso
1. Revisar [GUIA_USO_PRACTICO.md](GUIA_USO_PRACTICO.md)
2. Consultar ejemplos paso a paso
3. Verificar configuración con `run.bat check-index`

---

**📅 Última actualización**: 29 de septiembre de 2025  
**📋 Versión del sistema**: 0.1.0

1. **LangChain Framework**
   - `langchain`: Framework principal para el procesamiento de documentos y embeddings
   - `langchain_community`: Extensiones comunitarias para loaders de documentos
   - `langchain_openai`: Integración con modelos de OpenAI
   - `langchain-mongodb`: Conectores para MongoDB Atlas

2. **Base de Datos Vectorial**
   - **MongoDB Atlas Vector Search**: Base de datos NoSQL con capacidades de búsqueda vectorial
   - Índice vectorial: `vector_index`
   - Función de relevancia: Coseno (cosine similarity)

3. **Modelos de IA**
   - **OpenAI Embeddings**: Modelo `text-embedding-3-small` con 1024 dimensiones
   - Requiere API Key de OpenAI configurada en variables de entorno

4. **Procesamiento de Documentos**
   - **PyPDF**: Para extracción de texto de archivos PDF
   - **JSONLoader**: Para procesamiento de datos estructurados JSON
   - **RecursiveCharacterTextSplitter**: Para segmentación inteligente de documentos

5. **Entorno de Desarrollo**
   - **Google Colab**: Entorno de desarrollo principal (configurable para VS Code)
   - **Python 3.x**: Lenguaje de programación base

## Estructura de Datos

### Colecciones de Documentos

El sistema procesa tres categorías principales de documentos:

1. **Libros de Finanzas en Inglés** (`files/books/`)
   - Libros especializados en mercados financieros, análisis de inversiones y trading
   - Metadatos: `idioma: "en"`, categoría: finanzas generales

2. **Documentos de Finanzas Personales** (`files/finanzasPersonales/`)
   - Manuales y materiales en español sobre finanzas personales
   - Metadatos: `idioma: "es"`, categoría: finanzas personales

3. **Documentos sobre Warren Buffett** (`files/aboutWarrenBuffet/`)
   - Libros biográficos y sobre estrategias de inversión de Warren Buffett
   - FAQ estructurado con preguntas y respuestas sobre Buffett
   - Metadatos: `idioma: "en"`, categoría: Warren Buffett

### Estructura de Metadatos

Cada documento procesado incluye metadatos estructurados:

```json
{
  "source": "nombre_del_archivo.pdf",
  "idioma": "en|es",
  "description": "Descripción contextual del contenido"
}
```

## Configuración de Servicios Externos

### MongoDB Atlas

**Configuración requerida:**
- URI de conexión: `mongodb+srv://[usuario]:[password]@cluster0.8frt8.mongodb.net/`
- Base de datos: `langchain_db`
- Colección: `langchain_vectorstores`
- Índice vectorial: `vector_index`

**Configuración del índice vectorial en MongoDB Atlas:**
```javascript
{
  "fields": [
    {
      "numDimensions": 1024,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

### OpenAI API

**Configuración requerida:**
- Variable de entorno: `OPENAI_API_KEY`
- Modelo de embeddings: `text-embedding-3-small`
- Dimensiones: 1024

## Flujo de Procesamiento

### 1. Carga de Documentos
```python
# PDFs → PyPDFLoader → Documentos individuales
# JSON → JSONLoader → Datos estructurados
```

### 2. Segmentación de Texto
```python
# RecursiveCharacterTextSplitter
# chunk_size: 1024 caracteres
# chunk_overlap: 256 caracteres
```

### 3. Generación de Embeddings
```python
# OpenAI text-embedding-3-small
# Dimensiones: 1024
# Procesamiento en lotes de 500 documentos
```

### 4. Almacenamiento Vectorial
```python
# MongoDB Atlas Vector Search
# Función de similitud: cosine
# Indexación automática
```

### 5. Búsqueda Semántica
```python
# similarity_search(query, k=n)
# Retorna documentos más relevantes
```

## Consideraciones de Desarrollo

### Escalabilidad y Rendimiento

1. **Procesamiento por Lotes**
   - PDFs: Lotes de 500 documentos
   - JSON: Lotes de 1 documento (para datos sensibles)
   - Configuración de memoria: `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`

2. **Optimización de Memoria**
   - Segmentación inteligente de documentos grandes
   - Liberación de memoria entre procesamientos
   - Manejo de timeouts en conexiones MongoDB

### Seguridad y Configuración

1. **Gestión de Credenciales**
   - API Keys almacenadas en variables de entorno
   - Credenciales de MongoDB no hardcodeadas en código
   - Uso de Google Colab secrets/userdata

2. **Conexiones de Red**
   - Timeout de conexión MongoDB: 3,600,000 ms (1 hora)
   - Reintentos automáticos en MongoDB
   - Manejo de excepciones en conexiones

### Limitaciones Actuales

1. **Dependencia de Google Colab**
   - Configuración específica para Google Drive
   - Rutas hardcodeadas para Colab

2. **Escalabilidad de Costos**
   - Dependencia de OpenAI API (costos por embedding)
   - Límites de rate limiting de OpenAI

3. **Idiomas Soportados**
   - Principalmente inglés y español
   - Sin procesamiento específico por idioma

## Roadmap de Desarrollo

### Mejoras Inmediatas

1. **Portabilidad del Código**
   - Eliminar dependencias específicas de Google Colab
   - Configuración flexible de rutas y entornos
   - Dockerización del proyecto

2. **Interfaz de Usuario**
   - API REST para búsquedas
   - Interface web para consultas
   - Dashboard de administración

3. **Monitoreo y Logging**
   - Logging estructurado de operaciones
   - Métricas de rendimiento
   - Alertas automáticas

### Mejoras a Mediano Plazo

1. **Procesamiento Avanzado**
   - Soporte para más formatos de documento
   - Extracción de metadatos automática
   - Procesamiento multiidioma

2. **Optimización de Embeddings**
   - Cacheo de embeddings
   - Modelos locales como alternativa
   - Compresión de vectores

3. **Funcionalidades Avanzadas**
   - Búsqueda híbrida (texto + vector)
   - Clustering automático de documentos
   - Recomendaciones basadas en contenido

## Estructura de Archivos del Proyecto

```
maverik_vector_store/
├── README.md
├── vector-store-mongoDB-openai.ipynb    # Notebook principal
├── docs/
│   └── README.md                        # Esta documentación
└── files/
    ├── books/                           # Libros de finanzas (inglés)
    ├── finanzasPersonales/              # Finanzas personales (español)
    └── aboutWarrenBuffet/               # Contenido sobre Warren Buffett
        ├── buffett_faq.json            # FAQ estructurado
        └── *.pdf                       # Libros sobre Buffett
```

## Guía de Instalación y Configuración

### Prerequisitos

1. **Python 3.8+**
2. **Cuenta MongoDB Atlas** con cluster configurado
3. **API Key de OpenAI** con acceso a embeddings
4. **Google Colab** (o entorno Jupyter local)

### Instalación de Dependencias

```bash
pip install langchain
pip install langchain_community pypdf
pip install langchain-mongodb pymongo
pip install langchain_openai
pip install jq
```

### Configuración de Variables de Entorno

```python
# En Google Colab
from google.colab import userdata
os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')

# En entorno local
import os
os.environ["OPENAI_API_KEY"] = "tu_api_key_aqui"
```

### Configuración de MongoDB

1. Crear cluster en MongoDB Atlas
2. Configurar índice vectorial en la colección
3. Obtener URI de conexión
4. Configurar whitelist de IPs

## Casos de Uso

### Búsquedas Especializadas

1. **Consultas sobre Warren Buffett**
   ```python
   results = vector_store.similarity_search("estrategias de inversión de Warren Buffett", k=5)
   ```

2. **Finanzas Personales en Español**
   ```python
   results = vector_store.similarity_search("cómo hacer un presupuesto personal", k=3)
   ```

3. **Análisis Técnico y Trading**
   ```python
   results = vector_store.similarity_search("análisis técnico de mercados financieros", k=4)
   ```

## Contacto y Contribuciones

Este proyecto forma parte del ecosistema **Maverik** para herramientas financieras basadas en IA. Para contribuciones o consultas técnicas, revisar la documentación técnica específica en el notebook principal.

---

**Última actualización:** Septiembre 2025  
**Versión:** 1.0.0  
**Mantenedor:** Equipo Maverik Development