#!/bin/bash

# Script de ayuda para Maverik Vector Store
# Uso: ./run.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}🚀 Maverik Vector Store - Script de Ayuda${NC}"
    echo ""
    echo "Uso: ./run.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo ""
    echo -e "${GREEN}setup${NC}        - Configuración inicial (copia .env.example a .env)"
    echo -e "${GREEN}build${NC}        - Construir imagen Docker"
    echo -e "${GREEN}ingest${NC}       - Ejecutar ingesta completa de documentos"
    echo -e "${GREEN}search${NC}       - Modo búsqueda interactiva"
    echo -e "${GREEN}stats${NC}        - Mostrar estadísticas de la base de datos"
    echo -e "${GREEN}test${NC}         - Ejecutar tests unitarios"
    echo -e "${GREEN}clean${NC}        - Limpiar caché de embeddings"
    echo -e "${GREEN}cleanup${NC}      - LIMPIAR base de datos completa (PELIGROSO)"
    echo -e "${GREEN}check-space${NC}  - Verificar espacio disponible en MongoDB"
    echo -e "${GREEN}check-index${NC}  - Verificar configuración del índice vectorial"
    echo -e "${GREEN}logs${NC}         - Mostrar logs del contenedor"
    echo -e "${GREEN}log-stats${NC}    - Estadísticas de archivos de log"
    echo -e "${GREEN}log-errors${NC}   - Errores recientes en logs"
    echo -e "${GREEN}shell${NC}        - Abrir shell en el contenedor"
    echo ""
    echo "Ejemplos:"
    echo "  ./run.sh setup"
    echo "  ./run.sh ingest"
    echo "  ./run.sh search"
    echo ""
}

# Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose no está instalado${NC}"
        exit 1
    fi
}

# Configuración inicial
setup() {
    echo -e "${BLUE}🔧 Configuración inicial${NC}"
    
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Archivo .env creado desde .env.example${NC}"
        echo -e "${YELLOW}⚠️  Por favor edita .env con tus credenciales antes de continuar${NC}"
    else
        echo -e "${YELLOW}⚠️  El archivo .env ya existe${NC}"
    fi
}

# Construir imagen
build() {
    echo -e "${BLUE}🏗️  Construyendo imagen Docker${NC}"
    docker-compose build
    echo -e "${GREEN}✅ Imagen construida exitosamente${NC}"
}

# Ejecutar ingesta
ingest() {
    echo -e "${BLUE}📥 Ejecutando ingesta de documentos${NC}"
    
    if [ ! -f .env ]; then
        echo -e "${RED}❌ Archivo .env no encontrado. Ejecuta: ./run.sh setup${NC}"
        exit 1
    fi
    
    docker-compose up --build maverik-vector-store
    echo -e "${GREEN}✅ Ingesta completada${NC}"
}

# Búsqueda interactiva
search() {
    echo -e "${BLUE}🔍 Iniciando modo búsqueda interactiva${NC}"
    
    if [ ! -f .env ]; then
        echo -e "${RED}❌ Archivo .env no encontrado. Ejecuta: ./run.sh setup${NC}"
        exit 1
    fi
    
    docker-compose --profile search up search-interactive
}

# Mostrar estadísticas
stats() {
    echo -e "${BLUE}📊 Obteniendo estadísticas${NC}"
    docker-compose run --rm maverik-vector-store python scripts/ingest.py --stats
}

# Ejecutar tests
run_tests() {
    echo -e "${BLUE}🧪 Ejecutando tests${NC}"
    docker-compose run --rm maverik-vector-store python -m pytest tests/ -v
}

# Limpiar caché
clean() {
    echo -e "${BLUE}🧹 Limpiando caché de embeddings${NC}"
    docker-compose run --rm maverik-vector-store python -c "from src.embedding.openai_embeddings import OpenAIEmbeddingManager; OpenAIEmbeddingManager().clear_cache()"
    echo -e "${GREEN}✅ Caché limpiado${NC}"
}

# Mostrar logs
show_logs() {
    echo -e "${BLUE}📄 Mostrando logs${NC}"
    docker-compose logs -f maverik-vector-store
}

# Estadísticas de logs
log_stats() {
    echo -e "${BLUE}📊 Obteniendo estadísticas de logs${NC}"
    docker-compose run --rm maverik-vector-store python scripts/log_analyzer.py stats
}

# Errores recientes
log_errors() {
    echo -e "${BLUE}🚨 Mostrando errores recientes${NC}"
    docker-compose run --rm maverik-vector-store python scripts/log_analyzer.py errors
}

# Abrir shell
open_shell() {
    echo -e "${BLUE}🐚 Abriendo shell en contenedor${NC}"
    docker-compose run --rm -it maverik-vector-store /bin/bash
}

# Limpiar base de datos
cleanup() {
    echo -e "${RED}ADVERTENCIA: Esta operación eliminará TODOS los documentos de la base de datos${NC}"
    echo -e "${YELLOW}Esta acción NO se puede deshacer${NC}"
    read -p "¿Estás completamente seguro? Escribe 'SI ELIMINAR' para confirmar: " confirm
    
    if [ "$confirm" = "SI ELIMINAR" ]; then
        echo -e "${BLUE}Ejecutando limpieza completa de la base de datos...${NC}"
        docker-compose run --rm maverik-vector-store python scripts/cleanup_db.py
    else
        echo -e "${RED}Operación cancelada - No se eliminó nada${NC}"
    fi
}

check_space() {
    echo -e "${BLUE}Verificando espacio disponible en MongoDB Atlas${NC}"
    docker-compose run --rm maverik-vector-store python scripts/check_space.py
}

check_index() {
    echo -e "${BLUE}Verificando configuración del índice vectorial${NC}"
    docker-compose run --rm maverik-vector-store python scripts/check_index.py
}

# Función principal
main() {
    check_docker
    
    case "${1:-help}" in
        "help"|"--help"|"-h")
            show_help
            ;;
        "setup")
            setup
            ;;
        "build")
            build
            ;;
        "ingest")
            ingest
            ;;
        "search")
            search
            ;;
        "stats")
            stats
            ;;
        "test")
            run_tests
            ;;
        "clean")
            clean
            ;;
        "cleanup")
            cleanup
            ;;
        "check-space")
            check_space
            ;;
        "check-index")
            check_index
            ;;
        "logs")
            show_logs
            ;;
        "log-stats")
            log_stats
            ;;
        "log-errors")
            log_errors
            ;;
        "shell")
            open_shell
            ;;
        *)
            echo -e "${RED}❌ Comando desconocido: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"