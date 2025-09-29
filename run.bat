@echo off
REM Script de ayuda para Maverik Vector Store (Windows)
REM Uso: run.bat [comando]

setlocal enabledelayedexpansion

REM Verificar si Docker está instalado
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado
    exit /b 1
)

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose no está instalado
    exit /b 1
)

REM Función principal
if "%1"=="" goto :help
if "%1"=="help" goto :help
if "%1"=="--help" goto :help
if "%1"=="-h" goto :help
if "%1"=="setup" goto :setup
if "%1"=="build" goto :build
if "%1"=="ingest" goto :ingest
if "%1"=="search" goto :search
if "%1"=="stats" goto :stats
if "%1"=="test" goto :test
if "%1"=="clean" goto :clean
if "%1"=="cleanup" goto :cleanup
if "%1"=="check-space" goto :check-space
if "%1"=="check-index" goto :check-index
if "%1"=="logs" goto :logs
if "%1"=="log-stats" goto :log-stats
if "%1"=="log-errors" goto :log-errors
if "%1"=="shell" goto :shell

echo ❌ Comando desconocido: %1
echo.
goto :help

:help
echo 🚀 Maverik Vector Store - Script de Ayuda
echo.
echo Uso: run.bat [comando]
echo.
echo Comandos disponibles:
echo.
echo setup        - Configuración inicial (copia .env.example a .env)
echo build        - Construir imagen Docker
echo ingest       - Ejecutar ingesta completa de documentos
echo search       - Modo búsqueda interactiva
echo stats        - Mostrar estadísticas de la base de datos
echo test         - Ejecutar tests unitarios
echo clean        - Limpiar caché de embeddings
echo cleanup      - LIMPIAR base de datos completa (PELIGROSO)
echo check-space  - Verificar espacio disponible en MongoDB
echo check-index  - Verificar configuración del índice vectorial
echo logs         - Mostrar logs del contenedor
echo log-stats    - Estadísticas de archivos de log
echo log-errors   - Errores recientes en logs
echo shell        - Abrir shell en el contenedor
echo.
echo Ejemplos:
echo   run.bat setup
echo   run.bat ingest
echo   run.bat search
echo.
goto :end

:setup
echo 🔧 Configuración inicial
if not exist .env (
    copy .env.example .env
    echo ✅ Archivo .env creado desde .env.example
    echo ⚠️  Por favor edita .env con tus credenciales antes de continuar
) else (
    echo ⚠️  El archivo .env ya existe
)
goto :end

:build
echo 🏗️  Construyendo imagen Docker
docker-compose build
echo ✅ Imagen construida exitosamente
goto :end

:ingest
echo 📥 Ejecutando ingesta de documentos
if not exist .env (
    echo ❌ Archivo .env no encontrado. Ejecuta: run.bat setup
    exit /b 1
)
docker-compose up --build maverik-vector-store
echo ✅ Ingesta completada
goto :end

:search
echo 🔍 Iniciando modo búsqueda interactiva
if not exist .env (
    echo ❌ Archivo .env no encontrado. Ejecuta: run.bat setup
    exit /b 1
)
docker-compose --profile search up search-interactive
goto :end

:stats
echo 📊 Obteniendo estadísticas
docker-compose run --rm maverik-vector-store python scripts/ingest.py --stats
goto :end

:test
echo 🧪 Ejecutando tests
docker-compose run --rm maverik-vector-store python -m pytest tests/ -v
goto :end

:clean
echo 🧹 Limpiando caché de embeddings
docker-compose run --rm maverik-vector-store python -c "from src.embedding.openai_embeddings import OpenAIEmbeddingManager; OpenAIEmbeddingManager().clear_cache()"
echo ✅ Caché limpiado
goto :end

:logs
echo 📄 Mostrando logs
docker-compose logs -f maverik-vector-store
goto :end

:log-stats
echo 📊 Obteniendo estadísticas de logs
docker-compose run --rm maverik-vector-store python scripts/log_analyzer.py stats
goto :end

:log-errors
echo 🚨 Mostrando errores recientes
docker-compose run --rm maverik-vector-store python scripts/log_analyzer.py errors
goto :end

:shell
echo 🐚 Abriendo shell en contenedor
docker-compose run --rm -it maverik-vector-store /bin/bash
goto :end

:cleanup
echo ADVERTENCIA: Esta operación eliminará TODOS los documentos de la base de datos
echo Esta acción NO se puede deshacer
set /p confirm="¿Estás completamente seguro? Escribe 'SI ELIMINAR' para confirmar: "
if "%confirm%"=="SI ELIMINAR" (
    echo Ejecutando limpieza completa de la base de datos...
    docker-compose run --rm maverik-vector-store python scripts/cleanup_db.py
) else (
    echo Operación cancelada - No se eliminó nada
)
goto :end

:check-space
echo Verificando espacio disponible en MongoDB Atlas
docker-compose run --rm maverik-vector-store python scripts/check_space.py
goto :end

:check-index
echo Verificando configuración del índice vectorial
docker-compose run --rm maverik-vector-store python scripts/check_index.py
goto :end

:end
endlocal