# Guía de Uso Práctico - Maverik Vector Store

## Ejemplos de Uso Paso a Paso

### Escenario 1: Primera Configuración y Uso

#### Paso 1: Configuración Inicial
```bash
# 1. Clonar repositorio y navegar al directorio
cd maverik_vector_store

# 2. Configuración inicial (Windows)
run.bat setup

# 3. Editar .env con tus credenciales
notepad .env
```

#### Paso 2: Preparar Documentos
```bash
# Crear estructura de documentos
mkdir files\mi_biblioteca_financiera
mkdir files\estrategias_inversion
mkdir files\analisis_mercado

# Copiar tus documentos PDF/JSON a estas carpetas
copy "C:\MisDocumentos\warren_buffett.pdf" files\estrategias_inversion\
copy "C:\MisDocumentos\analisis_sp500.json" files\analisis_mercado\
```

#### Paso 3: Verificar Sistema
```bash
# Construir imagen Docker
run.bat build

# Verificar configuración
run.bat check-index
run.bat check-space
```

#### Paso 4: Primera Ingesta
```bash
# Ejecutar ingesta completa
run.bat ingest

# Verificar resultados
run.bat stats
```

#### Paso 5: Primera Búsqueda
```bash
# Modo búsqueda interactiva
run.bat search

# Ejemplo de consulta:
# Consulta: "estrategias de inversión a largo plazo"
# Idioma: es
# Resultados: 5
```

---

### Escenario 2: Añadir Nueva Colección de Documentos

#### Situación: Tienes 50 nuevos PDFs sobre trading
```bash
# 1. Verificar espacio disponible ANTES
run.bat check-space

# Salida esperada:
# Uso actual: 156.2 MB (30.5%)
# Espacio disponible: 355.8 MB (69.5%)
# **SEGURO PROCEDER** con la ingesta

# 2. Organizar nuevos documentos
mkdir files\trading_strategies
copy "C:\NuevosLibros\*.pdf" files\trading_strategies\

# 3. Ejecutar ingesta incremental
run.bat ingest

# 4. Verificar nuevo estado
run.bat check-space
run.bat stats
```

---

### Escenario 3: Búsquedas Especializadas

#### Búsqueda por Tema Específico
```bash
run.bat search

# Consulta: "análisis técnico de mercados financieros"
# Idioma: es
# Fuente específica: trading_strategies
# Resultados: 10
# Mostrar scores: y
```

#### Búsqueda en Inglés
```bash
run.bat search

# Consulta: "portfolio diversification strategies"
# Idioma: en
# Fuente específica: 
# Resultados: 5
# Mostrar scores: n
```

#### Búsqueda en Documento Específico
```bash
run.bat search

# Consulta: "warren buffett investment principles"
# Idioma: en
# Fuente específica: warren_buffett.pdf
# Resultados: 3
# Mostrar scores: y
```

---

### Escenario 4: Mantenimiento Regular

#### Rutina Semanal de Mantenimiento
```bash
# 1. Verificar estado del sistema
run.bat check-space
run.bat check-index

# 2. Revisar logs por errores
run.bat log-errors

# 3. Limpiar caché si es necesario
run.bat clean

# 4. Verificar estadísticas
run.bat stats
```

#### Limpieza Mensual
```bash
# 1. Análisis completo de logs
run.bat log-stats

# 2. Evaluar documentos obsoletos
run.bat cleanup  # Solo si es necesario

# 3. Respaldo de configuración
copy .env .env.backup
```

---

### Escenario 5: Resolución de Problemas

#### Problema: Espacio Insuficiente
```bash
# 1. Verificar uso actual
run.bat check-space

# Salida problemática:
# Uso actual: 480.2 MB (93.8%)
# Espacio disponible: 31.8 MB (6.2%)
# **NO SEGURO PROCEDER**

# 2. Revisar distribución por categorías
run.bat stats

# 3. Limpiar categorías menos importantes
run.bat cleanup
# Seleccionar: "2. Limpieza por tipo de documento"
# Elegir categoría a eliminar

# 4. Verificar espacio liberado
run.bat check-space
```

#### Problema: Búsquedas Sin Resultados
```bash
# 1. Verificar índice vectorial
run.bat check-index

# 2. Verificar contenido de la base de datos
run.bat stats

# 3. Revisar logs por errores de ingesta
run.bat log-errors

# 4. Si es necesario, re-ejecutar ingesta
run.bat ingest
```

#### Problema: Errores de Conexión
```bash
# 1. Verificar conectividad básica
run.bat check-index

# 2. Revisar configuración
notepad .env

# 3. Verificar logs detallados
run.bat logs

# 4. Acceder al contenedor para debugging
run.bat shell
```

---

## Estructura de Archivos JSON Soportados

### Formato Básico
```json
{
  "title": "Análisis del Mercado S&P 500",
  "content": "El mercado de valores ha mostrado tendencias...",
  "source": "analisis_sp500.json",
  "language": "es",
  "category": "analisis_mercado",
  "author": "Juan Pérez",
  "date": "2025-09-29"
}
```

### Formato con Múltiples Secciones
```json
{
  "document_info": {
    "title": "Estrategias de Inversión Avanzadas",
    "author": "María González",
    "category": "estrategias"
  },
  "sections": [
    {
      "title": "Introducción",
      "content": "Las estrategias de inversión modernas..."
    },
    {
      "title": "Análisis Fundamental",
      "content": "El análisis fundamental se basa en..."
    }
  ]
}
```

---

## Mejores Prácticas

### Organización de Documentos
1. **Usar nombres descriptivos** para archivos y carpetas
2. **Agrupar por tema/categoría** en subdirectorios
3. **Mantener estructura consistente** en el tiempo
4. **Documentar fuentes** y fechas cuando sea posible

### Gestión de Espacio
1. **Verificar espacio ANTES** de ingestas grandes
2. **Procesar en lotes** si tienes muchos documentos
3. **Limpiar documentos obsoletos** regularmente
4. **Monitorear uso** semanalmente

### Búsquedas Efectivas
1. **Usar términos específicos** en lugar de genéricos
2. **Especificar idioma** para mejores resultados
3. **Filtrar por fuente** cuando busques algo específico
4. **Experimentar con diferentes formulaciones** de la consulta

### Mantenimiento del Sistema
1. **Revisar logs** regularmente
2. **Limpiar caché** si hay problemas de espacio
3. **Verificar índices** después de cambios importantes
4. **Mantener respaldos** de configuración

---

## Comandos de Emergencia

### Recuperación Rápida del Sistema
```bash
# 1. Verificar estado completo
run.bat check-index && run.bat check-space && run.bat stats

# 2. Si hay problemas críticos, limpiar todo
run.bat cleanup
# Escribir: "SI ELIMINAR"

# 3. Re-ejecutar ingesta completa
run.bat ingest

# 4. Verificar recuperación
run.bat check-index && run.bat stats
```

### Debugging Avanzado
```bash
# Acceder al contenedor
run.bat shell

# Dentro del contenedor:
python scripts/check_index.py --verbose
python scripts/check_space.py --detailed
python -c "from src.vectorstore.mongodb_vectorstore import MongoDBVectorStore; print('Test connection')"
```

### Limpieza de Caché Forzada
```bash
# Desde el shell del contenedor
run.bat shell

# Dentro del contenedor:
rm -rf embedding_cache/*
python -c "from src.embedding.openai_embeddings import OpenAIEmbeddingManager; OpenAIEmbeddingManager().clear_cache()"
```

---

**Última actualización:** 29 de septiembre de 2025
**Documento:** Guía de Uso Práctico v0.1.0