# 🚀 INICIO RÁPIDO - Bot Analista A&C

## ⚡ En 5 Minutos

### 1️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Configurar Token
```bash
# Opción A: Ejecutar setup interactivo
python setup.py

# Opción B: Manual - Crear archivo .env
TELEGRAM_TOKEN=tu_token_aqui
```

### 3️⃣ Agregar PDFs (Opcional)
```bash
# Coloca tus PDFs en:
pdfs/
```

### 4️⃣ Ejecutar Bot
```bash
python main.py
```

### 5️⃣ Usar en Telegram
```
/start          ← Comienza aquí
/ayuda          ← Ver comandos
/cargar_pdfs    ← Entrenar cerebro
/analizar       ← Realizar análisis
```

---

## 📚 Documentación Completa

| Documento | Contenido |
|-----------|----------|
| `GUIA_COMPLETA.md` | Guía exhaustiva con ejemplos |
| `ARQUITECTURA.md` | Diseño técnico del sistema |
| `README.md` | Descripción general |

---

## 🔑 Obtener Token de Telegram

1. Abre Telegram
2. Busca **@BotFather**
3. Escribe `/newbot`
4. Sigue instrucciones
5. Copia el token
6. Pégalo en `.env`

---

## 📂 Estructura Rápida

```
Bot_Analist_A&C/
├── cerebro/          (🧠 Base de datos de conocimiento)
├── analisis/         (📊 Motor de análisis)
├── telegram_bot/     (🤖 Bot)
├── utils/            (🔧 Utilidades)
├── config/           (⚙️ Configuración)
├── pdfs/             (📚 Tus documentos aquí)
├── data/             (💾 Base de datos)
└── logs/             (📝 Logs)
```

---

## 🎯 Características Principales

✅ **Cerebro Inteligente** - Aprende de PDFs  
✅ **Análisis de Datos** - Financiero y general  
✅ **Visión Computacional** - Analiza imágenes  
✅ **OCR** - Extrae texto de fotos  
✅ **Aprendizaje Continuo** - Mejora con uso  
✅ **Base de Datos** - Histórico y estadísticas  
✅ **100% Modular** - Fácil de expandir  

---

## 🐛 Troubleshooting

### No funciona el token
```bash
# Verifica archivo .env existe
# Revisa que no tenga espacios extras
cat .env
```

### Módulo no encontrado
```bash
# Reactiva entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstala
pip install -r requirements.txt
```

### El bot no responde
```bash
# Revisa logs
tail -f logs/bot_analista.log
```

---

## 📊 Ejemplo de Uso

### Análisis de Datos
```json
{
    "tendencia": "al_alza",
    "volatilidad": 0.15,
    "valores": [100, 105, 110, 115]
}
```

### Análisis de Imagen
- Envía una foto de gráfica
- El bot extrae: texto, tipo, colores, formas

### Búsqueda
- Escribe una pregunta
- Bot busca en su cerebro (PDFs)

---

## 📞 Comandos del Bot

```
/start              - Inicia el bot
/ayuda              - Ver comandos
/status             - Estado actual
/cargar_pdfs        - Entrenar cerebro
/analizar           - Modo análisis
/estadisticas       - Ver métricas
```

---

## 🔗 Enlaces Útiles

- [Telegram BotFather](https://t.me/BotFather)
- [Docs python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Tutorial SQLite](https://www.sqlite.org/docs.html)

---

## 💡 Próximos Pasos

1. Familiarizarse con comandos básicos
2. Agregar PDFs para entrenar
3. Hacer análisis de ejemplo
4. Personalizar según necesidades
5. Expandir con nuevas funciones

---

## 🎉 ¡Listo!

Tu bot está configurado. 

**En Telegram escribe: `/start`**

¡Comenzamos! 🚀

---

## 📧 Soporte

Si tienes problemas:
1. Revisa `GUIA_COMPLETA.md`
2. Verifica `logs/bot_analista.log`
3. Ejecuta `python test_example.py`

**¡Éxito con tu Bot Analista!** 🤖💪
