#!/usr/bin/env python3
"""
Script para automatizar la actualización de documentos de referencia.
Identifica discrepancias entre el estado actual del proyecto y la documentación.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))
os.chdir(backend_path)

try:
    from app.database import get_db
    from sqlalchemy import text
    from app.models import Usuario, Negocio, Producto, Insumo
except ImportError as e:
    print(f"⚠️  No se pudo importar modelos del backend: {e}")
    print("   El script funcionará en modo limitado (solo análisis de archivos)")

class DocumentacionUpdater:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.current_state = {}
        self.documentation_state = {}
        self.discrepancies = []
        self.updates_made = []
        
    def analyze_current_state(self) -> Dict[str, Any]:
        """Analiza el estado actual del proyecto"""
        print("🔍 Analizando estado actual del proyecto...")
        
        state = {
            'timestamp': datetime.now().isoformat(),
            'files': {},
            'database': {},
            'endpoints': {},
            'functionality': {}
        }
        
        # Analizar archivos del proyecto
        state['files'] = self._analyze_project_files()
        
        # Analizar base de datos
        state['database'] = self._analyze_database()
        
        # Analizar endpoints
        state['endpoints'] = self._analyze_endpoints()
        
        # Analizar funcionalidades
        state['functionality'] = self._analyze_functionality()
        
        self.current_state = state
        return state
    
    def _analyze_project_files(self) -> Dict[str, Any]:
        """Analiza la estructura de archivos del proyecto"""
        files_info = {
            'backend_files': 0,
            'frontend_files': 0,
            'debugging_files': 0,
            'documentation_files': 0,
            'total_files': 0,
            'file_types': {},
            'recent_changes': []
        }
        
        # Contar archivos por directorio
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            relative_path = root_path.relative_to(self.project_root)
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = root_path / file
                file_ext = file_path.suffix.lower()
                
                files_info['total_files'] += 1
                files_info['file_types'][file_ext] = files_info['file_types'].get(file_ext, 0) + 1
                
                # Categorizar por directorio
                if 'backend' in str(relative_path):
                    files_info['backend_files'] += 1
                elif 'frontend' in str(relative_path):
                    files_info['frontend_files'] += 1
                elif 'debugging' in str(relative_path):
                    files_info['debugging_files'] += 1
                elif 'Documentación' in str(relative_path) or 'Documentacion' in str(relative_path):
                    files_info['documentation_files'] += 1
                
                # Verificar cambios recientes (últimas 24 horas)
                try:
                    mtime = file_path.stat().st_mtime
                    if datetime.now().timestamp() - mtime < 86400:  # 24 horas
                        files_info['recent_changes'].append(str(relative_path / file))
                except:
                    pass
        
        return files_info
    
    def _analyze_database(self) -> Dict[str, Any]:
        """Analiza el estado de la base de datos"""
        db_info = {
            'tables': {},
            'records': {},
            'enums': {},
            'status': 'unknown'
        }
        
        try:
            db = next(get_db())
            
            # Analizar tablas principales
            tables = ['usuarios', 'negocios', 'productos', 'insumos', 'producto_insumo']
            for table in tables:
                try:
                    # Contar registros
                    result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    
                    # Obtener estructura
                    result = db.execute(text(f"""
                        SELECT column_name, data_type, is_nullable 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}' 
                        ORDER BY ordinal_position
                    """))
                    columns = [dict(row) for row in result.fetchall()]
                    
                    db_info['tables'][table] = {
                        'record_count': count,
                        'columns': columns
                    }
                    db_info['records'][table] = count
                    
                except Exception as e:
                    print(f"⚠️  Error analizando tabla {table}: {e}")
            
            # Analizar enums
            try:
                result = db.execute(text("SELECT DISTINCT tipo_negocio FROM negocios"))
                db_info['enums']['business_type'] = [row[0] for row in result.fetchall()]
                
                result = db.execute(text("SELECT DISTINCT tipo_producto FROM productos"))
                db_info['enums']['product_type'] = [row[0] for row in result.fetchall()]
                
                result = db.execute(text("SELECT DISTINCT tipo_tier FROM usuarios"))
                db_info['enums']['user_tier'] = [row[0] for row in result.fetchall()]
                
            except Exception as e:
                print(f"⚠️  Error analizando enums: {e}")
            
            db_info['status'] = 'connected'
            db.close()
            
        except Exception as e:
            print(f"⚠️  No se pudo conectar a la base de datos: {e}")
            db_info['status'] = 'disconnected'
        
        return db_info
    
    def _analyze_endpoints(self) -> Dict[str, Any]:
        """Analiza los endpoints disponibles"""
        endpoints_info = {
            'auth_endpoints': [],
            'user_endpoints': [],
            'business_endpoints': [],
            'product_endpoints': [],
            'public_endpoints': [],
            'insumo_endpoints': [],
            'total_endpoints': 0
        }
        
        # Analizar routers del backend
        router_files = [
            'backend/app/routers/auth_router.py',
            'backend/app/routers/user_router.py',
            'backend/app/routers/business_router.py',
            'backend/app/routers/product_router.py',
            'backend/app/routers/public_router.py',
            'backend/app/routers/insumo_router.py'
        ]
        
        for router_file in router_files:
            file_path = self.project_root / router_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Extraer endpoints usando regex
                    endpoints = re.findall(r'@router\.(get|post|put|delete)\([\'"]([^\'"]+)[\'"]', content)
                    
                    for method, path in endpoints:
                        # Generar descripción automática basada en método y ruta
                        description = self._generate_endpoint_description(method, path, router_file)
                        
                        endpoint_info = {
                            'method': method.upper(),
                            'path': path,
                            'description': description,
                            'file': router_file
                        }
                        
                        if 'auth' in router_file:
                            endpoints_info['auth_endpoints'].append(endpoint_info)
                        elif 'user' in router_file:
                            endpoints_info['user_endpoints'].append(endpoint_info)
                        elif 'business' in router_file:
                            endpoints_info['business_endpoints'].append(endpoint_info)
                        elif 'product' in router_file:
                            endpoints_info['product_endpoints'].append(endpoint_info)
                        elif 'public' in router_file:
                            endpoints_info['public_endpoints'].append(endpoint_info)
                        elif 'insumo' in router_file:
                            endpoints_info['insumo_endpoints'].append(endpoint_info)
                        
                        endpoints_info['total_endpoints'] += 1
                        
                except Exception as e:
                    print(f"⚠️  Error analizando {router_file}: {e}")
        
        return endpoints_info
    
    def _generate_endpoint_description(self, method: str, path: str, router_file: str) -> str:
        """Genera una descripción automática para un endpoint"""
        method_actions = {
            'get': 'Obtener',
            'post': 'Crear',
            'put': 'Actualizar',
            'delete': 'Eliminar'
        }
        
        action = method_actions.get(method.lower(), 'Procesar')
        
        # Determinar el recurso basado en la ruta y el archivo
        if 'auth' in router_file:
            if 'login' in path:
                return f"{action} token de autenticación"
            elif 'register' in path:
                return f"{action} nuevo usuario"
            else:
                return f"{action} datos de autenticación"
        elif 'user' in router_file:
            if 'profile' in path:
                return f"{action} perfil de usuario"
            elif 'cv' in path:
                return f"{action} curriculum vitae"
            else:
                return f"{action} datos de usuario"
        elif 'business' in router_file:
            if path == '/':
                return f"{action} lista de negocios"
            elif '{business_id}' in path:
                return f"{action} negocio específico"
            else:
                return f"{action} datos de negocio"
        elif 'product' in router_file:
            if path == '/':
                return f"{action} lista de productos"
            elif '{product_id}' in path:
                return f"{action} producto específico"
            else:
                return f"{action} datos de producto"
        elif 'insumo' in router_file:
            if path == '/':
                return f"{action} lista de insumos"
            elif '{insumo_id}' in path:
                return f"{action} insumo específico"
            else:
                return f"{action} datos de insumo"
        elif 'public' in router_file:
            if 'business' in path:
                return f"{action} información pública de negocios"
            elif 'product' in path:
                return f"{action} información pública de productos"
            elif 'user' in path:
                return f"{action} información pública de usuario"
            else:
                return f"{action} información pública"
        else:
            return f"{action} recurso"
    
    def _analyze_functionality(self) -> Dict[str, Any]:
        """Analiza las funcionalidades implementadas"""
        functionality = {
            'authentication': {
                'jwt_implementation': False,
                'user_registration': False,
                'user_login': False,
                'password_hashing': False
            },
            'business_management': {
                'crud_operations': False,
                'user_association': False,
                'business_types': False
            },
            'product_management': {
                'crud_operations': False,
                'business_association': False,
                'insumo_association': False,
                'price_calculations': False
            },
            'insumo_management': {
                'crud_operations': False,
                'user_association': False,
                'product_association': False
            },
            'public_access': {
                'business_listing': False,
                'product_listing': False,
                'no_auth_required': False
            },
            'frontend': {
                'dashboard': False,
                'navigation': False,
                'forms': False,
                'public_pages': False
            }
        }
        
        # Verificar funcionalidades basándose en archivos existentes
        files_to_check = {
            'authentication.jwt_implementation': 'backend/app/dependencies.py',
            'authentication.user_registration': 'backend/app/routers/auth_router.py',
            'authentication.user_login': 'backend/app/routers/auth_router.py',
            'authentication.password_hashing': 'backend/app/crud/user.py',
            'business_management.crud_operations': 'backend/app/crud/business.py',
            'business_management.user_association': 'backend/app/models.py',
            'business_management.business_types': 'backend/app/models.py',
            'product_management.crud_operations': 'backend/app/crud/product.py',
            'product_management.business_association': 'backend/app/models.py',
            'product_management.insumo_association': 'backend/app/models.py',
            'product_management.price_calculations': 'backend/app/crud/product.py',
            'insumo_management.crud_operations': 'backend/app/crud/insumo.py',
            'insumo_management.user_association': 'backend/app/models.py',
            'insumo_management.product_association': 'backend/app/models.py',
            'public_access.business_listing': 'backend/app/routers/public_router.py',
            'public_access.product_listing': 'backend/app/routers/public_router.py',
            'frontend.dashboard': 'frontend/src/screens/DashboardScreen.js',
            'frontend.navigation': 'frontend/src/App.js',
            'frontend.forms': 'frontend/src/components/ui/',
            'frontend.public_pages': 'frontend/src/screens/PublicListingScreen.js'
        }
        
        for feature_path, file_path in files_to_check.items():
            if '.' in feature_path:
                category, feature = feature_path.split('.')
                check_path = self.project_root / file_path
                
                if check_path.exists():
                    functionality[category][feature] = True
                elif check_path.is_dir() and any(check_path.iterdir()):
                    functionality[category][feature] = True
        
        return functionality
    
    def analyze_documentation_state(self) -> Dict[str, Any]:
        """Analiza el estado actual de la documentación"""
        print("📚 Analizando estado de la documentación...")
        
        docs_state = {
            'files': {},
            'coverage': {},
            'last_updated': {},
            'completeness': {}
        }
        
        # Analizar archivos de documentación
        doc_files = [
            'Documentación/DOCUMENTACION_TECNICA.md',
            'Documentación/INDICE_ARCHIVOS_ACTUALIZADO.md',
            'Documentación/Roadmap/ROADMAP_DEFINITIVO_MVP.md',
            'debugging/README.md',
            'debugging/HISTORIAL_DE_BUGS.md'
        ]
        
        for doc_file in doc_files:
            file_path = self.project_root / doc_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Obtener fecha de última actualización
                    last_update_match = re.search(r'Última actualización[:\s]*(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', content, re.IGNORECASE)
                    last_update = last_update_match.group(1) if last_update_match else 'No especificada'
                    
                    # Calcular completitud basada en contenido
                    completeness = self._calculate_documentation_completeness(content, doc_file)
                    
                    docs_state['files'][doc_file] = {
                        'size': len(content),
                        'last_updated': last_update,
                        'completeness': completeness,
                        'sections': len(re.findall(r'^##\s+', content, re.MULTILINE))
                    }
                    
                except Exception as e:
                    print(f"⚠️  Error analizando {doc_file}: {e}")
        
        self.documentation_state = docs_state
        return docs_state
    
    def _calculate_documentation_completeness(self, content: str, filename: str) -> float:
        """Calcula la completitud de un documento"""
        completeness = 0.0
        
        if 'DOCUMENTACION_TECNICA' in filename:
            # Verificar secciones principales
            sections = ['BASE DE DATOS', 'BACKEND', 'FRONTEND', 'ENDPOINTS', 'AUTENTICACIÓN']
            for section in sections:
                if section.lower() in content.lower():
                    completeness += 20.0
        
        elif 'INDICE_ARCHIVOS' in filename:
            # Verificar cobertura de archivos
            file_mentions = len(re.findall(r'\.(py|js|jsx|md|json)', content))
            completeness = min(100.0, file_mentions * 2)
        
        elif 'HISTORIAL_DE_BUGS' in filename:
            # Verificar bugs documentados
            bug_count = len(re.findall(r'### \d+\.\s+\*\*PROBLEMA:', content))
            completeness = min(100.0, bug_count * 10)
        
        elif 'README' in filename:
            # Verificar estructura básica
            if '## ' in content and '### ' in content:
                completeness = 80.0
        
        return completeness
    
    def identify_discrepancies(self) -> List[Dict[str, Any]]:
        """Identifica discrepancias entre el estado actual y la documentación"""
        print("🔍 Identificando discrepancias...")
        
        discrepancies = []
        
        # 1. Verificar cobertura de archivos
        current_files = self.current_state['files']
        doc_files = self.documentation_state['files']
        
        if 'Documentación/INDICE_ARCHIVOS_ACTUALIZADO.md' in doc_files:
            index_content = ""
            try:
                with open(self.project_root / 'Documentación/INDICE_ARCHIVOS_ACTUALIZADO.md', 'r', encoding='utf-8') as f:
                    index_content = f.read()
            except:
                pass
            
            # Verificar si los archivos actuales están documentados
            for file_type, count in current_files['file_types'].items():
                if file_type in ['.py', '.js', '.jsx'] and count > 0:
                    if file_type not in index_content:
                        discrepancies.append({
                            'type': 'missing_file_type',
                            'severity': 'medium',
                            'description': f'Tipo de archivo {file_type} no documentado en el índice',
                            'current': count,
                            'documented': 0
                        })
        
        # 2. Verificar funcionalidades documentadas vs implementadas
        functionality = self.current_state['functionality']
        
        # Leer el contenido de la documentación técnica para verificar funcionalidades
        tech_doc_content = ""
        tech_doc_path = self.project_root / 'Documentación/DOCUMENTACION_TECNICA.md'
        if tech_doc_path.exists():
            try:
                with open(tech_doc_path, 'r', encoding='utf-8') as f:
                    tech_doc_content = f.read()
            except:
                pass
        
        for category, features in functionality.items():
            for feature, implemented in features.items():
                if implemented:
                    # Normalizar nombres para comparación flexible
                    def normalize(text):
                        return re.sub(r'[^a-z0-9]', '', text.lower())
                    normalized_feature = normalize(feature)
                    normalized_category = normalize(category)
                    
                    # Buscar en la sección de funcionalidades implementadas
                    is_documented = False
                    if '📋 FUNCIONALIDADES IMPLEMENTADAS' in tech_doc_content:
                        # Buscar la categoría y funcionalidad específica
                        category_pattern = rf'### \*\*.*{normalized_category}.*\*\*'
                        category_matches = re.finditer(category_pattern, tech_doc_content, re.IGNORECASE)
                        for match in category_matches:
                            # Buscar la funcionalidad específica en esa categoría
                            # Tomar el bloque de la categoría
                            start = match.end()
                            end = tech_doc_content.find('###', start)
                            block = tech_doc_content[start:end] if end != -1 else tech_doc_content[start:]
                            # Buscar cualquier línea que contenga el nombre normalizado de la funcionalidad y un check ✅
                            for line in block.splitlines():
                                if normalize(line).find(normalized_feature) != -1 and '✅' in line:
                                    is_documented = True
                                    break
                            if is_documented:
                                break
                    # Si no está documentada, agregar discrepancia
                    if not is_documented:
                        discrepancies.append({
                            'type': 'missing_functionality_doc',
                            'severity': 'high',
                            'description': f'Funcionalidad {category}.{feature} implementada pero no documentada',
                            'category': category,
                            'feature': feature
                        })
        
        # 3. Verificar endpoints documentados vs implementados
        endpoints = self.current_state['endpoints']
        total_endpoints = endpoints['total_endpoints']
        
        if total_endpoints > 0:
            # Verificar si los endpoints están correctamente documentados en la documentación técnica
            if '🔗 ENDPOINTS API' in tech_doc_content:
                # Contar endpoints documentados en la sección de endpoints
                documented_endpoints = len(re.findall(r'- `(GET|POST|PUT|DELETE)\s+[^`]+`', tech_doc_content))
                
                # Si hay una diferencia significativa, agregar discrepancia
                if abs(documented_endpoints - total_endpoints) > 2:  # Tolerancia de 2 endpoints
                            discrepancies.append({
                                'type': 'endpoint_count_mismatch',
                                'severity': 'medium',
                        'description': f'Conteo de endpoints desactualizado en Documentación/DOCUMENTACION_TECNICA.md',
                                'current': total_endpoints,
                        'documented': documented_endpoints
                    })
            else:
                # Si no hay sección de endpoints, agregar discrepancia
                discrepancies.append({
                    'type': 'missing_endpoints_section',
                    'severity': 'high',
                    'description': 'Sección de endpoints no encontrada en la documentación técnica',
                    'current': total_endpoints,
                    'documented': 0
                })
        
        # 4. Verificar datos de ejemplo
        database = self.current_state['database']
        if database['status'] == 'connected':
            for table, info in database['records'].items():
                if info > 0:
                    # Verificar si los datos de ejemplo están documentados
                    if not any(f'{table}' in str(doc) for doc in doc_files.values()):
                        discrepancies.append({
                            'type': 'missing_data_doc',
                            'severity': 'low',
                            'description': f'Datos en tabla {table} no documentados',
                            'table': table,
                            'record_count': info
                        })
        
        self.discrepancies = discrepancies
        return discrepancies
    
    def generate_update_plan(self) -> Dict[str, Any]:
        """Genera un plan de actualización basado en las discrepancias"""
        print("📋 Generando plan de actualización...")
        
        update_plan = {
            'priority_updates': [],
            'recommended_updates': [],
            'optional_updates': [],
            'files_to_update': []
        }
        
        for discrepancy in self.discrepancies:
            if discrepancy['severity'] == 'high':
                update_plan['priority_updates'].append(discrepancy)
            elif discrepancy['severity'] == 'medium':
                update_plan['recommended_updates'].append(discrepancy)
            else:
                update_plan['optional_updates'].append(discrepancy)
        
        # Identificar archivos que necesitan actualización
        files_to_update = set()
        
        for discrepancy in self.discrepancies:
            if discrepancy['type'] == 'missing_functionality_doc':
                files_to_update.add('Documentación/DOCUMENTACION_TECNICA.md')
            elif discrepancy['type'] == 'endpoint_count_mismatch':
                files_to_update.add('Documentación/DOCUMENTACION_TECNICA.md')
            elif discrepancy['type'] == 'missing_file_type':
                files_to_update.add('Documentación/INDICE_ARCHIVOS_ACTUALIZADO.md')
        
        update_plan['files_to_update'] = list(files_to_update)
        
        return update_plan
    
    def auto_update_documents(self, update_plan: Dict[str, Any]) -> List[str]:
        """Actualiza automáticamente los documentos basándose en el plan"""
        print("🔄 Actualizando documentos automáticamente...")
        
        updated_files = []
        
        for file_path in update_plan['files_to_update']:
            full_path = self.project_root / file_path
            
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Actualizar fecha de última actualización
                    current_date = datetime.now().strftime("%d de %B de %Y")
                    
                    # Múltiples patrones para diferentes formatos de fecha
                    date_patterns = [
                        r'Última actualización[:\s]*\d{1,2}\s+de\s+\w+\s+de\s+\d{4}',
                        r'\*\*Última actualización:\*\*\s*\d{1,2}\s+de\s+\w+\s+de\s+\d{4}',
                        r'Fecha[:\s]*\d{1,2}\s+de\s+\w+\s+de\s+\d{4}',
                        r'\*\*Fecha:\*\*\s*\d{1,2}\s+de\s+\w+\s+de\s+\d{4}'
                    ]
                    
                    for pattern in date_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            content = re.sub(
                                pattern,
                        f'Última actualización: {current_date}',
                        content,
                        flags=re.IGNORECASE
                    )
                            break
                    else:
                        # Si no se encuentra ningún patrón, buscar al final del archivo
                        if 'Última actualización' not in content:
                            # Agregar al final del archivo
                            content = content.rstrip() + f'\n\n---\n\n**Última actualización:** {current_date}'
                    
                    # Actualizar estadísticas si es el índice
                    if 'INDICE_ARCHIVOS' in file_path:
                        content = self._update_index_statistics(content)
                    
                    # Actualizar documentación técnica si es necesario
                    if 'DOCUMENTACION_TECNICA' in file_path:
                        content = self._update_technical_documentation(content)
                    
                    # Guardar cambios si hubo modificaciones
                    if content != original_content:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        updated_files.append(file_path)
                        self.updates_made.append({
                            'file': file_path,
                            'changes': 'Auto-updated based on current project state'
                        })
                
                except Exception as e:
                    print(f"❌ Error actualizando {file_path}: {e}")
        
        return updated_files
    
    def _update_index_statistics(self, content: str) -> str:
        """Actualiza las estadísticas en el índice de archivos"""
        current_files = self.current_state['files']
        
        # Actualizar conteo de archivos
        content = re.sub(
            r'### \*\*Archivos Totales:\*\* ~\d+ archivos',
            f'### **Archivos Totales:** ~{current_files["total_files"]} archivos',
            content
        )
        
        # Actualizar conteo de endpoints
        total_endpoints = self.current_state['endpoints']['total_endpoints']
        content = re.sub(
            r'### \*\*Endpoints:\*\* \d+ endpoints',
            f'### **Endpoints:** {total_endpoints} endpoints',
            content
        )
        
        return content
    
    def _update_technical_documentation(self, content: str) -> str:
        """Actualiza la documentación técnica"""
        functionality = self.current_state['functionality']
        
        # Actualizar conteo de endpoints
        content = self._update_endpoints_count(content)
        
        # Reemplazar completamente la sección de funcionalidades implementadas
        functionality_section_pattern = r'(## 📋 FUNCIONALIDADES IMPLEMENTADAS\s*\n)(.*?)(?=\n##|\Z)'
        new_functionality_section = self._generate_functionality_section(functionality)
        if re.search(functionality_section_pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(functionality_section_pattern, new_functionality_section + '\n', content, flags=re.DOTALL | re.IGNORECASE)
        else:
            # Si no existe la sección, la agregamos antes de la sección de Endpoints
            endpoints_pattern = r'(## 🔗 ENDPOINTS API\s*\n)'
            endpoints_match = re.search(endpoints_pattern, content, re.DOTALL | re.IGNORECASE)
            if endpoints_match:
                content = content.replace(endpoints_match.group(1), new_functionality_section + '\n' + endpoints_match.group(1))
            else:
                # Si no hay sección de endpoints, agregar al final
                content += f"\n\n{new_functionality_section}"
        
        return content
    
    def _update_endpoints_count(self, content: str) -> str:
        """Actualiza el conteo de endpoints en la documentación técnica"""
        endpoints = self.current_state['endpoints']
        
        # Buscar y actualizar el conteo total de endpoints
        total_pattern = r'(### \*\*Total de Endpoints:\*\* )\d+'
        total_match = re.search(total_pattern, content, re.IGNORECASE)
        if total_match:
            content = re.sub(total_pattern, f"{total_match.group(1)}{endpoints['total_endpoints']}", content)
        
        # Buscar y actualizar conteos por categoría
        category_patterns = {
            'auth': r'(### \*\*Autenticación:\*\* )\d+',
            'user': r'(### \*\*Usuarios:\*\* )\d+',
            'business': r'(### \*\*Negocios:\*\* )\d+',
            'product': r'(### \*\*Productos:\*\* )\d+',
            'public': r'(### \*\*Públicos:\*\* )\d+',
            'insumo': r'(### \*\*Insumos:\*\* )\d+'
        }
        
        category_counts = {
            'auth': len(endpoints['auth_endpoints']),
            'user': len(endpoints['user_endpoints']),
            'business': len(endpoints['business_endpoints']),
            'product': len(endpoints['product_endpoints']),
            'public': len(endpoints['public_endpoints']),
            'insumo': len(endpoints['insumo_endpoints'])
        }
        
        for category, pattern in category_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                content = re.sub(pattern, f"{match.group(1)}{category_counts[category]}", content)
        
        # Actualizar secciones de endpoints
        content = self._update_endpoints_sections(content)
        
        return content
    
    def _update_endpoints_sections(self, content: str) -> str:
        """Actualiza las secciones de endpoints en la documentación técnica"""
        endpoints = self.current_state['endpoints']
        
        # Reemplazar completamente la sección de endpoints
        endpoints_section_pattern = r'(## 🔗 ENDPOINTS API\s*\n)(.*?)(?=\n##|\Z)'
        new_endpoints_section = self._generate_endpoints_section(endpoints)
        if re.search(endpoints_section_pattern, content, re.DOTALL | re.IGNORECASE):
            content = re.sub(endpoints_section_pattern, new_endpoints_section + '\n', content, flags=re.DOTALL | re.IGNORECASE)
        else:
            # Buscar un lugar apropiado para insertar (antes de la sección de diccionario)
            dict_pattern = r'(## 📚 DICCIONARIO DE REFERENCIA\s*\n)'
            dict_match = re.search(dict_pattern, content, re.DOTALL | re.IGNORECASE)
            if dict_match:
                content = content.replace(dict_match.group(1), new_endpoints_section + '\n' + dict_match.group(1))
            else:
                # Si no hay sección de diccionario, agregar al final
                content += f"\n\n{new_endpoints_section}"
        
        return content
    
    def _generate_endpoints_section(self, endpoints: Dict[str, Any]) -> str:
        """Genera una nueva sección de endpoints"""
        section = "## 🔗 ENDPOINTS API\n\n"
        
        # Autenticación
        if endpoints['auth_endpoints']:
            section += "### **Autenticación**\n"
            for endpoint in endpoints['auth_endpoints']:
                section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            section += "\n"
        
        # Usuarios
        if endpoints['user_endpoints']:
            section += "### **Usuarios**\n"
            for endpoint in endpoints['user_endpoints']:
                section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            section += "\n"
        
        # Negocios
        if endpoints['business_endpoints']:
            section += "### **Negocios**\n"
            for endpoint in endpoints['business_endpoints']:
                section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            section += "\n"
        
        # Productos
        if endpoints['product_endpoints']:
            section += "### **Productos**\n"
            for endpoint in endpoints['product_endpoints']:
                section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            section += "\n"
        
        # Insumos
        if endpoints['insumo_endpoints']:
            section += "### **Insumos**\n"
            for endpoint in endpoints['insumo_endpoints']:
                section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            section += "\n"
        
        # Públicos
        if endpoints['public_endpoints']:
            section += "### **Públicos**\n"
            for endpoint in endpoints['public_endpoints']:
                section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
            section += "\n"
        
        return section
    
    def _update_existing_endpoints_section(self, existing_section: str, endpoints: Dict[str, Any]) -> str:
        """Actualiza una sección existente de endpoints"""
        updated_section = ""
        
        # Procesar cada categoría de endpoints
        categories = {
            'Autenticación': endpoints['auth_endpoints'],
            'Usuarios': endpoints['user_endpoints'],
            'Negocios': endpoints['business_endpoints'],
            'Productos': endpoints['product_endpoints'],
            'Insumos': endpoints['insumo_endpoints'],
            'Públicos': endpoints['public_endpoints']
        }
        
        for category_name, category_endpoints in categories.items():
            if not category_endpoints:
                continue
                
            # Buscar la subsección de esta categoría
            category_pattern = rf'### \*\*{category_name}\*\*\s*\n(.*?)(?=\n###|\Z)'
            category_match = re.search(category_pattern, existing_section, re.DOTALL | re.IGNORECASE)
            
            if category_match:
                # Actualizar subsección existente
                subsection = category_match.group(1)
                updated_subsection = self._update_endpoints_subsection(subsection, category_endpoints)
                updated_section += f"### **{category_name}**\n{updated_subsection}\n"
            else:
                # Agregar nueva subsección
                updated_section += f"### **{category_name}**\n"
                for endpoint in category_endpoints:
                    updated_section += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
                updated_section += "\n"
        
        return updated_section
    
    def _update_endpoints_subsection(self, subsection: str, endpoints: List[Dict[str, str]]) -> str:
        """Actualiza una subsección de endpoints"""
        # Primero, extraer los endpoints existentes para evitar duplicados
        existing_endpoints = set()
        for line in subsection.split('\n'):
            if line.strip().startswith('- `') and '` - ' in line:
                # Extraer método y ruta del endpoint existente
                match = re.search(r'- `(\w+)\s+([^`]+)`', line)
                if match:
                    method, path = match.groups()
                    existing_endpoints.add(f"{method} {path.strip()}")
        
        updated_subsection = ""
        
        for endpoint in endpoints:
            endpoint_key = f"{endpoint['method']} {endpoint['path']}"
            
            if endpoint_key in existing_endpoints:
                # El endpoint ya existe, mantenerlo como está
                for line in subsection.split('\n'):
                    if line.strip().startswith('- `') and endpoint_key in line:
                        updated_subsection += line + '\n'
                        break
            else:
                # Agregar nuevo endpoint
                updated_subsection += f"- `{endpoint['method']} {endpoint['path']}` - {endpoint['description']}\n"
        
        return updated_subsection
    
    def _generate_functionality_section(self, functionality: Dict[str, Dict[str, bool]]) -> str:
        """Genera una nueva sección de funcionalidades"""
        section = "## 📋 FUNCIONALIDADES IMPLEMENTADAS\n\n"
        
        for category, features in functionality.items():
            category_title = category.replace('_', ' ').title()
            section += f"### **{category_title}**\n"
            
                for feature, implemented in features.items():
                    status = "✅" if implemented else "❌"
                feature_name = feature.replace('_', ' ').title()
                section += f"- {feature_name}: {status}\n"
            
            section += "\n"
        
        return section
    
    def _update_existing_functionality_section(self, existing_section: str, functionality: Dict[str, Dict[str, bool]]) -> str:
        """Actualiza una sección existente de funcionalidades"""
        updated_section = ""
        
        for category, features in functionality.items():
            category_title = category.replace('_', ' ').title()
            
            # Buscar la subsección de esta categoría
            category_pattern = rf'### \*\*{category_title}\*\*\s*\n(.*?)(?=\n###|\Z)'
            category_match = re.search(category_pattern, existing_section, re.DOTALL | re.IGNORECASE)
            
            if category_match:
                # Actualizar subsección existente
                subsection = category_match.group(1)
                updated_subsection = self._update_functionality_subsection(subsection, features)
                updated_section += f"### **{category_title}**\n{updated_subsection}\n"
            else:
                # Agregar nueva subsección
                updated_section += f"### **{category_title}**\n"
                for feature, implemented in features.items():
                    status = "✅" if implemented else "❌"
                    feature_name = feature.replace('_', ' ').title()
                    updated_section += f"- {feature_name}: {status}\n"
                updated_section += "\n"
        
        return updated_section
    
    def _update_functionality_subsection(self, subsection: str, features: Dict[str, bool]) -> str:
        """Actualiza una subsección de funcionalidades"""
        updated_subsection = ""
        
        for feature, implemented in features.items():
            status = "✅" if implemented else "❌"
            feature_name = feature.replace('_', ' ').title()
            
            # Buscar si la funcionalidad ya existe en la subsección
            feature_pattern = rf'- {feature_name}.*'
            feature_match = re.search(feature_pattern, subsection, re.IGNORECASE)
            
            if feature_match:
                # Actualizar funcionalidad existente
                updated_subsection += f"- {feature_name}: {status}\n"
            else:
                # Agregar nueva funcionalidad
                updated_subsection += f"- {feature_name}: {status}\n"
        
        return updated_subsection
    
    def generate_report(self) -> str:
        """Genera un reporte completo de la actualización"""
        report = f"""
# 📊 REPORTE DE ACTUALIZACIÓN DE DOCUMENTACIÓN

**Fecha:** {datetime.now().strftime("%d de %B de %Y")}
**Proyecto:** SOUP Emprendimientos

## 📈 ESTADO ACTUAL DEL PROYECTO

### Archivos del Proyecto
- **Total de archivos:** {self.current_state['files']['total_files']}
- **Backend:** {self.current_state['files']['backend_files']} archivos
- **Frontend:** {self.current_state['files']['frontend_files']} archivos
- **Debugging:** {self.current_state['files']['debugging_files']} archivos
- **Documentación:** {self.current_state['files']['documentation_files']} archivos

### Base de Datos
- **Estado:** {self.current_state['database']['status']}
- **Tablas principales:** {len(self.current_state['database']['tables'])}
- **Total de registros:** {sum(self.current_state['database']['records'].values())}

### Endpoints
- **Total de endpoints:** {self.current_state['endpoints']['total_endpoints']}
- **Autenticación:** {len(self.current_state['endpoints']['auth_endpoints'])}
- **Usuarios:** {len(self.current_state['endpoints']['user_endpoints'])}
- **Negocios:** {len(self.current_state['endpoints']['business_endpoints'])}
- **Productos:** {len(self.current_state['endpoints']['product_endpoints'])}
- **Públicos:** {len(self.current_state['endpoints']['public_endpoints'])}
- **Insumos:** {len(self.current_state['endpoints']['insumo_endpoints'])}

## 🔍 DISCREPANCIAS IDENTIFICADAS

### Prioridad Alta ({len([d for d in self.discrepancies if d['severity'] == 'high'])})
"""
        
        for discrepancy in self.discrepancies:
            if discrepancy['severity'] == 'high':
                report += f"- **{discrepancy['description']}**\n"
        
        report += f"""
### Prioridad Media ({len([d for d in self.discrepancies if d['severity'] == 'medium'])})
"""
        
        for discrepancy in self.discrepancies:
            if discrepancy['severity'] == 'medium':
                report += f"- **{discrepancy['description']}**\n"
        
        report += f"""
### Prioridad Baja ({len([d for d in self.discrepancies if d['severity'] == 'low'])})
"""
        
        for discrepancy in self.discrepancies:
            if discrepancy['severity'] == 'low':
                report += f"- **{discrepancy['description']}**\n"
        
        report += f"""
## 🔄 ACTUALIZACIONES REALIZADAS

### Archivos Actualizados ({len(self.updates_made)})
"""
        
        for update in self.updates_made:
            report += f"- **{update['file']}**: {update['changes']}\n"
        
        report += f"""
## 📋 FUNCIONALIDADES IMPLEMENTADAS

### Autenticación
"""
        
        auth_features = self.current_state['functionality']['authentication']
        for feature, implemented in auth_features.items():
            status = "✅" if implemented else "❌"
            report += f"- {feature}: {status}\n"
        
        report += f"""
### Gestión de Negocios
"""
        
        business_features = self.current_state['functionality']['business_management']
        for feature, implemented in business_features.items():
            status = "✅" if implemented else "❌"
            report += f"- {feature}: {status}\n"
        
        report += f"""
### Gestión de Productos
"""
        
        product_features = self.current_state['functionality']['product_management']
        for feature, implemented in product_features.items():
            status = "✅" if implemented else "❌"
            report += f"- {feature}: {status}\n"
        
        report += f"""
### Frontend
"""
        
        frontend_features = self.current_state['functionality']['frontend']
        for feature, implemented in frontend_features.items():
            status = "✅" if implemented else "❌"
            report += f"- {feature}: {status}\n"
        
        report += f"""
## 🎯 RECOMENDACIONES

1. **Revisar discrepancias de alta prioridad** antes del próximo commit
2. **Actualizar manualmente** las discrepancias que requieren intervención humana
3. **Ejecutar este script regularmente** para mantener la documentación actualizada
4. **Revisar funcionalidades no implementadas** para planificar próximas iteraciones

## 📝 NOTAS

- Este reporte se generó automáticamente
- Las actualizaciones automáticas se aplicaron a {len(self.updates_made)} archivos
- Se identificaron {len(self.discrepancies)} discrepancias en total
- El proyecto está en estado **{'OPERATIVO' if len(self.discrepancies) < 5 else 'REQUIERE ATENCIÓN'}**

---
**Generado por:** Script de Actualización de Documentación  
**Versión:** 1.0
"""
        
        return report
    
    def save_report(self, report: str):
        """Guarda el reporte en un archivo"""
        report_path = self.project_root / 'debugging' / 'reportes' / f'actualizacion_documentacion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        # Crear directorio si no existe
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Reporte guardado en: {report_path}")
        return str(report_path)

def main():
    """Función principal del script"""
    print("🚀 INICIANDO ACTUALIZACIÓN AUTOMÁTICA DE DOCUMENTACIÓN")
    print("=" * 60)
    
    updater = DocumentacionUpdater()
    
    # 1. Analizar estado actual
    current_state = updater.analyze_current_state()
    
    # 2. Analizar estado de documentación
    docs_state = updater.analyze_documentation_state()
    
    # 3. Identificar discrepancias
    discrepancies = updater.identify_discrepancies()
    
    # 4. Generar plan de actualización
    update_plan = updater.generate_update_plan()
    
    # 5. Mostrar resumen
    print(f"\n📊 RESUMEN DE ANÁLISIS:")
    print(f"   - Archivos del proyecto: {current_state['files']['total_files']}")
    print(f"   - Endpoints implementados: {current_state['endpoints']['total_endpoints']}")
    print(f"   - Discrepancias encontradas: {len(discrepancies)}")
    print(f"   - Archivos a actualizar: {len(update_plan['files_to_update'])}")
    
    # 6. Preguntar si proceder con actualizaciones automáticas
    if update_plan['files_to_update']:
        print(f"\n🔄 ARCHIVOS QUE SE ACTUALIZARÁN AUTOMÁTICAMENTE:")
        for file in update_plan['files_to_update']:
            print(f"   - {file}")
        
        response = input("\n¿Proceder con las actualizaciones automáticas? (s/n): ").lower().strip()
        
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            updated_files = updater.auto_update_documents(update_plan)
            print(f"\n✅ Archivos actualizados: {len(updated_files)}")
        else:
            print("\n⚠️  Actualizaciones automáticas canceladas")
    else:
        print("\n✅ No se requieren actualizaciones automáticas")
    
    # 7. Generar y guardar reporte
    report = updater.generate_report()
    report_path = updater.save_report(report)
    
    print(f"\n📋 REPORTE COMPLETO:")
    print(report)
    
    print(f"\n🎉 PROCESO COMPLETADO")
    print(f"   - Reporte guardado en: {report_path}")
    print(f"   - Discrepancias identificadas: {len(discrepancies)}")
    print(f"   - Archivos actualizados: {len(updater.updates_made)}")

if __name__ == "__main__":
    main() 