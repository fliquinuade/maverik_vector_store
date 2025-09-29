"""
Script para analizar y monitorear logs del sistema.
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from src.config import get_settings

settings = get_settings()


class LogAnalyzer:
    """Analizador de logs del sistema."""
    
    def __init__(self):
        """Inicializa el analizador de logs."""
        self.log_dir = Path("logs")
        self.main_log = self.log_dir / "maverik_vector_store.log"
        self.error_log = self.log_dir / "errors.log"
        self.critical_log = self.log_dir / "critical_errors.log"
    
    def get_recent_errors(self, hours: int = 24) -> List[str]:
        """Obtiene errores recientes de las últimas N horas."""
        if not self.error_log.exists():
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = []
        
        try:
            with open(self.error_log, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            # Extraer timestamp del formato de log
                            timestamp_str = line.split(' - ')[0]
                            log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                            
                            if log_time >= cutoff_time:
                                recent_errors.append(line.strip())
                        except (ValueError, IndexError):
                            # Si no podemos parsear el timestamp, incluirlo por seguridad
                            recent_errors.append(line.strip())
            
        except Exception as e:
            print(f"Error leyendo log de errores: {e}")
            
        return recent_errors
    
    def get_critical_errors(self) -> List[Dict]:
        """Obtiene todos los errores críticos."""
        if not self.critical_log.exists():
            return []
        
        critical_errors = []
        
        try:
            with open(self.critical_log, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Dividir por separadores
                error_blocks = content.split('-' * 80)
                
                for block in error_blocks:
                    if block.strip():
                        lines = block.strip().split('\n')
                        if len(lines) >= 2:
                            timestamp_line = lines[0]
                            json_content = '\n'.join(lines[1:])
                            
                            try:
                                error_data = json.loads(json_content)
                                error_data['log_timestamp'] = timestamp_line
                                critical_errors.append(error_data)
                            except json.JSONDecodeError:
                                # Si no es JSON válido, guardarlo como texto
                                critical_errors.append({
                                    'log_timestamp': timestamp_line,
                                    'raw_content': json_content,
                                    'error_type': 'ParseError'
                                })
                                
        except Exception as e:
            print(f"Error leyendo log de errores críticos: {e}")
            
        return critical_errors
    
    def get_log_stats(self) -> Dict:
        """Obtiene estadísticas generales de los logs."""
        stats = {
            'main_log_exists': self.main_log.exists(),
            'error_log_exists': self.error_log.exists(),
            'critical_log_exists': self.critical_log.exists(),
            'main_log_size': 0,
            'error_log_size': 0,
            'critical_log_size': 0,
            'total_errors_24h': 0,
            'total_critical_errors': 0
        }
        
        if self.main_log.exists():
            stats['main_log_size'] = self.main_log.stat().st_size
            
        if self.error_log.exists():
            stats['error_log_size'] = self.error_log.stat().st_size
            
        if self.critical_log.exists():
            stats['critical_log_size'] = self.critical_log.stat().st_size
        
        # Contar errores
        stats['total_errors_24h'] = len(self.get_recent_errors(24))
        stats['total_critical_errors'] = len(self.get_critical_errors())
        
        return stats
    
    def tail_logs(self, lines: int = 50) -> None:
        """Muestra las últimas N líneas del log principal."""
        if not self.main_log.exists():
            print("Log principal no encontrado")
            return
        
        try:
            with open(self.main_log, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                
                print(f"📄 Últimas {len(recent_lines)} líneas del log principal:")
                print("-" * 80)
                
                for line in recent_lines:
                    print(line.rstrip())
                    
        except Exception as e:
            print(f"Error leyendo log principal: {e}")
    
    def search_logs(self, query: str, log_file: str = "main") -> List[str]:
        """Busca un término en los logs."""
        if log_file == "main":
            target_log = self.main_log
        elif log_file == "error":
            target_log = self.error_log
        elif log_file == "critical":
            target_log = self.critical_log
        else:
            print(f"Log desconocido: {log_file}")
            return []
        
        if not target_log.exists():
            print(f"Log {log_file} no encontrado")
            return []
        
        matches = []
        
        try:
            with open(target_log, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if query.lower() in line.lower():
                        matches.append(f"Línea {line_num}: {line.strip()}")
                        
        except Exception as e:
            print(f"Error buscando en log {log_file}: {e}")
            
        return matches
    
    def clean_old_logs(self, days: int = 30) -> None:
        """Limpia logs más antiguos que N días (función futura)."""
        print(f"🧹 Función de limpieza de logs (>{days} días) - Por implementar")
        # TODO: Implementar rotación de logs


def main():
    """Función principal del analizador de logs."""
    analyzer = LogAnalyzer()
    
    if len(sys.argv) < 2:
        print("📊 Maverik Vector Store - Analizador de Logs")
        print("")
        print("Uso: python scripts/log_analyzer.py [comando]")
        print("")
        print("Comandos:")
        print("  stats           - Estadísticas generales de logs")
        print("  errors [horas]  - Errores recientes (default: 24h)")
        print("  critical        - Todos los errores críticos")
        print("  tail [líneas]   - Últimas N líneas del log (default: 50)")
        print("  search <query>  - Buscar término en logs")
        print("  search-error <query> - Buscar en log de errores")
        print("")
        return
    
    command = sys.argv[1]
    
    if command == "stats":
        stats = analyzer.get_log_stats()
        print("📊 Estadísticas de Logs:")
        print(f"  Log principal: {'✅' if stats['main_log_exists'] else '❌'} ({stats['main_log_size']} bytes)")
        print(f"  Log de errores: {'✅' if stats['error_log_exists'] else '❌'} ({stats['error_log_size']} bytes)")
        print(f"  Log crítico: {'✅' if stats['critical_log_exists'] else '❌'} ({stats['critical_log_size']} bytes)")
        print(f"  Errores (24h): {stats['total_errors_24h']}")
        print(f"  Errores críticos: {stats['total_critical_errors']}")
    
    elif command == "errors":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        errors = analyzer.get_recent_errors(hours)
        
        print(f"🚨 Errores recientes ({hours}h):")
        if errors:
            for error in errors[-10:]:  # Últimos 10
                print(f"  {error}")
        else:
            print("  ✅ No hay errores recientes")
    
    elif command == "critical":
        critical_errors = analyzer.get_critical_errors()
        
        print("💥 Errores Críticos:")
        if critical_errors:
            for i, error in enumerate(critical_errors, 1):
                print(f"\n{i}. {error.get('log_timestamp', 'Sin timestamp')}")
                print(f"   Tipo: {error.get('error_type', 'Desconocido')}")
                print(f"   Mensaje: {error.get('error_message', 'Sin mensaje')}")
                if 'context' in error:
                    print(f"   Contexto: {error['context']}")
        else:
            print("  ✅ No hay errores críticos")
    
    elif command == "tail":
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        analyzer.tail_logs(lines)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Proporciona un término de búsqueda")
            return
        
        query = sys.argv[2]
        matches = analyzer.search_logs(query, "main")
        
        print(f"Búsqueda '{query}' en log principal:")
        if matches:
            for match in matches[-20:]:  # Últimos 20 matches
                print(f"  {match}")
        else:
            print("  No se encontraron coincidencias")
    
    elif command == "search-error":
        if len(sys.argv) < 3:
            print("Proporciona un término de búsqueda")
            return
        
        query = sys.argv[2]
        matches = analyzer.search_logs(query, "error")
        
        print(f"Búsqueda '{query}' en log de errores:")
        if matches:
            for match in matches[-20:]:  # Últimos 20 matches
                print(f"  {match}")
        else:
            print("  No se encontraron coincidencias")
    
    else:
        print(f"Comando desconocido: {command}")


if __name__ == "__main__":
    main()