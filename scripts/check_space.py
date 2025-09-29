"""
Script para verificar el espacio disponible en MongoDB Atlas.
"""
from pymongo import MongoClient
from src.config import get_settings
from src.utils.logger import get_logger

def check_available_space():
    """Verifica el espacio disponible en MongoDB Atlas."""
    settings = get_settings()
    logger = get_logger()
    
    try:
        print("Conectando a MongoDB Atlas...")
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.db_name]
        
        db_stats = db.command("dbStats")
        total_size_mb = db_stats.get('dataSize', 0) / 1024 / 1024
        
        try:
            coll_stats = db.command("collStats", settings.collection_name)
            doc_count = coll_stats.get('count', 0)
            coll_size_mb = coll_stats.get('size', 0) / 1024 / 1024
            avg_doc_size = coll_stats.get('avgObjSize', 0)
        except Exception:
            doc_count = 0
            coll_size_mb = 0
            avg_doc_size = 0
        
        print(f"\nEstado actual de MongoDB Atlas")
        print("=" * 50)
        print(f"Base de datos: {settings.db_name}")
        print(f"Colección: {settings.collection_name}")
        print(f"Espacio usado total: {total_size_mb:.2f} MB")
        print(f"Límite gratuito: 512 MB")
        print(f"Espacio disponible: {512 - total_size_mb:.2f} MB")
        print(f"Documentos en colección: {doc_count:,}")
        print(f"Tamaño de colección: {coll_size_mb:.2f} MB")
        
        if avg_doc_size > 0:
            print(f"Tamaño promedio por documento: {avg_doc_size / 1024:.2f} KB")
        
        available_space = 512 - total_size_mb
        usage_percentage = (total_size_mb / 512) * 100
        
        print(f"\nAnálisis de Uso")
        print(f"Porcentaje usado: {usage_percentage:.1f}%")
        
        if total_size_mb < 200:
            status = "EXCELENTE"
            recommendation = "Seguro proceder con ingesta completa"
            can_proceed = True
        elif total_size_mb < 350:
            status = "BUENO"
            recommendation = "Seguro proceder con ingesta, monitorear ocasionalmente"
            can_proceed = True
        elif total_size_mb < 450:
            status = "PRECAUCIÓN"
            recommendation = "Proceder con precaución, monitorear frecuentemente"
            can_proceed = True
        elif total_size_mb < 500:
            status = "CRÍTICO"
            recommendation = "Solo ingesta selectiva, considerar limpieza"
            can_proceed = False
        else:
            status = "PELIGROSO"
            recommendation = "NO proceder - Limpiar base de datos primero"
            can_proceed = False
        
        print(f"Estado: {status}")
        print(f"Recomendación: {recommendation}")
        
        if can_proceed and doc_count > 0:
            print(f"\nEstimaciones para Ingesta")
            
            if avg_doc_size > 0:
                remaining_docs = int((available_space * 1024 * 1024) / avg_doc_size)
                print(f"Documentos adicionales estimados: ~{remaining_docs:,}")
            
            if total_size_mb > 300:
                print(f"Sugerencias:")
                print(f"   • Usar CHUNK_SIZE=512 (en lugar de 1024)")
                print(f"   • Usar BATCH_SIZE=25 (en lugar de 100)")
                print(f"   • Monitorear cada 100 documentos procesados")
        
        if total_size_mb > 480:
            print(f"\nALERTA CRÍTICA")
            print(f"   • Quedan menos de 32 MB disponibles")
            print(f"   • Alto riesgo de exceder el límite")
            print(f"   • Considera limpieza inmediata: run.bat cleanup")
        
        client.close()
        
        logger.log_event(
            'space_check_complete',
            level='INFO',
            total_size_mb=total_size_mb,
            available_space_mb=available_space,
            usage_percentage=usage_percentage,
            can_proceed=can_proceed,
            document_count=doc_count
        )
        
        return can_proceed, total_size_mb, available_space
    except Exception as e:
        error_msg = f"Error verificando espacio: {e}"
        print(f"Error: {error_msg}")
        logger.log_critical_error(
            error_type="SpaceCheckError",
            error_message=error_msg,
            context={
                "operation": "space_verification",
                "db_name": settings.db_name,
                "collection_name": settings.collection_name
            }
        )
        return False, 0, 0

def monitor_during_ingestion():
    """Monitorea el espacio durante la ingesta."""
    can_proceed, current_size, available = check_available_space()
    
    if not can_proceed:
        print(f"\nDETENER INGESTA INMEDIATAMENTE")
        print(f"Espacio insuficiente para continuar")
        print(f"Ejecutar limpieza: run.bat cleanup")
        return False
    
    if current_size > 480:
        print(f"\nADVERTENCIA: Acercándose al límite")
        print(f"Quedan {available:.1f} MB disponibles")
        return True
    
    return True

def get_collection_breakdown():
    """Obtiene un desglose detallado del uso de espacio por tipo de documento."""
    settings = get_settings()
    
    try:
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.db_name]
        collection = db[settings.collection_name]
        
        print(f"\n**Desglose por Tipo de Documento**")
        print("=" * 50)
        
        # Agrupar por fuente/tipo
        pipeline = [
            {
                "$group": {
                    "_id": "$metadata.source",
                    "count": {"$sum": 1},
                    "avgSize": {"$avg": {"$bsonSize": "$$ROOT"}}
                }
            },
            {"$sort": {"count": -1}}
        ]
        
        results = list(collection.aggregate(pipeline))
        
        total_docs = 0
        for result in results:
            source = result["_id"] or "Sin fuente"
            count = result["count"]
            avg_size_kb = result["avgSize"] / 1024
            total_size_mb = (count * result["avgSize"]) / 1024 / 1024
            
            print(f"📁 {source}:")
            print(f"   Documentos: {count:,}")
            print(f"   📏 Tamaño promedio: {avg_size_kb:.2f} KB")
            print(f"   📦 Tamaño total: {total_size_mb:.2f} MB")
            
            total_docs += count
        
        print(f"\nTotal de documentos: {total_docs:,}")
        
        client.close()
        
    except Exception as e:
        print(f"Error obteniendo desglose: {e}")

def main():
    """Función principal del script de verificación."""
    print("**Maverik Vector Store - Verificación de Espacio**")
    print("=" * 60)
    
    can_proceed, size_mb, available_mb = check_available_space()
    
    if size_mb > 0:
        print(f"\n" + "=" * 60)
        get_collection_breakdown()
    
    print(f"\n" + "=" * 60)
    print(f"📋 **Resumen Final**")
    
    if can_proceed:
        print(f"**SEGURO PROCEDER** con la ingesta")
        print(f"Ejecutar: run.bat ingest")
    else:
        print(f"**NO SEGURO PROCEDER**")
        print(f"🧹 Ejecutar primero: run.bat cleanup")
    
    print(f"Para monitoreo continuo: run.bat check-space")

if __name__ == "__main__":
    main()