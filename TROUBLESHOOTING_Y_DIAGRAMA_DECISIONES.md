# 🔍 TROUBLESHOOTING Y DIAGRAMA DE DECISIONES

## Solución de Problemas Comunes

---

## PARTE 1: ÁRBOL DE DECISIONES DE INICIO

```
┌──────────────────────────────────────────────────────────┐
│  ¿QUIERES REPLICAR LA ARQUITECTURA?                      │
└──────────────┬───────────────────────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
       SÍ            NO
        │             │
        ▼             └─ Ir a CASOS DE USO
    ┌────────────────────────┐
    │ Nivel de experiencia:  │
    └────┬───────┬───────────┘
         │       │
      JUNIOR   SENIOR
         │       │
    ┌────▼─┐ ┌──▼────┐
    │      │ │       │
  6-8h   3-4h
```

---

## PARTE 2: MATRIZ DE PROBLEMAS COMUNES

### CATEGORÍA A: PROBLEMAS DE CONFIGURACIÓN

#### ❌ Problema A.1: Token de Telegram no funciona
```
ERROR: Response from Telegram: {"ok":false,"error_code":401}

CAUSA: Token inválido, expirado o mal copiado
SOLUCIÓN:
  1. Ir a BotFather en Telegram
  2. Usar /token para renovar
  3. Copiar token COMPLETO (sin espacios)
  4. Pegar en .env exactamente
  5. Reiniciar bot
  
VERIFICACIÓN:
  python -c "from config.settings import settings; print(settings.TELEGRAM_TOKEN)"
```

#### ❌ Problema A.2: API Gemini no responde
```
ERROR: API key not found or invalid

CAUSA: Clave API incorrecta, expirada o permisos faltantes
SOLUCIÓN:
  1. Ir a console.cloud.google.com
  2. Crear proyecto nuevo
  3. Habilitar Generative AI API
  4. Crear clave API (API key, no service account)
  5. Copiar en .env como GEMINI_API_KEY
  
VERIFICACIÓN:
  python -c "import google.generativeai as genai; print('OK')"
```

#### ❌ Problema A.3: .env no se carga
```
ERROR: NameError: name 'settings' is not found

CAUSA: .env no está en la raíz del proyecto
SOLUCIÓN:
  1. Verificar que .env está en la carpeta principal
  2. No en subcarpetas
  3. python -m dotenv list (para ver variables)
  
VERIFICACIÓN:
  from dotenv import load_dotenv
  load_dotenv()
  import os
  print(os.getenv('TELEGRAM_TOKEN'))
```

---

### CATEGORÍA B: PROBLEMAS DE INSTALACIÓN

#### ❌ Problema B.1: ModuleNotFoundError: No module named 'telegram'
```
ERROR: ModuleNotFoundError: No module named 'telegram'

CAUSA: Dependencias no instaladas
SOLUCIÓN:
  1. .\venv\Scripts\Activate.ps1  (Activar venv)
  2. pip install -r requirements.txt
  3. pip install python-telegram-bot==22.5
  
VERIFICACIÓN:
  python -c "import telegram; print(telegram.__version__)"
```

#### ❌ Problema B.2: pip install falla en OpenCV
```
ERROR: Could not find a version that satisfies opencv-python

CAUSA: Compatible wheels no disponibles para tu Python
SOLUCIÓN:
  1. Actualizar pip: python -m pip install --upgrade pip
  2. Verificar Python version: python --version (debe ser 3.8+)
  3. Instalar uno por uno:
     pip install numpy
     pip install opencv-python==4.8.1.78
  
ALTERNATIVA:
  pip install opencv-python-headless (sin GUI)
```

#### ❌ Problema B.3: Error en pytesseract
```
ERROR: pytesseract.TesseractNotFoundError: tesseract is not installed

CAUSA: Tesseract OCR no instalado en sistema
SOLUCIÓN (Windows):
  1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
  2. Instalar en C:\Program Files\Tesseract-OCR
  3. En código:
     import pytesseract
     pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SOLUCIÓN (Linux):
  sudo apt-get install tesseract-ocr

SOLUCIÓN (macOS):
  brew install tesseract
```

---

### CATEGORÍA C: PROBLEMAS DE BASE DE DATOS

#### ❌ Problema C.1: Error al crear tabla
```
ERROR: sqlite3.OperationalError: table documents already exists

CAUSA: Tabla ya existe (intento de crear duplicada)
SOLUCIÓN:
  1. Primera ejecución: OK (crea tablas)
  2. Ejecuciones posteriores: Ignora (IF NOT EXISTS)
  3. Si necesita limpiar:
     rm data/bot_database.db
     python main.py
```

#### ❌ Problema C.2: Base de datos bloqueada
```
ERROR: sqlite3.OperationalError: database is locked

CAUSA: Otra instancia del bot accediendo a BD
SOLUCIÓN:
  1. Verificar que solo una instancia corre
  2. Si hay múltiples, detener todas
  3. Esperar 5 segundos
  4. Reiniciar
  
VERIFICACIÓN:
  Get-Process python | Where-Object {$_.Path -like "*venv*"}
```

#### ❌ Problema C.3: Sin permisos en archivo de BD
```
ERROR: PermissionError: [Errno 13] Permission denied: 'data/bot_database.db'

CAUSA: Archivo de BD sin permisos de lectura/escritura
SOLUCIÓN:
  1. (Windows) Clic derecho → Propiedades → Seguridad
  2. Verificar permisos de usuario
  3. O simplemente: del data/bot_database.db
  4. Reiniciar bot (se recreará)
```

---

### CATEGORÍA D: PROBLEMAS DE BOT DE TELEGRAM

#### ❌ Problema D.1: Bot no responde a comandos
```
ERROR: No se ejecuta el handler al escribir /start

CAUSA: Múltiples causas posibles
SOLUCIÓN (checklist):
  1. ¿Está el bot en polling?
     logger debe mostrar "run_polling"
  
  2. ¿Respondió a /start en grupo?
     Agregar bot como admin
  
  3. ¿El token es correcto?
     python -c "from telegram import Bot; Bot('TOKEN').get_me()"
  
  4. ¿Hay excepciones no capturadas?
     Ver logs en logs/bot_analista.log
```

#### ❌ Problema D.2: Comando /analizar cuelga
```
ERROR: Comando comienza pero nunca responde (timeout)

CAUSA: Descarga de datos es lenta o falla
SOLUCIÓN:
  1. Añadir timeout:
     datos = yf.download(ticker, period="1y", timeout=10)
  
  2. Verificar ticker:
     if not Validator.validar_ticker(ticker):
         return "Ticker inválido"
  
  3. Usar async:
     async def comando_analizar(...):
         resultado = await self.analyzer.analizar_ticker(ticker)
  
  4. Mostrar progreso:
     procesando = await update.message.reply_text("⏳ Analizando...")
     await procesando.edit_text("✅ Análisis completo")
```

#### ❌ Problema D.3: Errores en manejador de imagen
```
ERROR: Al procesar imagen, falla

CAUSA: Imagen muy grande, formato incompatible, o sin soporte
SOLUCIÓN:
  1. Validar imagen primero:
     if not Validator.validar_imagen(ruta):
         return "Imagen no válida"
  
  2. Convertir formato:
     from PIL import Image
     img = Image.open(ruta).convert('RGB')
  
  3. Limitar tamaño:
     if img.size[0] * img.size[1] > 10_000_000:
         return "Imagen muy grande"
```

---

### CATEGORÍA E: PROBLEMAS DE RENDIMIENTO

#### ❌ Problema E.1: Bot lento respondiendo
```
ERROR: Demora >10 segundos en responder

CAUSA: Operación bloqueante, sin async
SOLUCIÓN:
  1. Usar async/await:
     async def comando(...):
         resultado = await algo_lento()
  
  2. Usar threading para operaciones largas:
     from threading import Thread
     thread = Thread(target=algo_lento)
     thread.start()
  
  3. Caché de resultados:
     cache = {}
     if ticker in cache:
         return cache[ticker]
```

#### ❌ Problema E.2: Memoria se llenan de logs
```
ERROR: logs/bot_analista.log crece demasiado (>100MB)

CAUSA: Sin rotación de logs
SOLUCIÓN:
  1. En utils/logger.py:
     from logging.handlers import RotatingFileHandler
     handler = RotatingFileHandler(
         log_path,
         maxBytes=10_000_000,  # 10MB
         backupCount=5
     )
  
  2. O limpiar manualmente:
     rm logs/bot_analista.log
```

---

## PARTE 3: CHECKLIST DE DEBUGGING

### 📋 Cuando algo no funciona, seguir este orden:

```
1. ¿Hay errores en consola?
   → Leer el traceback completamente
   → Copiar último error

2. ¿Hay logs en logs/bot_analista.log?
   → Get-Content logs/bot_analista.log -Tail 100
   → Buscar ERROR o WARNING

3. ¿Configuración correcta?
   → python -c "from config.settings import settings; print(settings.mostrar_configuracion())"

4. ¿Venv activo?
   → (venv) debe aparecer en prompt
   → Si no: .\venv\Scripts\Activate.ps1

5. ¿Dependencias instaladas?
   → pip list | grep telegram
   → pip list | grep pandas

6. ¿Token y API keys válidas?
   → No copiar con espacios
   → No tener comentarios en .env

7. ¿Permisos de archivo?
   → data/ debe tener permisos de lectura/escritura
   → logs/ debe existir

8. ¿Firewall/Red?
   → ¿Conexión a internet?
   → ¿proxy configurado?

9. ¿Código tiene errores de lógica?
   → Testear módulos individually
   → python -c "from cerebro.knowledge_manager import knowledge_manager; print('OK')"

10. ¿Hay múltiples instancias?
    → ps aux | grep python (Linux/Mac)
    → Get-Process python (Windows)
    → Detener todas
```

---

## PARTE 4: HERRAMIENTAS DE DEBUGGING

### Herramienta 1: Test de Conectividad

```python
# test_conectividad.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import logger

print("\n" + "="*60)
print("TEST DE CONECTIVIDAD")
print("="*60)

# Test 1: Configuración
print("\n1. Configuración")
try:
    settings.validar_configuracion()
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 2: Logger
print("\n2. Logger")
try:
    logger.info("Test de logger")
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 3: Base de datos
print("\n3. Base de datos")
try:
    from cerebro.knowledge_manager import knowledge_manager
    knowledge_manager.buscar_conocimiento("test")
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 4: Telegram
print("\n4. Telegram")
try:
    from telegram import Bot
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    me = bot.get_me()
    print(f"   ✅ OK - Bot: {me.username}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

# Test 5: Gemini
print("\n5. Gemini")
try:
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "="*60)
```

### Herramienta 2: Limpieza de Sistema

```bash
# cleanup.ps1
Write-Host "🧹 Limpiando sistema..."

# Eliminar cache de Python
Remove-Item -Recurse -Force "__pycache__" -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include "__pycache__" -Recurse -Force | Remove-Item -Recurse -Force

# Eliminar pyc
Get-ChildItem -Path . -Include "*.pyc" -Recurse | Remove-Item -Force

# Limpiar BD si es necesario
# Remove-Item "data/bot_database.db" -Force -ErrorAction SilentlyContinue

Write-Host "✅ Sistema limpio"
```

### Herramienta 3: Monitor de Rendimiento

```python
# monitor.py
import psutil
import time
from datetime import datetime

print("\n" + "="*60)
print("MONITOR DE RECURSOS")
print("="*60)

proceso = psutil.Process()

while True:
    cpu = proceso.cpu_percent(interval=1)
    memoria = proceso.memory_info().rss / 1024 / 1024  # MB
    
    print(f"{datetime.now().strftime('%H:%M:%S')} | "
          f"CPU: {cpu:5.1f}% | MEM: {memoria:6.1f}MB")
    
    time.sleep(5)
```

---

## PARTE 5: FLUJO DE RESOLUCIÓN PARA ERRORES COMUNES

```
┌─────────────────────────────────────┐
│ Se detiene o no inicia el bot       │
└────────────┬────────────────────────┘
             │
      ┌──────┴───────┐
      │              │
   TIMEOUT      EXCEPCIÓN
      │              │
      ▼              ▼
  ¿Datos?      ¿Qué error?
   Lento │        │
         │        └────────────────────┐
         │                             │
         ▼                             ▼
   ┌─────────┐              ┌──────────────┐
   │ Async   │              │ Que tipo?    │
   │ await   │              └──────┬───────┘
   │         │                     │
   │ Timeout │              ┌──────┴──────────────┐
   │         │              │                     │
   └─────────┘         ModuleError           TokenError
                            │                     │
                            ▼                     ▼
                        pip install          .env válido?
                        requirements         Regenerar token
```

---

## PARTE 6: TABLA DE CÓDIGOS DE ERROR

| Código | Significado | Solución |
|--------|------------|----------|
| 401 | Unauthorized (Telegram) | Token inválido/expirado |
| 400 | Bad request | Token/API mal formateado |
| 429 | Rate limited | Esperar, demasiadas requests |
| 500 | Server error | Problema en servidor API |
| ModuleNotFoundError | Falta librería | pip install [librería] |
| PermissionError | Sin permisos | Verificar permisos de archivo |
| TimeoutError | Operación lenta | Aumentar timeout |
| ConnectionError | Sin internet | Verificar conexión |

---

## PARTE 7: GUÍA RÁPIDA DE COMANDOS ÚTILES

```bash
# Ver qué Python se está usando
python -c "import sys; print(sys.executable)"

# Ver todas las dependencias instaladas
pip list

# Ver qué módulos se usan
python -m modulefinder main.py

# Generar requirements.txt
pip freeze > requirements.txt

# Ver variables de entorno
python -c "import os; [print(k,v) for k,v in os.environ.items() if 'TELEGRAM' in k]"

# Probar conexión a Telegram
python -c "from telegram import Bot; print(Bot('TOKEN').get_me())"

# Ejecutar bot con debug
python -X dev main.py

# Ver logs en vivo
Get-Content logs/bot_analista.log -Wait

# Contar líneas de código
Get-ChildItem -Recurse -Include "*.py" | Measure-Object -Line

# Encuentre todas las excepciones no capturadas
grep -r "except:" . --include="*.py"
```

---

## 📞 RESUMEN DE SOPORTE

### Si nada funciona:
1. ✅ Verificar configuración (.env)
2. ✅ Reinstalar dependencias: `pip install -r requirements.txt`
3. ✅ Limpiar caché: `./cleanup.ps1`
4. ✅ Ejecutar test: `python test_conectividad.py`
5. ✅ Revisar logs: `Get-Content logs/bot_analista.log`
6. ✅ Reiniciar venv: `.\venv\Scripts\Activate.ps1`
7. ✅ Reiniciar PC (último recurso)

### Información a tener lista si pides ayuda:
- Output completo del error (traceback)
- Primeras 50 líneas de logs
- Versión de Python: `python --version`
- Sistema operativo: `Get-ComputerInfo | select @{N=\"OS\";E={$_.OsName}}`
- Resultado de: `python test_conectividad.py`

---

