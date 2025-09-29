"""
Script para limpiar la base de datos MongoDB Atlas.
"""
from pymongo import MongoClient
from src.config import get_settings
from src.utils.logger import get_logger

def cleanup_database():
    """Limpia completamente la base de datos."""
    settings = get_settings()
    logger = get_logger()
    
    try:
        print("Conectando a MongoDB Atlas...")
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.db_name]
        collection = db[settings.collection_name]
        
        try:
            stats_before = db.command("collStats", settings.collection_name)
            doc_count = stats_before.get('count', 0)
            size_mb = stats_before.get('size', 0) / 1024 / 1024
            print(f"Estado actual:")
            print(f"   Documentos: {doc_count:,}")
            print(f"   Tamaño: {size_mb:.2f} MB")
            
            db_stats = db.command("dbStats")
            total_size_mb = db_stats.get('dataSize', 0) / 1024 / 1024
            print(f"   Tamaño total BD: {total_size_mb:.2f} MB / 512 MB")
            
        except Exception as e:
            print(f"No se pudieron obtener estadísticas: {e}")
            print("La colección podría no existir o estar vacía")
        
        print("\nEsta operación eliminará TODOS los documentos de la colección:")
        print(f"   Base de datos: {settings.db_name}")
        print(f"   Colección: {settings.collection_name}")
        confirm = input("\n¿Estás seguro de que quieres continuar? (y/N): ")
        
        if confirm.lower() != 'y':
            print("Operación cancelada por el usuario")
            logger.log_event('cleanup_cancelled', level='INFO')
            return False
        
        print("Eliminando documentos...")
        result = collection.delete_many({})
        print(f"Documentos eliminados: {result.deleted_count:,}")
        
        # Eliminar la colección completamente (libera más espacio)
        print("🗑️  Eliminando colección completamente...")
        collection.drop()
        print("Colección eliminada")
        
        # Verificar espacio liberado
        try:
            db_stats_after = db.command("dbStats")
            total_size_after_mb = db_stats_after.get('dataSize', 0) / 1024 / 1024
            print(f"Estado después de la limpieza:")
            print(f"  Tamaño total BD: {total_size_after_mb:.2f} MB / 512 MB")
            print(f"  Espacio disponible: {512 - total_size_after_mb:.2f} MB")
            
            if total_size_after_mb < 450:
                print("EXCELENTE - Espacio suficiente para ingesta completa")
            elif total_size_after_mb < 500:
                print("PRECAUCIÓN - Espacio limitado, monitorear durante ingesta")
            else:
                print("PROBLEMA - Aún queda poco espacio disponible")
                
        except Exception as e:
            print(f"No se pudieron obtener estadísticas finales: {e}")
        
        client.close()
        
        logger.log_event(
            'database_cleanup_complete',
            level='INFO',
            documents_deleted=result.deleted_count,
            operation='full_cleanup'
        )
        
        print("\nLimpieza completada exitosamente")
        return True
        
    except Exception as e:
        error_msg = f"Error durante la limpieza: {e}"
        print(f"{error_msg}")
        logger.log_critical_error(
            error_type="CleanupError",
            error_message=error_msg,
            context={
                "operation": "database_cleanup",
                "db_name": settings.db_name,
                "collection_name": settings.collection_name
            }
        )
        return False

def cleanup_specific_documents():
    """Limpia solo documentos específicos (alternativa más conservadora)."""
    settings = get_settings()
    logger = get_logger()
    
    try:
        print("Conectando a MongoDB Atlas...")
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.db_name]
        collection = db[settings.collection_name]
        
        # Mostrar opciones de limpieza selectiva
        print("\nOpciones de limpieza selectiva:")
        print("1. Eliminar solo documentos PDF (mantener FAQ)")
        print("2. Eliminar solo FAQ (mantener PDFs)")
        print("3. Eliminar documentos por idioma (es/en)")
        print("4. Cancelar")
        
        choice = input("\nSelecciona una opción (1-4): ")
        
        if choice == "1":
            # Eliminar solo PDFs
            filter_query = {"metadata.source": {"$regex": "\.pdf$", "$options": "i"}}
            description = "documentos PDF"
        elif choice == "2":
            # Eliminar solo FAQ
            filter_query = {"metadata.source": "Warren Buffett FAQ"}
            description = "documentos FAQ"
        elif choice == "3":
            language = input("¿Qué idioma eliminar? (es/en): ")
            if language in ["es", "en"]:
                filter_query = {"metadata.idioma": language}
                description = f"documentos en {language}"
            else:
                print("Idioma no válido")
                return False
        elif choice == "4":
            print("Operación cancelada")
            return False
        else:
            print("Opción no válida")
            return False
        
        # Contar documentos que serán eliminados
        count_to_delete = collection.count_documents(filter_query)
        print(f"\nSe eliminarán {count_to_delete:,} {description}")
        
        confirm = input("¿Continuar? (y/N): ")
        if confirm.lower() != 'y':
            print("Operación cancelada")
            return False
        
        # Ejecutar eliminación selectiva
        result = collection.delete_many(filter_query)
        print(f"Eliminados {result.deleted_count:,} {description}")
        
        client.close()
        
        logger.log_event(
            'selective_cleanup_complete',
            level='INFO',
            documents_deleted=result.deleted_count,
            filter_applied=str(filter_query)
        )
        
        return True
        
    except Exception as e:
        error_msg = f"Error durante la limpieza selectiva: {e}"
        print(f"{error_msg}")
        logger.log_critical_error(
            error_type="SelectiveCleanupError",
            error_message=error_msg,
            context={"operation": "selective_cleanup"}
        )
        return False

def main():
    """Función principal del script de limpieza."""
    print("**Maverik Vector Store - Limpieza de Base de Datos**")
    print("=" * 60)
    
    print("\n📋 Opciones disponibles:")
    print("1. Limpieza completa (eliminar TODO)")
    print("2. Limpieza selectiva (eliminar parte)")
    print("3. Cancelar")
    
    choice = input("\nSelecciona una opción (1-3): ")
    
    if choice == "1":
        success = cleanup_database()
    elif choice == "2":
        success = cleanup_specific_documents()
    elif choice == "3":
        print("Operación cancelada")
        return
    else:
        print("Opción no válida")
        return
    
    if success:
        print("\nLimpieza completada exitosamente")
        print("Ahora puedes ejecutar la ingesta nuevamente con:")
        print("   run.bat ingest")
    else:
        print("\n**Error en la limpieza**")
        print("Revisa los logs para más detalles:")
        print("   run.bat log-errors")

if __name__ == "__main__":
    main()