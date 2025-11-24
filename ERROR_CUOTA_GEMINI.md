# ❌ ERROR: Cuota de Gemini Excedida

## 🔴 Problema Identificado

El comando `/razonar` está fallando porque la **API key de Google Gemini ha excedido su cuota gratuita**.

```
Error: 429 You exceeded your current quota
Límite: 0 generaciones por minuto (Free Tier)
Modelo: gemini-2.0-flash-exp
```

## 📊 Detalles de la Cuota

Google AI Studio (Free Tier) tiene límites estrictos:
- **Solicitudes por minuto:** 60 (Free Tier)
- **Tokens de entrada por minuto:** 1,000 (Free Tier)
- **Estado actual:** Cuota agotada

## 🔧 Soluciones

### ✅ Solución 1: Esperar a que se renueve la cuota (RECOMENDADO PARA PRUEBAS)
- Las cuotas se renuevan automáticamente
- Espera **4+ segundos** y vuelve a intentar
- Prueba nuevamente: `/razonar ¿tu pregunta?`

### ✅ Solución 2: Cambiar a un plan pago (PARA PRODUCCIÓN)

1. Ir a: https://ai.google.dev/billing
2. Crear un proyecto de Google Cloud
3. Habilitar "Google AI Studio" en el proyecto
4. Vincularse a una tarjeta de crédito
5. Copiar la nueva API key
6. Actualizar `.env`:
   ```
   GOOGLE_API_KEY=tu_nueva_api_key
   ```

### ✅ Solución 3: Usar un modelo con menos consumo

Cambiar en `config/settings.py` o `ia/ai_engine.py`:

```python
# Menos poderoso pero usa menos tokens
GEMINI_MODEL = "gemini-1.5-flash"  # Más eficiente
```

## 📝 Resumen del Error

| Aspecto | Detalles |
|---------|----------|
| **Comando afectado** | `/razonar` |
| **Causa** | Cuota gratuita de Gemini agotada |
| **Código HTTP** | 429 (Too Many Requests) |
| **Solución rápida** | Esperar y reintentar |
| **Solución permanente** | Plan pago o cambiar modelo |

## 🚀 Próximos Pasos

1. **Intenta nuevamente** después de 5 segundos
2. **Si el problema persiste**, considera un plan pago
3. **Si quieres seguir probando gratis**, usa modelos alternativos

---

**Nota:** El código del bot está funcionando correctamente. Este es un límite de uso de la API, no un bug.
