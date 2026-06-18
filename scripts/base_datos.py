import sqlite3  # Libreria que nos permite integrar una base de datos local, ligera y basada en archivos directamente en nuestro código


def existe_proveedor(cuit):

    conexion = sqlite3.connect("../base_datos/proveedores.db")

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

    conexion = sqlite3.connect("../base_datos/proveedores.db")

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