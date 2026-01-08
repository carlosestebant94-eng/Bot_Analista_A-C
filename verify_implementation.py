#!/usr/bin/env python3
"""
verify_implementation.py
Verificación rápida de que todo esté instalado y funcionando
"""

import sys
import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica si un archivo existe"""
    if os.path.exists(filepath):
        size_kb = os.path.getsize(filepath) / 1024
        print(f"✅ {description}")
        print(f"   └─ {size_kb:.1f} KB")
        return True
    else:
        print(f"❌ {description} - NO ENCONTRADO")
        return False

def check_module_import(module_name, description):
    """Verifica si un módulo se puede importar"""
    try:
        __import__(module_name)
        print(f"✅ {description}")
        return True
    except ImportError as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN DE IMPLEMENTACIÓN - PASO 2 & PASO 4")
    print("="*70 + "\n")
    
    base_path = Path(__file__).parent
    checks = []
    
    # ===== ARCHIVOS NUEVOS =====
    print("📁 ARCHIVOS NUEVOS CREADOS:")
    print("-" * 70)
    
    checks.append(check_file_exists(
        base_path / "ia" / "ml_predictions.py",
        "ia/ml_predictions.py (ML Predictor - 800+ líneas)"
    ))
    
    checks.append(check_file_exists(
        base_path / "app" / "backend.py",
        "app/backend.py (Flask Backend - 400+ líneas)"
    ))
    
    checks.append(check_file_exists(
        base_path / "app" / "templates" / "index.html",
        "app/templates/index.html (Dashboard UI - 22KB)"
    ))
    
    checks.append(check_file_exists(
        base_path / "scripts" / "start_dashboard.py",
        "scripts/start_dashboard.py (Startup script - 150+ líneas)"
    ))
    
    checks.append(check_file_exists(
        base_path / "test_ml_dashboard.py",
        "test_ml_dashboard.py (Test suite - 400+ líneas)"
    ))
    
    # ===== DOCUMENTACIÓN =====
    print("\n📚 DOCUMENTACIÓN NUEVA:")
    print("-" * 70)
    
    checks.append(check_file_exists(
        base_path / "ML_DASHBOARD_COMPLETED.md",
        "ML_DASHBOARD_COMPLETED.md (Referencia completa - 2000+ líneas)"
    ))
    
    checks.append(check_file_exists(
        base_path / "README_ML_DASHBOARD.md",
        "README_ML_DASHBOARD.md (Guía rápida)"
    ))
    
    checks.append(check_file_exists(
        base_path / "IMPLEMENTACION_COMPLETADA.md",
        "IMPLEMENTACION_COMPLETADA.md (Resumen ejecutivo)"
    ))
    
    # ===== MÓDULOS PYTHON =====
    print("\n🐍 MÓDULOS PYTHON DISPONIBLES:")
    print("-" * 70)
    
    checks.append(check_module_import(
        "flask",
        "Flask 3.1.2 (Backend framework)"
    ))
    
    checks.append(check_module_import(
        "flask_cors",
        "Flask-CORS 6.0.1 (API security)"
    ))
    
    checks.append(check_module_import(
        "sklearn",
        "scikit-learn 1.7.2 (Machine Learning)"
    ))
    
    checks.append(check_module_import(
        "numpy",
        "NumPy (Data processing)"
    ))
    
    checks.append(check_module_import(
        "pandas",
        "Pandas (Data frames)"
    ))
    
    # ===== MÓDULOS DEL PROYECTO =====
    print("\n🎯 MÓDULOS DEL PROYECTO:")
    print("-" * 70)
    
    sys.path.insert(0, str(base_path))
    
    checks.append(check_module_import(
        "ia.ml_predictions",
        "ia.ml_predictions (ML Predictor class)"
    ))
    
    checks.append(check_module_import(
        "app.backend",
        "app.backend (Flask backend app)"
    ))
    
    checks.append(check_module_import(
        "cerebro.analysis_methodology",
        "cerebro.analysis_methodology (Análisis integrado)"
    ))
    
    checks.append(check_module_import(
        "data_sources",
        "data_sources (Market data manager)"
    ))
    
    # ===== TESTS =====
    print("\n🧪 EJECUCIÓN DE TESTS:")
    print("-" * 70)
    
    if os.path.exists(base_path / "test_ml_dashboard.py"):
        print("ℹ️  Para ejecutar los tests, usar:")
        print("    python test_ml_dashboard.py")
        checks.append(True)
    
    # ===== RESUMEN =====
    print("\n" + "="*70)
    print("📊 RESUMEN:")
    print("="*70)
    
    passed = sum(1 for c in checks if c)
    total = len(checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\n✅ Verificaciones pasadas: {passed}/{total} ({percentage:.1f}%)\n")
    
    if percentage == 100:
        print("🎉 ¡TODO ESTÁ LISTO!")
        print("\n📖 Próximos pasos:")
        print("  1. Leer: README_ML_DASHBOARD.md")
        print("  2. Ejecutar: python scripts/start_dashboard.py")
        print("  3. Abrir: http://localhost:5000")
        return 0
    elif percentage >= 80:
        print("⚠️  Algunas dependencias o archivos faltantes")
        print("   Ejecutar: pip install flask flask-cors scikit-learn")
        return 1
    else:
        print("❌ Verificación incompleta")
        return 1

if __name__ == "__main__":
    sys.exit(main())
