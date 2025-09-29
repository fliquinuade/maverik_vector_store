# Referencia Rápida - Maverik Vector Store

## 🚀 Comandos Esenciales

### Configuración Inicial
```bash
run.bat setup          # Crear archivo .env
run.bat build           # Construir imagen Docker
run.bat check-index     # Verificar configuración
run.bat check-space     # Verificar espacio disponible
```

### Operaciones Principales
```bash
run.bat ingest          # ⭐ Procesar documentos del directorio files/
run.bat search          # ⭐ Búsqueda interactiva
run.bat stats           # Ver estadísticas de la base de datos
```

### Mantenimiento
```bash
run.bat check-space     # ⚠️  VERIFICAR ANTES de ingesta
run.bat clean           # Limpiar caché de embeddings
run.bat cleanup         # 🚨 PELIGROSO - Limpiar toda la BD
run.bat logs            # Ver logs del sistema
```

---

## 📁 Gestión de Documentos

### ⚡ Flujo Rápido
1. **Copiar documentos** → `files/categoria/`
2. **Verificar espacio** → `run.bat check-space`
3. **Ejecutar ingesta** → `run.bat ingest`
4. **Buscar contenido** → `run.bat search`

### 📋 Formatos Soportados
- **PDF**: Extracción automática de texto
- **JSON**: Estructura con `content`, `title`, `source`

### 🏗️ Estructura Recomendada
```
files/
├── estrategias_inversion/
├── analisis_mercado/
├── educacion_financiera/
└── libros_referencia/
```

---

## 🔍 Búsquedas Efectivas

### Tipos de Consulta
```
"estrategias de inversión warren buffett"    # Específica
"análisis técnico mercados"                  # Temática  
"diversificación portfolio"                  # Conceptual
"riesgo financiero gestión"                  # Combinada
```

### Filtros Disponibles
- **Idioma**: `es` / `en`
- **Fuente**: nombre de archivo específico
- **Cantidad**: 1-20 resultados
- **Scores**: mostrar relevancia (recomendado)

---

## ⚠️ Alertas y Límites

### 🚨 Límites Críticos
- **MongoDB Atlas**: 512MB máximo (tier gratuito)
- **Estimación**: ~2,000-3,000 documentos típicos
- **Verificar SIEMPRE**: `run.bat check-space` antes de ingesta

### 📊 Estados de Espacio
- **Verde** (0-70%): ✅ Seguro proceder
- **Amarillo** (70-85%): ⚠️ Monitorear de cerca
- **Rojo** (85%+): 🚨 Limpiar antes de continuar

### 🔧 Mantenimiento Preventivo
- **Semanal**: `run.bat check-space` + `run.bat log-errors`
- **Mensual**: `run.bat clean` + análisis de documentos obsoletos

---

## 🆘 Resolución Rápida de Problemas

### Problema: No se puede conectar
```bash
run.bat check-index    # Verificar configuración
# → Revisar .env (MongoDB URI, OpenAI API key)
```

### Problema: Espacio insuficiente
```bash
run.bat check-space    # Ver uso actual
run.bat cleanup        # Limpiar si necesario
# → Opción 2: Limpieza por categoría
```

### Problema: Búsqueda sin resultados
```bash
run.bat stats          # Verificar contenido
run.bat check-index    # Verificar índice
# → Si está vacío: run.bat ingest
```

### Problema: Errores durante ingesta
```bash
run.bat log-errors     # Ver errores recientes
run.bat clean          # Limpiar caché
run.bat ingest         # Reintentar
```

---

## 📋 Checklist Pre-Ingesta

### ✅ Antes de Procesar Documentos
- [ ] Verificar espacio: `run.bat check-space`
- [ ] Organizar documentos en `files/categoria/`
- [ ] Nombres de archivo descriptivos
- [ ] Verificar formato (PDF/JSON válidos)
- [ ] Verificar conectividad: `run.bat check-index`

### ✅ Después de Ingesta
- [ ] Verificar estadísticas: `run.bat stats`
- [ ] Probar búsqueda: `run.bat search`
- [ ] Revisar logs: `run.bat log-errors`
- [ ] Verificar espacio restante: `run.bat check-space`

---

## 🎯 Configuración Típica `.env`

```env
# OpenAI (REQUERIDO)
OPENAI_API_KEY=sk-your-api-key-here

# MongoDB Atlas (REQUERIDO)
MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
MONGODB_DATABASE=maverik_vector_store
MONGODB_COLLECTION=documents

# Vector Search (OPCIONAL - usar defaults)
VECTOR_INDEX_NAME=vector_index
EMBEDDING_DIMENSIONS=1024

# Logging (OPCIONAL)
LOG_LEVEL=INFO
```

---

## 📞 Referencias Rápidas

### 📚 Documentación Completa
- `docs/DOCUMENTACION_PROYECTO.md` - Guía completa del sistema
- `docs/GUIA_USO_PRACTICO.md` - Ejemplos paso a paso
- `docs/TECHNICAL_CONSIDERATIONS.md` - Detalles técnicos

### 🔗 Enlaces Importantes
- **MongoDB Atlas**: https://cloud.mongodb.com/
- **OpenAI API**: https://platform.openai.com/api-keys
- **Docker**: https://docs.docker.com/get-docker/

### 💡 Consejos Rápidos
1. **Siempre verificar espacio** antes de ingestas grandes
2. **Usar nombres descriptivos** para archivos y carpetas
3. **Organizar por categorías** para facilitar búsquedas
4. **Limpiar caché** si hay problemas de rendimiento
5. **Monitorear logs** para detectar problemas temprano

---

**⏰ Última actualización:** 29 de septiembre de 2025  
**📋 Versión:** Referencia Rápida v0.1.0