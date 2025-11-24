# 🔧 OPCIONES PARA RESOLVER EL ERROR DE CUOTA

## 🎯 La Mejor Solución: Plan Pago de Google (RECOMENDADO)

### Paso 1: Crear proyecto en Google Cloud
```
https://console.cloud.google.com/
```

### Paso 2: Habilitar Gemini API
- Busca "Google AI Studio" 
- Habilita la API
- Crea credenciales

### Paso 3: Obtener API Key
- Ve a: https://ai.google.dev
- Crea una nueva API key
- Vinculada a tu proyecto de pago

### Paso 4: Actualizar .env
```
GOOGLE_API_KEY=tu_nueva_api_key_con_cuota_paga
```

### Paso 5: Reiniciar bot
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File run_bot.ps1
```

---

## ✅ Alternativa 1: Usar OpenAI (Si tienes créditos)

### Paso 1: Obtener API Key de OpenAI
```
https://platform.openai.com/account/api-keys
```

### Paso 2: Actualizar .env
```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=  # Puede quedar vacía
```

### Paso 3: Cambiar ai_engine.py
En `ia/ai_engine.py`, cambiar:
```python
# Línea 62
modelo = "gpt-4-turbo"  # o gpt-3.5-turbo para más rápido
```

### Paso 4: Ejecutar bot
```powershell
.\venv_bot\Scripts\Activate.ps1
python main.py
```

---

## ✅ Alternativa 2: Esperar y Reintentar (GRATUITO)

Google renovará tu cuota gratuita en poco tiempo.

**Timing:**
- Cuotas se renuevan cada **60 segundos**
- Máximo: 60 solicitudes por minuto
- Máximo: 1,000 tokens de entrada por minuto

**Prueba:**
```powershell
# Espera 2 minutos
Start-Sleep -Seconds 120

# Vuelve a ejecutar
.\run_bot.ps1
```

---

## ✅ Alternativa 3: Usar Modelo Más Ligero (GRATUITO)

Cambia a `gemini-1.5-flash` (menos consumo de tokens):

**En config/settings.py, línea 32:**
```python
GEMINI_MODEL = "gemini-1.5-flash"
```

Este modelo es:
- ✅ 60% más rápido
- ✅ Usa 70% menos tokens
- ✅ Mantiene buena calidad para trading

---

## 📊 Comparación de Opciones

| Opción | Costo | Tiempo | Limitaciones |
|--------|------|--------|--------------|
| **Plan Pago** | $5-20/mes | Inmediato | Ninguna |
| **OpenAI** | Depende créditos | Inmediato | Requiere otra API |
| **Esperar** | Gratis | 1-2 min | Limitado por hora |
| **Modelo Ligero** | Gratis | Inmediato | Menos potente |

---

## 🚀 Mi Recomendación

Para **producción y sin límites**: Plan pago de Google AI Studio (es el más barato)

Para **pruebas**: Espera 2 minutos y vuelve a intentar

Para **alternativa rápida**: Usa gemini-1.5-flash (modelo más ligero)

---

## 📞 Soporte

Si necesitas ayuda:
1. Verifica GOOGLE_API_KEY en .env
2. Confirma que el proyecto tiene plan de pago vinculado
3. Prueba con una pregunta simple
4. Revisa logs en `logs/bot.log`
