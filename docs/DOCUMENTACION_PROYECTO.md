# Maverik Vector Store - Documentación del Proyecto

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración e Instalación](#configuración-e-instalación)
5. [Uso del Sistema](#uso-del-sistema)
6. [Comandos Disponibles](#comandos-disponibles)
7. [Gestión de Documentos](#gestión-de-documentos)
8. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
9. [Consideraciones Técnicas](#consideraciones-técnicas)
10. [Resolución de Problemas](#resolución-de-problemas)

---

## Descripción General

Maverik Vector Store es un sistema de almacenamiento vectorial diseñado para procesar, indexar y buscar documentos financieros utilizando tecnologías de inteligencia artificial. El sistema convierte documentos en representaciones vectoriales que permiten búsquedas semánticas avanzadas.

### Características Principales
- **Procesamiento de documentos PDF y JSON** con texto completo
- **Embeddings vectoriales** utilizando OpenAI text-embedding-3-small (1024 dimensiones)
- **Almacenamiento en MongoDB Atlas** con Vector Search
- **Búsqueda semántica** por similitud vectorial
- **Arquitectura containerizada** con Docker
- **Sistema de logging** y monitoreo integrado
- **Gestión automatizada** de espacio y recursos

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    Maverik Vector Store                     │
├─────────────────────────────────────────────────────────────┤
│  Input Layer: PDF/JSON Documents → files/                  │
├─────────────────────────────────────────────────────────────┤
│  Processing Layer:                                          │
│  ├── Document Loaders (PDF/JSON)                           │
│  ├── Text Splitters                                        │
│  ├── OpenAI Embeddings                                     │
│  └── Caching System                                        │
├─────────────────────────────────────────────────────────────┤
│  Storage Layer:                                             │
│  ├── MongoDB Atlas (512MB Free Tier)                       │
│  ├── Vector Index (1024 dimensions)                        │
│  └── Metadata Storage                                      │
├─────────────────────────────────────────────────────────────┤
│  Interface Layer:                                           │
│  ├── Command Line Tools                                    │
│  ├── Interactive Search                                    │
│  └── Monitoring Scripts                                    │
└─────────────────────────────────────────────────────────────┘
```

### Tecnologías Utilizadas
- **Python 3.11** - Runtime principal
- **LangChain** - Framework para procesamiento de documentos y embeddings
- **OpenAI API** - Generación de embeddings vectoriales
- **MongoDB Atlas** - Base de datos vectorial
- **Docker & Docker Compose** - Containerización
- **PyPDF** - Procesamiento de documentos PDF

---

## Estructura del Proyecto

```
maverik_vector_store/
├── src/                           # Código fuente principal
│   ├── config.py                  # Configuraciones del sistema
│   ├── embedding/                 # Gestión de embeddings
│   │   └── openai_embeddings.py   # Integración con OpenAI
│   ├── loaders/                   # Cargadores de documentos
│   │   ├── json_loader.py         # Procesamiento de JSON
│   │   └── pdf_loader.py          # Procesamiento de PDF
│   ├── utils/                     # Utilidades del sistema
│   │   ├── logger.py              # Sistema de logging
│   │   └── splitter.py            # Particionado de texto
│   └── vectorstore/               # Gestión de base de datos vectorial
│       └── mongodb_vectorstore.py # Integración con MongoDB
├── scripts/                       # Scripts de operación
│   ├── check_index.py             # Verificación de índices
│   ├── check_space.py             # Monitoreo de espacio
│   ├── cleanup_db.py              # Limpieza de base de datos
│   ├── ingest.py                  # Proceso de ingesta principal
│   ├── log_analyzer.py            # Análisis de logs
│   └── search.py                  # Motor de búsqueda
├── files/                         # 📁 DIRECTORIO DE DOCUMENTOS
│   ├── aboutWarrenBuffet/         # Documentos sobre Warren Buffett
│   ├── books/                     # Libros financieros
│   └── finanzasPersonales/        # Finanzas personales
├── tests/                         # Tests unitarios
├── docs/                          # Documentación
├── logs/                          # Archivos de log
├── embedding_cache/               # Caché de embeddings
├── docker-compose.yml             # Configuración de contenedores
├── Dockerfile                     # Imagen de Docker
├── requirements.txt               # Dependencias de Python
├── run.bat                        # Script de comandos (Windows)
└── run.sh                         # Script de comandos (Linux/macOS)
```

---

## Configuración e Instalación

### Prerrequisitos
1. **Docker** y **Docker Compose** instalados
2. **Cuenta OpenAI** con API key
3. **MongoDB Atlas** configurado (tier gratuito suficiente)
4. **Git** para clonación del repositorio

### Pasos de Instalación

#### 1. Clonar el Repositorio
```bash
git clone <repository-url>
cd maverik_vector_store
```

#### 2. Configuración Inicial
```bash
# Windows
run.bat setup

# Linux/macOS
./run.sh setup
```

#### 3. Configurar Variables de Entorno
Editar el archivo `.env` creado:
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=maverik_vector_store
MONGODB_COLLECTION=documents

# Vector Search Configuration
VECTOR_INDEX_NAME=vector_index
EMBEDDING_DIMENSIONS=1024

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/maverik.log
```

#### 4. Construir la Imagen Docker
```bash
# Windows
run.bat build

# Linux/macOS
./run.sh build
```

#### 5. Verificar Configuración
```bash
# Windows
run.bat check-index
run.bat check-space

# Linux/macOS
./run.sh check-index
./run.sh check-space
```

---

## Uso del Sistema

### Flujo de Trabajo Típico

#### 1. Preparar Documentos
**IMPORTANTE:** Coloca todos los documentos que deseas procesar en el directorio `files/`:

```bash
files/
├── categoria1/
│   ├── documento1.pdf
│   ├── documento2.json
│   └── documento3.pdf
├── categoria2/
│   └── libro_financiero.pdf
└── documento_raiz.pdf
```

**Formatos Soportados:**
- **PDF**: Extracción automática de texto
- **JSON**: Estructura con campos `content`, `title`, `source`, etc.

#### 2. Ejecutar Ingesta
```bash
# Windows
run.bat ingest

# Linux/macOS
./run.sh ingest
```

El proceso de ingesta:
1. Escanea recursivamente el directorio `files/`
2. Procesa cada documento (PDF → texto, JSON → contenido)
3. Divide el texto en chunks manejables
4. Genera embeddings vectoriales via OpenAI
5. Almacena en MongoDB Atlas con metadatos

#### 3. Buscar Documentos
```bash
# Windows
run.bat search

# Linux/macOS
./run.sh search
```

Ejemplo de búsqueda interactiva:
```
Ingresa tu consulta: estrategias de inversión de Warren Buffett
Idioma (es/en): es
Fuente específica (opcional): 
Número de resultados (1-20): 5
¿Mostrar scores? (y/n): y

Resultados encontrados:
1. [Score: 0.89] Warren Buffett Investment Strategies
   Fuente: The Essays of Warren Buffett.pdf
   "Las estrategias de inversión de largo plazo..."

2. [Score: 0.85] Value Investing Principles
   Fuente: Buffettology.pdf
   "Los principios fundamentales del value investing..."
```

---

## Comandos Disponibles

### Comandos de Operación Principal

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `setup` | Configuración inicial del proyecto | `run.bat setup` |
| `build` | Construir imagen Docker | `run.bat build` |
| `ingest` | Ejecutar ingesta completa de documentos | `run.bat ingest` |
| `search` | Búsqueda interactiva de documentos | `run.bat search` |

### Comandos de Monitoreo

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `check-space` | Verificar espacio disponible en MongoDB | `run.bat check-space` |
| `check-index` | Verificar configuración del índice vectorial | `run.bat check-index` |
| `stats` | Mostrar estadísticas de la base de datos | `run.bat stats` |

### Comandos de Mantenimiento

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `clean` | Limpiar caché de embeddings | `run.bat clean` |
| `cleanup` | **PELIGROSO** - Limpiar base de datos completa | `run.bat cleanup` |
| `logs` | Mostrar logs del contenedor | `run.bat logs` |
| `log-stats` | Estadísticas de archivos de log | `run.bat log-stats` |
| `log-errors` | Errores recientes en logs | `run.bat log-errors` |

### Comandos de Desarrollo

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `test` | Ejecutar tests unitarios | `run.bat test` |
| `shell` | Abrir shell en el contenedor | `run.bat shell` |

---

## Gestión de Documentos

### Añadir Nuevos Documentos

#### Proceso Recomendado:
1. **Organizar por categorías** en subdirectorios dentro de `files/`
2. **Nombrar archivos** de forma descriptiva
3. **Verificar espacio** antes de ingesta masiva
4. **Ejecutar ingesta** para procesar nuevos documentos

#### Ejemplo de Organización:
```bash
files/
├── estrategias_inversion/
│   ├── warren_buffett_estrategias.pdf
│   ├── value_investing_guide.pdf
│   └── analisis_financiero.json
├── educacion_financiera/
│   ├── finanzas_personales_basico.pdf
│   └── presupuesto_familiar.pdf
└── mercados_financieros/
    ├── derivatives_trading.pdf
    └── market_analysis.json
```

### Verificación Antes de Ingesta

**SIEMPRE ejecutar antes de procesar documentos grandes:**
```bash
run.bat check-space
```

Salida típica:
```
**Maverik Vector Store - Verificación de Espacio**

Cluster: MaverikCluster (M0 Sandbox - 512MB)
Base de datos: maverik_vector_store
Uso actual: 156.2 MB (30.5%)
Espacio disponible: 355.8 MB (69.5%)

**SEGURO PROCEDER** con la ingesta
Ejecutar: run.bat ingest

**Desglose por Tipo de Documento**
   aboutWarrenBuffet: 45 documentos
   books: 32 documentos
   finanzasPersonales: 18 documentos

Total de documentos: 95
```

### Limpieza Selectiva

Para limpiar documentos específicos:
```bash
run.bat cleanup
```

Opciones disponibles:
1. **Limpieza completa** - Elimina TODOS los documentos
2. **Por categoría** - Elimina documentos de una carpeta específica
3. **Por idioma** - Elimina documentos en español o inglés
4. **Cancelar** - No eliminar nada

---

## Monitoreo y Mantenimiento

### Verificación de Salud del Sistema

#### 1. Estado del Índice Vectorial
```bash
run.bat check-index
```

Verifica:
- Existencia del índice vectorial
- Configuración correcta (1024 dimensiones)
- Funcionalidad de búsqueda vectorial

#### 2. Espacio de Almacenamiento
```bash
run.bat check-space
```

Monitorea:
- Uso actual vs. límite de 512MB
- Distribución por categorías
- Recomendaciones de espacio

#### 3. Análisis de Logs
```bash
# Estadísticas generales
run.bat log-stats

# Errores recientes
run.bat log-errors
```

### Mantenimiento Preventivo

#### Limpieza de Caché (Recomendado Semanalmente)
```bash
run.bat clean
```

#### Monitoreo de Espacio (Antes de Ingesta Grande)
```bash
run.bat check-space
```

#### Respaldo de Configuración
- Respaldar archivo `.env`
- Documentar cambios en configuración de MongoDB
- Mantener logs importantes

---

## Consideraciones Técnicas

### Limitaciones del Sistema

#### MongoDB Atlas (Tier Gratuito)
- **Límite:** 512MB de almacenamiento total
- **Estimación:** ~2,000-3,000 documentos típicos
- **Recomendación:** Monitorear espacio regularmente

#### OpenAI API
- **Costo:** ~$0.0001 por 1K tokens de entrada
- **Optimización:** Caché de embeddings para evitar recálculos
- **Límites:** Rate limits según plan de OpenAI

#### Rendimiento
- **Ingesta:** ~10-50 documentos/minuto (depende del tamaño)
- **Búsqueda:** <1 segundo para consultas típicas
- **Memoria:** ~512MB RAM durante ingesta

### Configuraciones Avanzadas

#### Ajuste de Chunk Size
En `src/utils/splitter.py`:
```python
chunk_size=1000,      # Tamaño de fragmentos
chunk_overlap=200,    # Solapamiento entre fragmentos
```

#### Configuración de Embeddings
En `src/embedding/openai_embeddings.py`:
```python
model="text-embedding-3-small"  # Modelo de embeddings
dimensions=1024                  # Dimensiones del vector
```

#### Configuración de Logging
Niveles disponibles: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

### Optimizaciones Recomendadas

1. **Caché de Embeddings:** Habilitado por defecto para evitar recálculos
2. **Procesamiento Batch:** Procesa múltiples documentos en lotes
3. **Índices MongoDB:** Optimizados para búsqueda vectorial
4. **Compresión:** Los embeddings se almacenan optimizados

---

## Resolución de Problemas

### Problemas Comunes

#### Error: "MongoDB connection failed"
**Síntomas:** No se puede conectar a MongoDB
**Solución:**
1. Verificar credenciales en `.env`
2. Confirmar whitelist de IP en MongoDB Atlas
3. Verificar string de conexión

```bash
# Verificar conexión
run.bat check-index
```

#### Error: "OpenAI API key invalid"
**Síntomas:** Error de autenticación con OpenAI
**Solución:**
1. Verificar API key en `.env`
2. Confirmar saldo/créditos en cuenta OpenAI
3. Verificar límites de rate

#### Error: "No space left on device" (MongoDB)
**Síntomas:** Base de datos llena
**Solución:**
1. Verificar uso actual: `run.bat check-space`
2. Limpiar documentos innecesarios: `run.bat cleanup`
3. Considerar upgrade de MongoDB Atlas

#### Error: "Document processing failed"
**Síntomas:** Fallos durante ingesta
**Solución:**
1. Verificar formato de documentos
2. Revisar logs: `run.bat log-errors`
3. Procesar documentos en lotes más pequeños

### Comandos de Diagnóstico

```bash
# Estado general del sistema
run.bat check-index && run.bat check-space

# Logs detallados
run.bat logs

# Estadísticas completas
run.bat stats

# Shell para debugging
run.bat shell
```

### Logs del Sistema

Los logs se almacenan en:
- `logs/maverik.log` - Log principal
- `logs/error.log` - Solo errores
- `logs/critical.log` - Errores críticos

Niveles de log:
- **INFO:** Operaciones normales
- **WARNING:** Situaciones que requieren atención
- **ERROR:** Errores recuperables
- **CRITICAL:** Errores que requieren intervención inmediata

---

## Contacto y Soporte

Para soporte técnico o preguntas:
1. Revisar esta documentación
2. Verificar logs del sistema
3. Consultar documentos adicionales en `docs/`

### Documentación Adicional
- `docs/TECHNICAL_CONSIDERATIONS.md` - Consideraciones técnicas detalladas
- `docs/OPTIMIZACIONES.md` - Guías de optimización
- `docs/README.md` - Información básica del proyecto

---

**Última actualización:** 29 de septiembre de 2025
**Versión del sistema:** 0.1.0