#!/usr/bin/env python3
"""
SCRIPT DE VALIDACION PRE-DEPLOYMENT
Fase 5C: Verificar que todo está listo para producción

Uso:
    python PRE_DEPLOYMENT_VALIDATION.py
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DeploymentValidator:
    """Validador pre-deployment para Railway"""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.errors = []
        self.warnings = []
        
    def log_success(self, message):
        """Log de éxito"""
        self.checks_passed += 1
        print(f"  ✓ {message}")
    
    def log_error(self, message):
        """Log de error"""
        self.checks_failed += 1
        self.errors.append(message)
        print(f"  ✗ {message}")
    
    def log_warning(self, message):
        """Log de advertencia"""
        self.warnings.append(message)
        print(f"  ⚠ {message}")
    
    def check_files(self):
        """Verificar archivos necesarios"""
        print("\n[1/7] Verificando archivos...")
        
        required_files = {
            'main.py': 'Punto de entrada principal',
            'Procfile': 'Configuración para Railway',
            'requirements.txt': 'Dependencias Python',
            '.env': 'Variables de entorno (local)',
            'telegram_bot/bot.py': 'Bot de Telegram',
            '.gitignore': 'Configuración Git',
        }
        
        for file, description in required_files.items():
            if Path(file).exists():
                self.log_success(f"{file} ({description})")
            else:
                self.log_error(f"Falta {file} ({description})")
    
    def check_env_variables(self):
        """Verificar variables de entorno"""
        print("\n[2/7] Verificando variables de entorno...")
        
        required_vars = {
            'TELEGRAM_TOKEN': 'Token del bot de Telegram',
            'GOOGLE_API_KEY': 'API Key de Google Gemini',
            'FRED_API_KEY': 'API Key de FRED',
            'POLYGON_API_KEY': 'API Key de Polygon',
            'ALPHA_VANTAGE_KEY': 'API Key de Alpha Vantage',
        }
        
        optional_vars = {
            'LOG_LEVEL': 'Nivel de logging (INFO, DEBUG)',
            'ENVIRONMENT': 'Entorno (development, production)',
        }
        
        # Verificar variables requeridas
        for var, description in required_vars.items():
            if os.getenv(var):
                self.log_success(f"{var} presente")
            else:
                self.log_warning(f"{var} no definida - necesaria para Railway")
        
        # Verificar variables opcionales
        for var, description in optional_vars.items():
            if os.getenv(var):
                self.log_success(f"{var} = {os.getenv(var)}")
            else:
                self.log_warning(f"{var} no definida (usará default)")
    
    def check_imports(self):
        """Verificar que los imports funcionan"""
        print("\n[3/7] Verificando imports...")
        
        try:
            import telegram
            self.log_success("python-telegram-bot importado")
        except ImportError:
            self.log_error("python-telegram-bot NO instalado")
        
        try:
            import google.generativeai
            self.log_success("google-generativeai importado")
        except ImportError:
            self.log_error("google-generativeai NO instalado")
        
        try:
            from telegram_bot.bot import TelegramAnalystBot
            self.log_success("TelegramAnalystBot importado")
        except ImportError as e:
            self.log_error(f"No se puede importar TelegramAnalystBot: {e}")
        
        try:
            from logging_audit import setup_centralized_logging
            self.log_success("Logging centralizado importado")
        except ImportError as e:
            self.log_error(f"No se puede importar logging: {e}")
    
    def check_procfile(self):
        """Verificar Procfile"""
        print("\n[4/7] Verificando Procfile...")
        
        if Path('Procfile').exists():
            with open('Procfile', 'r') as f:
                content = f.read().strip()
            
            if 'python main.py' in content:
                self.log_success("Procfile configurado correctamente")
            else:
                self.log_error(f"Procfile incorrecto. Debe contener: 'worker: python main.py'")
                self.log_warning(f"Contenido actual: {content}")
        else:
            self.log_error("Procfile no existe")
    
    def check_requirements(self):
        """Verificar requirements.txt"""
        print("\n[5/7] Verificando requirements.txt...")
        
        if Path('requirements.txt').exists():
            with open('requirements.txt', 'r') as f:
                content = f.read()
            
            required_packages = [
                'python-telegram-bot',
                'google-generativeai',
                'pandas',
                'yfinance',
                'scikit-learn',
            ]
            
            for package in required_packages:
                if package in content:
                    self.log_success(f"{package} en requirements.txt")
                else:
                    self.log_warning(f"{package} NO en requirements.txt (necesario)")
        else:
            self.log_error("requirements.txt no existe")
    
    def check_git(self):
        """Verificar configuración de Git"""
        print("\n[6/7] Verificando configuración Git...")
        
        # Verificar .gitignore
        if Path('.gitignore').exists():
            with open('.gitignore', 'r') as f:
                content = f.read()
            
            if '.env' in content:
                self.log_success(".env está en .gitignore (seguro)")
            else:
                self.log_error(".env NO está en .gitignore (RIESGO SEGURIDAD)")
            
            if '*.db' in content or '*.sqlite' in content:
                self.log_success("Bases de datos ignoradas")
            else:
                self.log_warning("Bases de datos podrían pushearse a GitHub")
        else:
            self.log_error(".gitignore no existe")
        
        # Verificar si hay un repositorio Git
        if Path('.git').exists():
            self.log_success("Repositorio Git configurado")
        else:
            self.log_warning("Repositorio Git NO inicializado - ejecutar: git init")
    
    def check_main_py(self):
        """Verificar main.py"""
        print("\n[7/7] Verificando main.py...")
        
        if Path('main.py').exists():
            with open('main.py', 'r') as f:
                content = f.read()
            
            if 'setup_centralized_logging' in content:
                self.log_success("main.py tiene logging centralizado")
            else:
                self.log_warning("main.py podría no tener logging (pero es opcional)")
            
            if '__main__' in content:
                self.log_success("main.py tiene punto de entrada correcto")
            else:
                self.log_warning("main.py podría no ejecutarse correctamente")
        else:
            self.log_error("main.py no existe")
    
    def print_summary(self):
        """Imprimir resumen"""
        print("\n" + "="*80)
        print("                    RESUMEN PRE-DEPLOYMENT")
        print("="*80)
        
        print(f"\n✓ Checks pasados: {self.checks_passed}")
        print(f"✗ Checks fallidos: {self.checks_failed}")
        print(f"⚠ Advertencias: {len(self.warnings)}")
        
        if self.errors:
            print("\n[ERRORES - DEBEN ARREGLARSE]:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n[ADVERTENCIAS - REVISAR]:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        print("\n" + "="*80)
        
        if self.checks_failed == 0:
            print("✓ LISTO PARA DEPLOYMENT A RAILWAY")
            print("  Próximo paso: git push origin main")
            print("  Luego: Crear proyecto en railway.app")
            return True
        else:
            print("✗ NO LISTO - Arreglar errores arriba")
            return False
    
    def run(self):
        """Ejecutar todas las validaciones"""
        print("\n" + "="*80)
        print("         PRE-DEPLOYMENT VALIDATION - FASE 5C")
        print("="*80)
        
        self.check_files()
        self.check_env_variables()
        self.check_imports()
        self.check_procfile()
        self.check_requirements()
        self.check_git()
        self.check_main_py()
        
        return self.print_summary()


if __name__ == '__main__':
    validator = DeploymentValidator()
    success = validator.run()
    
    # Exit code 0 si todo está bien, 1 si hay errores
    sys.exit(0 if success else 1)
