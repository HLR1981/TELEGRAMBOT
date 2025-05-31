import sqlite3
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# === Cargar variables de entorno (.env) ===
load_dotenv()
# Asegúrate de tener "token=TU_TOKEN" en tu archivo .env
BOT_TOKEN = os.getenv("token")

# === Inicializar base de datos SQLite ===
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INTEGER PRIMARY KEY,
            nombre TEXT
        )
    ''')
    conn.commit()
    conn.close()

# === Guardar usuario ===
def guardar_usuario(user_id, nombre):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO usuarios (user_id, nombre) VALUES (?, ?)", (user_id, nombre))
    conn.commit()
    conn.close()

# === Obtener todos los usuarios registrados ===
def obtener_usuarios():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM usuarios")
    usuarios = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usuarios

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    guardar_usuario(user.id, user.full_name)
    print(f"Nuevo usuario registrado: {user.id} - {user.full_name}")
    await update.message.reply_text("👋 Te has registrado para recibir mensajes del bot.")

# === /notificar ===
async def notificar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != 6006164397:
        await update.message.reply_text("⛔ No tienes permiso para usar este comando.")
        return

    mensaje = ' '.join(context.args) or "📢 Este es un mensaje de prueba."
    usuarios = obtener_usuarios()
    enviados = 0
    for user_id in usuarios:
        try:
            await context.bot.send_message(chat_id=user_id, text=mensaje)
            enviados += 1
        except Exception as e:
            print(f"No se pudo enviar mensaje a {user_id}: {e}")
    await update.message.reply_text(f"✅ Mensaje enviado a {enviados} usuario(s).")

# === Main ===
def main():
    print("Iniciando el bot...")

    # Validar que el token exista
    if not BOT_TOKEN:
        raise ValueError("❌ No se encontró el token. Asegúrate de que el archivo .env tenga: token=TU_TOKEN")

    init_db()

    # Crear la aplicación de Telegram
    app = Application.builder().token(BOT_TOKEN).build()

    # Registrar comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notificar", notificar))

    # Iniciar el bot
    app.run_polling()

if __name__ == "__main__":
    main()
    
