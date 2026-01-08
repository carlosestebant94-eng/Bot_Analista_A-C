"""
config/secrets_manager.py
PUNTO 3: Gestión centralizada y segura de credenciales
Punto único para todas las claves y secretos del proyecto
"""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import json

logger = logging.getLogger("SecretsManager")


class SecretsManager:
    """
    Gestiona credenciales de forma segura
    
    Características:
    - Lee desde variables de entorno
    - NO expone keys en logs
    - Valida que existan
    - Centraliza todas las credenciales
    """
    
    # Credenciales requeridas
    REQUIRED_SECRETS = {
        'FRED_API_KEY': 'Federal Reserve API Key',
        'GOOGLE_API_KEY': 'Google Gemini API Key',
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot Token',
    }
    
    # Credenciales opcionales
    OPTIONAL_SECRETS = {
        'POLYGON_API_KEY': 'Polygon.io API Key',
        'ALPHA_VANTAGE_KEY': 'Alpha Vantage API Key',
    }
    
    def __init__(self):
        """Inicializa el gestor de secretos"""
        self.secrets: Dict[str, Optional[str]] = {}
        self._load_secrets()
    
    def _load_secrets(self) -> None:
        """Carga secretos desde variables de entorno"""
        # Cargar requeridos
        for key, description in self.REQUIRED_SECRETS.items():
            value = os.getenv(key)
            if not value:
                logger.warning(f"⚠️  Secreto requerido NO encontrado: {key} ({description})")
            else:
                self.secrets[key] = value
                logger.info(f"✅ Secreto cargado: {key}")
        
        # Cargar opcionales
        for key, description in self.OPTIONAL_SECRETS.items():
            value = os.getenv(key)
            if value:
                self.secrets[key] = value
                logger.info(f"✅ Secreto opcional cargado: {key}")
            else:
                logger.debug(f"ℹ️  Secreto opcional no configurado: {key}")
    
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtiene un secreto de forma segura
        
        IMPORTANTE: Esta función NUNCA retorna el secreto completo en logs
        
        Args:
            key: Nombre del secreto
            default: Valor por defecto si no existe
            
        Returns:
            Valor del secreto o None
        """
        if key not in self.secrets and key not in self.REQUIRED_SECRETS and key not in self.OPTIONAL_SECRETS:
            logger.warning(f"⚠️  Intento de acceso a secreto desconocido: {key}")
            return default
        
        return self.secrets.get(key, default)
    
    def validate_secrets(self) -> bool:
        """
        Valida que todos los secretos requeridos estén configurados
        
        Returns:
            True si están todos, False en caso contrario
        """
        missing = []
        for key in self.REQUIRED_SECRETS:
            if key not in self.secrets or not self.secrets[key]:
                missing.append(key)
        
        if missing:
            logger.error(f"❌ Secretos requeridos faltantes: {', '.join(missing)}")
            return False
        
        logger.info("✅ Todos los secretos requeridos están configurados")
        return True
    
    def get_masked_secrets(self) -> Dict[str, str]:
        """
        Retorna estado de secretos con valores enmascarados
        Útil para debugging sin exponer keys
        
        Returns:
            Dict con status y primeros 4 caracteres enmascarados
        """
        result = {}
        
        for key, description in self.REQUIRED_SECRETS.items():
            if key in self.secrets and self.secrets[key]:
                masked = f"{self.secrets[key][:4]}...***"
                result[key] = f"✅ Configurado ({masked})"
            else:
                result[key] = "❌ NO configurado"
        
        for key, description in self.OPTIONAL_SECRETS.items():
            if key in self.secrets and self.secrets[key]:
                masked = f"{self.secrets[key][:4]}...***"
                result[key] = f"✅ Configurado ({masked})"
            else:
                result[key] = "⚠️  No configurado"
        
        return result
    
    def generate_env_template(self) -> str:
        """
        Genera un archivo .env.example para documentación
        
        Returns:
            Contenido del template
        """
        template = "# PLANTILLA .env - Copy a .env y completa los valores\n\n"
        template += "# Secretos REQUERIDOS\n"
        for key, description in self.REQUIRED_SECRETS.items():
            template += f"# {description}\n"
            template += f"{key}=your_key_here\n\n"
        
        template += "# Secretos OPCIONALES\n"
        for key, description in self.OPTIONAL_SECRETS.items():
            template += f"# {description}\n"
            template += f"# {key}=your_key_here\n\n"
        
        return template


# Instancia global del gestor de secretos
_secrets_manager: Optional[SecretsManager] = None


def get_secrets_manager() -> SecretsManager:
    """Obtiene la instancia singleton del gestor de secretos"""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
    return _secrets_manager


# Funciones de conveniencia
def get_fred_key() -> Optional[str]:
    """Obtiene la API key de FRED"""
    return get_secrets_manager().get_secret('FRED_API_KEY')


def get_google_key() -> Optional[str]:
    """Obtiene la API key de Google Gemini"""
    return get_secrets_manager().get_secret('GOOGLE_API_KEY')


def get_telegram_token() -> Optional[str]:
    """Obtiene el token de Telegram"""
    return get_secrets_manager().get_secret('TELEGRAM_BOT_TOKEN')


def get_polygon_key() -> Optional[str]:
    """Obtiene la API key de Polygon.io"""
    return get_secrets_manager().get_secret('POLYGON_API_KEY')


def get_alpha_vantage_key() -> Optional[str]:
    """Obtiene la API key de Alpha Vantage"""
    return get_secrets_manager().get_secret('ALPHA_VANTAGE_KEY')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test del gestor
    manager = get_secrets_manager()
    
    print("\n🔐 ESTADO DE SECRETOS (valores enmascarados)")
    print("=" * 60)
    masked = manager.get_masked_secrets()
    for key, status in masked.items():
        print(f"{key:25} {status}")
    
    print("\n📋 VALIDACIÓN")
    print("=" * 60)
    is_valid = manager.validate_secrets()
    print(f"Validación: {'✅ PASS' if is_valid else '❌ FAIL'}")
    
    print("\n📝 TEMPLATE .env.example")
    print("=" * 60)
    template = manager.generate_env_template()
    print(template)
