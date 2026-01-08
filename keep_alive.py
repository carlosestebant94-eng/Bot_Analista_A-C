from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "¡Estoy vivo! El bot está corriendo."

def run():
    # Escucha en el puerto 8080 o en el que Render asigne
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
