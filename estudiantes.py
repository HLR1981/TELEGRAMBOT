import sqlite3
import re  # Para validación de correo

# Conexión y creación de tabla
conn = sqlite3.connect("alumnos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    correo TEXT
)
""")
conn.commit()

# Función para validar correos
def correo_valido(correo):
    if ' ' in correo:
        return False
    if '..' in correo:
        return False
    if re.search(r"[<>(){}\[\];:,]", correo):
        return False
    if not re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", correo):
        return False
    parte_local = correo.split('@')[0]
    if len(parte_local) < 3:
        return False
    return True

# Funciones principales
def agregar_estudiante(nombre, edad, correo):
    if not correo_valido(correo):
        print("Correo inválido. Intenta nuevamente.")
        return
    cursor.execute("INSERT INTO estudiantes (nombre, edad, correo) VALUES (?, ?, ?)", (nombre, edad, correo))
    conn.commit()
    print("Estudiante agregado correctamente.")

def mostrar_estudiantes():
    cursor.execute("SELECT * FROM estudiantes")
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)

def buscar_por_nombre(nombre):
    cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ?", ('%' + nombre + '%',))
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)

def eliminar_estudiante():
    mostrar_estudiantes()
    try:
        id_borrar = int(input("ID del estudiante a eliminar: "))
        cursor.execute("SELECT * FROM estudiantes WHERE id = ?", (id_borrar,))
        estudiante = cursor.fetchone()
        if estudiante:
            confirmar = input(f"¿Estás seguro de eliminar a {estudiante[1]}? (s/n): ")
            if confirmar.lower() == 's':
                cursor.execute("DELETE FROM estudiantes WHERE id = ?", (id_borrar,))
                conn.commit()
                print("Estudiante eliminado.")
            else:
                print("Eliminación cancelada.")
        else:
            print("No se encontró un estudiante con ese ID.")
    except ValueError:
        print("ID inválido.")

# Menú principal
while True:
    print("\n1. Agregar estudiante\n2. Mostrar todos\n3. Buscar por nombre\n4. Eliminar estudiante\n5. Salir")
    op = input("Elige una opción: ")

    if op == '1':
        nombre = input("Nombre: ")
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida.")
            continue
        correo = input("Correo: ")
        agregar_estudiante(nombre, edad, correo)

    elif op == '2':
        mostrar_estudiantes()

    elif op == '3':
        nombre = input("Nombre a buscar: ")
        buscar_por_nombre(nombre)

    elif op == '4':
        eliminar_estudiante()

    elif op == '5':
        break

    else:
        print("Opción no válida.")

# Cierre de conexión
conn.close()





