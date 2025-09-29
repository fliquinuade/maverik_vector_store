"""
Script para verificar la configuración del índice vectorial en MongoDB Atlas.
"""
from pymongo import MongoClient
from src.config import get_settings
from src.utils.logger import get_logger

def check_vector_index():
    """Verifica la configuración del índice vectorial."""
    settings = get_settings()
    logger = get_logger()
    
    try:
        print("Conectando a MongoDB Atlas...")
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.db_name]
        collection = db[settings.collection_name]
        
        print(f"\nVerificación del Índice Vectorial")
        print("=" * 50)
        print(f"Base de datos: {settings.db_name}")
        print(f"Colección: {settings.collection_name}")
        print(f"Índice esperado: {settings.atlas_vector_search_index_name}")
        
        doc_count = collection.count_documents({})
        print(f"Documentos en colección: {doc_count:,}")
        
        if doc_count == 0:
            print("No hay documentos en la colección")
            print("Ejecutar primero: run.bat ingest")
            logger.log_event('index_check_failed', reason='no_documents')
            return False
        
        sample_doc = collection.find_one()
        if sample_doc:
            print(f"\nEstructura del Documento:")
            print(f"   ID presente: SI")
            
            text_field = sample_doc.get('text', '')
            if text_field:
                print(f"   Campo texto: SI ({len(str(text_field))} caracteres)")
                print(f"      Muestra: \"{str(text_field)[:100]}...\"")
            else:
                print(f"   Campo texto: NO encontrado")
            
            embedding_field = sample_doc.get('embedding')
            if embedding_field and isinstance(embedding_field, list):
                embedding_dims = len(embedding_field)
                print(f"   Embedding: SI ({embedding_dims} dimensiones)")
                
                if embedding_dims == settings.embedding_dimensions:
                    print(f"      Dimensiones correctas ({settings.embedding_dimensions})")
                else:
                    print(f"      Dimensiones diferentes: esperado {settings.embedding_dimensions}, encontrado {embedding_dims}")
            else:
                print(f"   Embedding: NO encontrado o formato incorrecto")
            
            metadata = sample_doc.get('metadata', {})
            if metadata:
                print(f"   Metadata: SI")
                for key, value in metadata.items():
                    print(f"      - {key}: {value}")
            else:
                print(f"   Metadata: NO encontrado")
        
        indexes = list(collection.list_indexes())
        print(f"\nÍndices de MongoDB ({len(indexes)}):")
        for idx in indexes:
            idx_name = idx.get('name', 'Sin nombre')
            idx_key = idx.get('key', {})
            print(f"   - {idx_name}: {dict(idx_key)}")
        
        print(f"\nPrueba de Búsqueda de Texto:")
        
        test_terms = ['warren', 'investment', 'inversión', 'finanzas', 'buffett']
        found_terms = []
        
        for term in test_terms:
            text_results = collection.find(
                {"text": {"$regex": term, "$options": "i"}}
            ).limit(1)
            
            if list(text_results):
                found_terms.append(term)
        
        if found_terms:
            print(f"   Términos encontrados: {', '.join(found_terms)}")
            print(f"   Los documentos contienen texto relevante")
        else:
            print(f"   No se encontraron términos comunes de prueba")
        
        print(f"\nConfiguración Vector Store:")
        print(f"   Modelo embedding: {settings.embedding_model}")
        print(f"   Dimensiones: {settings.embedding_dimensions}")
        print(f"   Índice vectorial: {settings.atlas_vector_search_index_name}")
        
        print(f"\nEstado y Recomendaciones:")
        
        if doc_count > 0 and sample_doc.get('embedding'):
            print(f"   ESTADO: LISTO PARA BÚSQUEDAS")
            print(f"   Los documentos tienen embeddings")
            print(f"   El índice vectorial debe estar configurado en Atlas")
            print(f"   Probar búsqueda: run.bat search")
            
            logger.log_event(
                'index_check_success',
                document_count=doc_count,
                embedding_dimensions=len(sample_doc.get('embedding', [])),
                has_text=bool(sample_doc.get('text')),
                has_metadata=bool(sample_doc.get('metadata'))
            )
            
        elif doc_count > 0 and not sample_doc.get('embedding'):
            print(f"   ESTADO: PROBLEMA CON EMBEDDINGS")
            print(f"   Los documentos NO tienen embeddings")
            print(f"   Ejecutar nueva ingesta: run.bat ingest")
            
            logger.log_event(
                'index_check_warning',
                reason='missing_embeddings',
                document_count=doc_count
            )
            
        else:
            print(f"   ESTADO: SIN DATOS")
            print(f"   Ejecutar ingesta: run.bat ingest")
            
            logger.log_event(
                'index_check_failed',
                reason='no_data'
            )
        
        print(f"\nInformación del Índice Atlas Search:")
        print(f"   Configurable en: MongoDB Atlas Dashboard > Search")
        print(f"   Tipo: Vector Search")
        print(f"   Campo: embedding")
        print(f"   Dimensiones: {settings.embedding_dimensions}")
        print(f"   Similaridad: cosine")
        
        client.close()
        return True
    except Exception as e:
        error_msg = f"Error verificando índice: {e}"
        print(f"Error: {error_msg}")
        logger.log_critical_error(
            error_type="IndexCheckError",
            error_message=error_msg,
            context={
                "operation": "check_vector_index",
                "db_name": settings.db_name,
                "collection_name": settings.collection_name
            }
        )
        return False

def test_vector_search():
    """Prueba básica de búsqueda vectorial."""
    try:
        from src.vectorstore.mongodb_vectorstore import MongoDBVectorStore
        from src.embedding.openai_embeddings import OpenAIEmbeddingManager
        
        print(f"\nPrueba de Búsqueda Vectorial:")
        
        embedding_manager = OpenAIEmbeddingManager()
        vector_store = MongoDBVectorStore(embedding_manager)
        
        if vector_store.test_connection():
            print(f"   Conexión exitosa al vector store")
            
            test_query = "investment strategy"
            print(f"   Probando consulta: '{test_query}'")
            
            results = vector_store.similarity_search(test_query, k=2)
            
            if results:
                print(f"   Búsqueda exitosa: {len(results)} resultados")
                for i, result in enumerate(results, 1):
                    print(f"      {i}. {result.page_content[:80]}...")
            else:
                print(f"   Búsqueda sin resultados")
                print(f"   Verificar configuración del índice en Atlas")
            
            vector_store.close_connection()
            return len(results) > 0
        else:
            print(f"   Error de conexión al vector store")
            return False
            
    except ImportError as e:
        print(f"   No se puede importar vector store: {e}")
        return False
    except Exception as e:
        print(f"   Error en prueba de búsqueda: {e}")
        return False

def main():
    """Función principal del script de verificación."""
    print("Maverik Vector Store - Verificación de Índice Vectorial")
    print("=" * 70)
    
    basic_check = check_vector_index()
    
    if basic_check:
        print(f"\n" + "=" * 70)
        
        search_test = test_vector_search()
        
        print(f"\n" + "=" * 70)
        print(f"Resumen Final:")
        
        if search_test:
            print(f"SISTEMA FUNCIONANDO CORRECTAMENTE")
            print(f"   Búsquedas vectoriales operativas")
            print(f"   Listo para usar: run.bat search")
        else:
            print(f"SISTEMA PARCIALMENTE CONFIGURADO")
            print(f"   Datos presentes pero búsquedas no funcionan")
            print(f"   Verificar índice vectorial en MongoDB Atlas")
            print(f"   Consultar documentación de Atlas Search")
    else:
        print(f"\nVERIFICACIÓN FALLIDA")
        print(f"   Revisar configuración y conexión")
        print(f"   Ejecutar ingesta si es necesario")

if __name__ == "__main__":
    main()