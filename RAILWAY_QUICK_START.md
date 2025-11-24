# 🚀 RAILWAY DEPLOYMENT - QUICK START

## En 3 pasos simples:

### 1️⃣ PREPARAR PROYECTO (2 min)

Ejecuta en PowerShell:
```powershell
cd "C:\Users\sk894\OneDrive\Carlos\OneDrive\Escritorio\Bot_Analist_A&C"
powershell -ExecutionPolicy Bypass -File prepare_railway_deploy.ps1
```

Esto crea un archivo `Bot_Analista_Railway.zip`

### 2️⃣ REGISTRARSE EN RAILWAY (3 min)

Ve a: https://railway.app/

- Click en "Sign Up"
- Opción: GitHub (recomendado) o Email
- Completa el registro

### 3️⃣ CREAR PROYECTO Y DEPLOY (5 min)

En Railway dashboard:

```
1. Click: "Create New Project"
2. Selecciona: "Deploy from File"
3. Drag & Drop: Bot_Analista_Railway.zip
4. Espera a que se procese
5. Click en el servicio
6. Tab: "Variables"
7. Agrega:
   - TELEGRAM_TOKEN = 8065924513:AAHcI033x83E9r2fztwWJ-EFMdgUWj4ARJI
   - GOOGLE_API_KEY = AIzaSyCMXs2CGhTgnFB6bHMxB3aDWXCH_dnDn7Y
   - LOG_LEVEL = INFO
8. Espera a que redeploy automáticamente
9. ¡Listo! Bot 24/7 ✅
```

---

## ✅ VERIFICAR QUE FUNCIONA

En Railway:
1. Ve a "Logs"
2. Busca: "Bot en funcionamiento"
3. En Telegram: `/start` a tu bot
4. Si responde, ¡está vivo! 🎉

---

## 📊 ESTADO DESPUÉS DE DEPLOY

- ✅ Bot corriendo 24/7
- ✅ Sin tu máquina encendida
- ✅ Logs en tiempo real
- ✅ Base de datos sincronizada
- ✅ PDFs disponibles

---

## 💰 COSTOS

- Primeros 5 USD: Gratis (crédito inicial)
- Después: ~$0.40/mes para este bot
- Puedes monitorear en tiempo real

---

## 🆘 SI ALGO FALLA

**El bot no responde:**
- Verifica en Railway > Logs
- Busca "ERROR"
- Comprueba TELEGRAM_TOKEN

**Error de API:**
- Confirma GOOGLE_API_KEY exacta
- Sin espacios antes/después
- Reinicia desde Railway

**No ve los logs:**
- Espera 30 segundos después de deploy
- Refresh la página
- El bot tardará en inicializar

---

**¿Listo para empezar? 🚀**
