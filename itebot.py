import importlib
import sqlite3
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler
import archivotron  
import sqlite3
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler

import menu  # Esta importación no cambiará, ya que menu.py es un archivo separado

TOKEN = "8036679211:AAHHjlFUZ4ZCPbdFAnQemL1-VkursnTGDTg"

# Función para conectar con la base de datos y crear tablas si no existen
def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    # Eliminar la tabla 'carros' si este ya existe
    cursor.execute("DROP TABLE IF EXISTS carros")
    
    # Crear la tabla de "carros" con la columna 'tipo'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        tipo TEXT,
        semestre INTEGER
    )""")
    
    # Crear las demás tablas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ayudas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra_clave TEXT UNIQUE,
        contenido TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        opciones TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS palabras_clave (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra TEXT UNIQUE,
        respuesta TEXT
    )""")
    
    conn.commit()
    conn.close()

# Función para insertar los carros en la base de datos
def insertar_carros():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Lista de carros a insertar en bd
    carros = [
        ("Carros Nissan", "Rojos", 8),
        ("Carros Ford", "Blancos", 3),
        ("Carros Toyota", "Grises", 5),
        ("Carros Chevrolet","Plateados", 6),
        ("Carros Mitsubishi", "Azules", 4),
    ]

    # Insertar los carros en la tabla
    for carro in carros:
        cursor.execute("""
        INSERT OR IGNORE INTO carros (nombre, tipo, semestre)
        VALUES (?, ?, ?)
        """, carro)

    conn.commit()
    conn.close()

# Función para insertar datos en la base de datos solo si no existen
def insertar_datos_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Insertar datos en la tabla "menus" si no existen
    cursor.execute("SELECT * FROM menus WHERE nombre = 'carros'")
    resultado = cursor.fetchone()
    if not resultado:  # Si no existe, insertamos los datos
        cursor.execute("""
        INSERT INTO menus (nombre, opciones)
        VALUES ('carros', '1. Marca de carro, 2. Color, 3. Cantidad')
        """)

    # Insertar datos en la tabla "ayudas" si no existen
    cursor.execute("SELECT * FROM ayudas WHERE palabra_clave = 'ayuda'")
    resultado = cursor.fetchone()
    if not resultado:  # Si no existe, insertamos los datos
        cursor.execute("""
        INSERT INTO ayudas (palabra_clave, contenido)
        VALUES ('ayuda', 'Este es el contenido de la ayuda.')
        """)

    # Insertar datos en la tabla "palabras_clave" si no existen
    cursor.execute("SELECT * FROM palabras_clave WHERE palabra = 'carros'")
    resultado = cursor.fetchone()
    if not resultado:  # Si no existe, insertamos los datos
        cursor.execute("""
        INSERT INTO palabras_clave (palabra, respuesta)
        VALUES ('carros', 'carros.')
        """)

    conn.commit()
    conn.close()

# Función para obtener datos de la base de datos
def obtener_datos_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT palabra_clave, contenido FROM ayudas")
    ayudas = {fila[0].lower(): fila[1] for fila in cursor.fetchall()}
    
    cursor.execute("SELECT nombre, opciones FROM menus")
    menus = {fila[0].lower(): fila[1] for fila in cursor.fetchall()}
    
    cursor.execute("SELECT palabra, respuesta FROM palabras_clave")
    palabras_clave = {fila[0].lower(): fila[1] for fila in cursor.fetchall()}
    
    cursor.execute("SELECT nombre, tipo, semestre FROM carros")
    carros = {fila[0].lower(): f"{fila[1]} - carro: {fila[2]}" for fila in cursor.fetchall()}
    
    conn.close()
    return ayudas, menus, palabras_clave, carros

# Función para consultar la base de datos manualmente
def consultar_db(tabla):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabla}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Comando para consultar la base de datos desde Telegram
async def consultar(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Uso: /consultar <nombre_tabla>")
        return
    
    tabla = context.args[0]
    resultados = consultar_db(tabla)
    
    if resultados:
        respuesta = f"Resultados de la tabla '{tabla}':\n"
        for fila in resultados:
            respuesta += f"{fila}\n"
    else:
        respuesta = f"No se encontraron datos en la tabla '{tabla}'."
    
    await update.message.reply_text(respuesta)

# Función para iniciar el bot y responder al comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Envíame un mensaje y verificaré las palabras.")

# Función para analizar el mensaje enviado por el usuario
async def analizar_mensaje(update: Update, context: CallbackContext):
    importlib.reload(archivotron)
    
    palabras_validas = archivotron.palabras_validas
    palabras_prohibidas = archivotron.palabras_prohibidas
    palabras_especiales = archivotron.palabras_especiales
    
    ayudas, menus, palabras_clave, carros = obtener_datos_db()
    
    user_text = update.message.text.lower()
    palabras = user_text.split()
    respuesta = ""
    
    # Si el usuario pregunta por "carros", se muestra los carros
    if "carros" in palabras:
        for nombre_carro, detalle in carros.items():
            respuesta += f"🚗 Carro: {nombre_carro.title()}, {detalle}\n"
    
    # Analizamos cada palabra en el mensaje del usuario
    for palabra in palabras:
        palabra_lower = palabra.lower()
        if palabra_lower in palabras_prohibidas:
            respuesta += f"⚠️ La palabra '{palabra}' está en la lista prohibida.\n"
        elif palabra_lower in palabras_especiales:
            respuesta += f"⭐ La palabra '{palabra}' está en la lista especial.\n"
        elif palabra_lower in palabras_validas:
            respuesta += f"✅ La palabra '{palabra}' está en la lista válida.\n"
        elif palabra_lower in ayudas:
            respuesta += f"📖 Ayuda sobre '{palabra}': {ayudas[palabra_lower]}\n"
        elif palabra_lower in menus:
            respuesta += f"📌 Menú '{palabra}': {menus[palabra_lower]}\n"
        elif palabra_lower in palabras_clave:
            respuesta += f"🔑 '{palabra}': {palabras_clave[palabra_lower]}\n"
        elif palabra_lower in carros: # type: ignore
            respuesta += f"🚗 Carro: '{palabra}', {carros[palabra_lower]}\n"
    
    if respuesta:
        await update.message.reply_text(respuesta)
    else:
        await update.message.reply_text("No se encontraron coincidencias en las listas ni en la base de datos.")

# Inicializamos la base de datos e insertamos datos si no existen
init_db()
insertar_datos_db()
insertar_carros() # Insertamos los carros

# Configuración del bot
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("consultar", consultar))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analizar_mensaje))

print("🤖 Bot de filtrado iniciado...")
app.run_polling()