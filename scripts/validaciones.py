# Funcion creada para validar los formatos de cuit.
def validar_cuit(cuit):

    # En el caso en que el usuario ingrese datos que no sean estrictamente digitos, retornará Falso como valor.
    if not cuit.isdigit():
        return False

    # Tambien retornará Falso si el cuit ingresado no contiene exactamenete 11 caracteres.
    if len(cuit) != 11:
        return False

    return True