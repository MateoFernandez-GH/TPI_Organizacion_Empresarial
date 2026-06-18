import sqlite3  # Libreria que nos permite integrar una base de datos local, ligera y basada en archivos directamente en nuestro código
import os

# Construimos la ruta absoluta de la base de datos dinamicamente
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "base_datos", "proveedores.db")

def existe_proveedor(cuit):

    conexion = sqlite3.connect(DB_PATH)

    # Utilizamos el metodo .cursor() para poder relacionarnos con nuestra base de datos.
    cursor = conexion.cursor()

    # El metodo .excecute() nos permite indicar los comandos SQL que necesitamos realizar sobre la base de datos, para extrear en proveedro 
    # correspondiente al cuit ingresado en la funcion como argumento.
    cursor.execute(
        """
        SELECT cuit
        FROM proveedores
        WHERE cuit = ?
        """,
        (cuit,)
    )

    resultado = cursor.fetchone() # Con este metodo recuperamos los datos en forma de fila, guardandolos en la variable resultado.

    conexion.close()

    # En caso el resultado "no sea Falso", y por lo tanto, no esté vacio y haya efectivamente encotrado datos coincidentes, procede a retornarlo. 
    return resultado is not None

# Creamos una base de datos en nuestro archivo "proveedores.db"
def crear_base_datos():

    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            cuit TEXT PRIMARY KEY,
            razon_social TEXT,
            email TEXT,
            telefono TEXT,
            rubro TEXT,
            cbu TEXT
        )
    """)

    conexion.commit()
    conexion.close()


# Creamos una funcion para que inserte datos de prueba en la base de datos, y podamos empezar a simular el funcionamiento correcot
def cargar_datos_prueba():

    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO proveedores
        VALUES (
            '30712345678',
            'Proveedor Uno SA',
            'contacto@proveedor1.com',
            '3815551111',
            'Tecnologia',
            '2850590940090418135201'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO proveedores
        VALUES (
            '30698765432',
            'Servicios del Norte SRL',
            'info@norte.com',
            '3815552222',
            'Servicios',
            '2850590940090418135202'
        )
    """)

    conexion.commit()
    conexion.close()


# Funcion para guardar un nuevo proveedor en la base de datos
def guardar_proveedor(cuit, razon_social, email, telefono, rubro, cbu):

    conexion = sqlite3.connect(DB_PATH)

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO proveedores
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cuit, razon_social, email, telefono, rubro, cbu))

    conexion.commit()
    conexion.close()