import sqlite3


# Función para crear la tabla de carros
def crear_tabla_carros():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Crear la tabla "carros" si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT UNIQUE,
        color TEXT,
        cantidad INTEGER
    )""")

    conn.commit()
    conn.close()


# Función para insertar carros en la base de datos
def insertar_carros():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    # Lista de carros para insertar en la base de datos
    carros = [
        ("Nissan", "Rojo", 8),
        ("Ford", "Blanco", 3),
        ("Toyota", "Gris", 5),
        ("Chevrolet", "Plateados", 6),
        ("Mitsubishi", "Azules", 4)
    ]

    # Insertar los carros en la tabla
    for carro in carros:
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO carros (marca, color, cantidad)
            VALUES (?, ?, ?)
            """, carro)
        except sqlite3.Error as e:
            print(f"Error al insertar {carro}: {e}")

    conn.commit()
    conn.close()


# Llamar a las funciones para crear la tabla y insertar los datos
crear_tabla_carros()
insertar_carros()
