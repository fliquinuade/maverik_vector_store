"""
Script para realizar búsquedas en el vector store.
"""
import sys
from typing import Optional

from src.config import get_settings
from src.embedding.openai_embeddings import OpenAIEmbeddingManager
from src.utils.logger import get_logger
from src.vectorstore.mongodb_vectorstore import MongoDBVectorStore

settings = get_settings()
logger = get_logger()


class SearchEngine:
    """Motor de búsqueda para el vector store."""
    
    def __init__(self):
        """Inicializa el motor de búsqueda."""
        self.embedding_manager = OpenAIEmbeddingManager()
        self.vector_store = MongoDBVectorStore(self.embedding_manager)
        
        logger.log_event('search_engine_initialized')
    
    def search(
        self, 
        query: str, 
        k: int = 5, 
        language: Optional[str] = None,
        source: Optional[str] = None,
        with_scores: bool = False
    ) -> None:
        """Realiza una búsqueda y muestra los resultados."""
        try:
            # Construir filtros
            filters = {}
            if language:
                filters['metadata.idioma'] = language
            if source:
                filters['metadata.source'] = {"$regex": source, "$options": "i"}
            
            # Realizar búsqueda
            if with_scores:
                results = self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k,
                    filter_dict=filters if filters else None
                )
            else:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter_dict=filters if filters else None
                )
            
            # Mostrar resultados
            self._display_results(query, results, with_scores)
            
        except Exception as e:
            logger.log_event(
                'search_error',
                level='ERROR',
                query=query,
                error=str(e)
            )
            print(f"Error en la búsqueda: {e}")
    
    def _display_results(self, query: str, results, with_scores: bool = False) -> None:
        """Muestra los resultados de búsqueda formateados."""
        print(f"\nResultados para: '{query}'")
        print("=" * 80)
        
        if not results:
            print("No se encontraron resultados")
            return
        
        for i, result in enumerate(results, 1):
            if with_scores:
                doc, score = result
                print(f"\nResultado {i} (Score: {score:.4f}):")
            else:
                doc = result
                print(f"\nResultado {i}:")
            
            print(f"Contenido:")
            content = doc.page_content[:300]
            if len(doc.page_content) > 300:
                content += "..."
            print(f"   {content}")
            
            print(f"Metadatos:")
            for key, value in doc.metadata.items():
                print(f"   {key}: {value}")
            
            print("-" * 40)
    
    def interactive_search(self) -> None:
        """Modo de búsqueda interactiva."""
        print("Modo de búsqueda interactiva")
        print("Escribe 'exit' para salir")
        print("Comandos especiales:")
        print("  --lang=es|en    : Filtrar por idioma")
        print("  --source=texto  : Filtrar por fuente")
        print("  --k=número      : Número de resultados")
        print("  --scores        : Mostrar scores")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nConsulta: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'salir']:
                    print("Hasta luego!")
                    break
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                query_parts = []
                k = 5
                language = None
                source = None
                with_scores = False
                
                for part in parts:
                    if part.startswith('--lang='):
                        language = part.split('=')[1]
                    elif part.startswith('--source='):
                        source = part.split('=')[1]
                    elif part.startswith('--k='):
                        k = int(part.split('=')[1])
                    elif part == '--scores':
                        with_scores = True
                    else:
                        query_parts.append(part)
                
                query = ' '.join(query_parts)
                
                if query:
                    self.search(query, k, language, source, with_scores)
                else:
                    print("Por favor ingresa una consulta válida")
                    
            except KeyboardInterrupt:
                print("\nHasta luego!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Función principal."""
    try:
        engine = SearchEngine()
        
        # Verificar conexión
        if not engine.vector_store.test_connection():
            print("No se pudo conectar a MongoDB")
            sys.exit(1)
        
        if len(sys.argv) == 1:
            # Modo interactivo
            engine.interactive_search()
        else:
            # Búsqueda directa desde argumentos
            query = ' '.join(sys.argv[1:])
            
            # Parsear argumentos especiales
            if '--help' in sys.argv or '-h' in sys.argv:
                print("Uso: python search.py [consulta]")
                print("     python search.py  (modo interactivo)")
                print("\nEjemplos:")
                print("  python search.py 'estrategias de inversión'")
                print("  python search.py 'warren buffett' --lang=en --k=3")
                return
            
            # Extraer parámetros
            k = 5
            language = None
            source = None
            with_scores = False
            
            query_parts = []
            for arg in sys.argv[1:]:
                if arg.startswith('--lang='):
                    language = arg.split('=')[1]
                elif arg.startswith('--source='):
                    source = arg.split('=')[1]
                elif arg.startswith('--k='):
                    k = int(arg.split('=')[1])
                elif arg == '--scores':
                    with_scores = True
                else:
                    query_parts.append(arg)
            
            query = ' '.join(query_parts)
            
            if query:
                engine.search(query, k, language, source, with_scores)
            else:
                print("Por favor proporciona una consulta")
                
    except KeyboardInterrupt:
        print("\n👋 Proceso interrumpido")
        sys.exit(1)
    except Exception as e:
        logger.log_event('search_main_error', level='ERROR', error=str(e))
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()