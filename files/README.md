# Directorio de Documentos - files/

## 📁 Propósito

Este directorio es donde debes colocar **todos los documentos** que quieres procesar con Maverik Vector Store.

## 📋 Instrucciones de Uso

### 1. Organización Recomendada
```
files/
├── estrategias_inversion/
│   ├── warren_buffett_strategies.pdf
│   └── value_investing_guide.pdf
├── educacion_financiera/
│   ├── finanzas_personales_101.pdf
│   └── presupuesto_familiar.json
├── analisis_mercado/
│   └── sp500_analysis.json
└── libros_referencia/
    └── investment_analysis.pdf
```

### 2. Formatos Soportados
- **📄 PDF**: Extracción automática de texto completo
- **📝 JSON**: Estructura con campos `content`, `title`, `source`, etc.

### 3. Antes de Agregar Documentos
```bash
# Verificar espacio disponible (IMPORTANTE)
run.bat check-space
```

### 4. Después de Agregar Documentos
```bash
# Procesar nuevos documentos
run.bat ingest

# Verificar resultados
run.bat stats
```

## ⚠️ Notas Importantes

- **Límite de Espacio**: MongoDB Atlas tiene límite de 512MB (tier gratuito)
- **Estimación**: ~2,000-3,000 documentos típicos
- **Verificar SIEMPRE**: Espacio antes de agregar documentos grandes
- **Organizar**: Por categorías para facilitar búsquedas posteriores

## 🔒 Privacidad

Los documentos en este directorio **NO se suben al repositorio Git** por razones de privacidad y tamaño. Solo la estructura del directorio se mantiene en el repositorio.

## 📚 Documentación

Para más información, consulta:
- `docs/DOCUMENTACION_PROYECTO.md` - Guía completa
- `docs/GUIA_USO_PRACTICO.md` - Ejemplos paso a paso
- `docs/REFERENCIA_RAPIDA.md` - Comandos esenciales