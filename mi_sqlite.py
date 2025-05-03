import sqlite3


# Función para crear tabla carros
def crear_tabla_carros():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "nombre" TEXT UNIQUE
    )
    """)
    
    conn.commit()
    conn.close()


# Función insertar carros en la base de datos
def insertar_carros():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    carros = [
        "Carros Nissan"
        "Carros Ford"
        "Carros Toyota"
        "Carros Chevrolet"
        "Carros Mitsubishi"
    ]
    
    for carro in carros:
        cursor.execute("INSERT OR IGNORE INTO carros (nombre) VALUES (?)", (carro,))
    
    conn.commit()
    conn.close()


# Función obtener carros de la base de datos
def obtener_carros():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT nombre FROM carros")
    carros = [fila[0] for fila in cursor.fetchall()]
    
    conn.close()
    return carros
