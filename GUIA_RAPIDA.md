# 🚀 GUÍA RÁPIDA - CÓMO EJECUTAR EL BOT

## ⚡ Inicio Rápido (30 segundos)

### Opción 1: Script Automatizado (RECOMENDADO)
```powershell
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
powershell -NoProfile -ExecutionPolicy Bypass -File run_bot.ps1
```

**El bot debería mostrar:**
```
✅ Bot en funcionamiento. Presiona Ctrl+C para detener.
```

### Opción 2: Manual (si la opción 1 falla)
```powershell
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
.\venv_bot\Scripts\Activate.ps1
python main.py
```

---

## 📱 Usar el Bot en Telegram

### Paso 1: Abrir Telegram
1. Abre la app de Telegram
2. Busca el bot por su nombre (@Bot_Analista_A&C o similar)
3. O accede directamente con el token

### Paso 2: Comandos Disponibles

#### `/start` - Iniciar conversación
```
Usuario: /start
Bot: Bienvenido al Bot Analista A&C...
```

#### `/ayuda` - Ver lista de comandos
```
Usuario: /ayuda
Bot: Comandos disponibles:
- /start: Iniciar
- /status: Ver estado
- /razonar: Usar IA
- ...
```

#### `/status` - Ver estado del bot
```
Usuario: /status
Bot: Estado actual:
- Bot: ✅ Operativo
- Base de datos: ✅ Conectada
- IA Gemini: ✅ Disponible
```

#### `/estadisticas` - Ver datos cargados
```
Usuario: /estadisticas
Bot: 📊 Estadísticas:
- Documentos: 3
- Conocimientos: 3
- Análisis realizados: 0
```

#### `/razonar` - Usar IA para preguntas
```
Usuario: /razonar ¿Cuáles son las mejores estrategias de trading?
Bot: Basándome en el conocimiento de los PDFs cargados...
[Respuesta generada por Gemini]
```

#### `/cargar_pdfs` - Cargar nuevos PDFs
```
Usuario: /cargar_pdfs
Bot: Buscando PDFs en carpeta pdfs/...
Documentos cargados: X
```

---

## 🔧 Requisitos

### Archivo .env
Debe existir en la raíz del proyecto:
```
TELEGRAM_TOKEN=8065924513:ABE...
GOOGLE_API_KEY=AIzaSyCMXs...
```

### Carpeta pdfs/
Coloca tus archivos PDF aquí:
```
pdfs/
├── Los magos del trading PDF .pdf
├── Trading al día.pdf
└── TRADING EN LA ZONA.pdf
```

### Virtual Environment
Debe estar creado en `venv_bot/`:
```
venv_bot/
├── Scripts/
├── Lib/
└── pyvenv.cfg
```

---

## ⚠️ Solucionar Problemas

### Error: "ModuleNotFoundError"
**Solución:**
```powershell
.\venv_bot\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
python main.py
```

### Error: "TELEGRAM_TOKEN not found"
**Solución:**
1. Verificar que existe archivo `.env`
2. Verificar que tiene: `TELEGRAM_TOKEN=...`
3. Verificar que no está vacío

### Error: "GOOGLE_API_KEY not found"
**Solución:**
1. Verificar `.env` tiene `GOOGLE_API_KEY=...`
2. Generar nueva key en: https://aistudio.google.com
3. Actualizar `.env`

### El bot se congela
**Solución:**
```powershell
# Detener todos los procesos Python
Get-Process python | Stop-Process -Force

# Reiniciar
powershell -NoProfile -ExecutionPolicy Bypass -File run_bot.ps1
```

### Base de datos corrupta
**Solución:**
```powershell
# Respaldar BD antigua
mv data/memory.db data/memory.db.backup

# Recargar PDFs
.\venv_bot\Scripts\Activate.ps1
python cargar_libros.py
```

---

## 📊 Monitoreo

### Ver logs
```powershell
Get-Content logs/bot.log -Tail 50
```

### Verificar proceso
```powershell
Get-Process python | Where-Object {$_.ProcessName -eq "python"}
```

### Ver tamaño de BD
```powershell
(Get-Item data/memory.db).Length / 1MB
```

---

## 📝 Información Técnica

### Ubicación del Proyecto
```
C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C
```

### Archivos Importantes
- `main.py` - Punto de entrada
- `run_bot.ps1` - Script para ejecutar
- `.env` - Configuración (credenciales)
- `data/memory.db` - Base de datos
- `logs/bot.log` - Archivo de logs
- `pdfs/` - Carpeta de PDFs

### Estructura del Código
```
cerebro/           ← Gestión de conocimiento
analisis/          ← Motor de análisis
ia/                ← IA (Gemini)
telegram_bot/      ← Bot de Telegram
config/            ← Configuración
utils/             ← Utilidades
data/              ← Base de datos
logs/              ← Registros
pdfs/              ← Documentos
```

---

## 🧪 Ejecutar Pruebas

### Todas las pruebas
```powershell
.\venv_bot\Scripts\Activate.ps1

# Core tests
python test_bot.py

# Telegram tests
python test_telegram_integration.py

# Stress tests
python test_stress.py
```

### Resultado esperado
```
RESULTADO FINAL: 6/6 pruebas exitosas (100%)
🎉 ¡TODOS LOS TESTS PASARON!
```

---

## 💾 Backups

### Crear backup de BD
```powershell
Copy-Item data/memory.db "data/memory_$(Get-Date -f 'yyyy-MM-dd_HH-mm-ss').db.backup"
```

### Crear backup de config
```powershell
Copy-Item .env ".env.backup"
```

---

## 🔐 Seguridad

### ⚠️ NUNCA hagas esto:
- ❌ Commitear `.env` a Git
- ❌ Compartir TELEGRAM_TOKEN
- ❌ Compartir GOOGLE_API_KEY
- ❌ Dejar credenciales en código

### ✅ Haz esto:
- ✅ Proteger `.env` en `.gitignore`
- ✅ Usar variables de entorno
- ✅ Rotar tokens periódicamente
- ✅ Monitorear acceso a logs

---

## 📞 Contacto y Soporte

Si tienes problemas:

1. **Verificar logs:**
   ```powershell
   Get-Content logs/bot.log | Select-String "ERROR" | Tail -10
   ```

2. **Revisar README.md:**
   ```powershell
   Get-Content README.md
   ```

3. **Ejecutar tests:**
   ```powershell
   python test_bot.py
   ```

4. **Revisar REPORTE_PRUEBAS.md** para más detalles

---

## 🎯 Next Steps

1. ✅ Ejecutar bot: `run_bot.ps1`
2. ✅ Abre Telegram y busca el bot
3. ✅ Escribe `/start`
4. ✅ Prueba comandos: `/status`, `/razonar ¿tu pregunta?`
5. ✅ Disfruta de análisis inteligentes con IA 🚀

---

**¡El bot está listo para usar! Cualquier duda, revisa los logs en `logs/bot.log`**

Última actualización: 24 de Noviembre de 2025
