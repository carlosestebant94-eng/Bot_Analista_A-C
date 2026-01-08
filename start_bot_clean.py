#!/usr/bin/env python3
"""Script limpio para iniciar el bot sin problemas de imports"""

import sys
import os

# Limpiar variables de entorno que interfieran
os.environ.pop('PYTHONHOME', None)
os.environ.pop('CONDA_DEFAULT_ENV', None)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

# Importar e iniciar el bot
if __name__ == '__main__':
    from main import main
    main()
