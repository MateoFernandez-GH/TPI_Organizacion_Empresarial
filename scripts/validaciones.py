import re


# Funcion creada para validar los formatos de cuit.
def validar_cuit(cuit):

    # En el caso en que el usuario ingrese datos que no sean estrictamente digitos, retornará Falso como valor.
    if not cuit.isdigit():
        return False

    # Tambien retornará Falso si el cuit ingresado no contiene exactamenete 11 caracteres.
    if len(cuit) != 11:
        return False

    return True


# Valida formato de email usando una expresión regular simple
def validar_email(email):
    if not isinstance(email, str):
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# Valida telefono: al menos 10 dígitos (acepta guiones/espacios y extrae dígitos)
def validar_telefono(telefono):
    if not isinstance(telefono, str):
        return False
    digits = ''.join(ch for ch in telefono if ch.isdigit())
    return len(digits) >= 10


# Valida CBU: debe contener exactamente 22 dígitos (acepta formateos con espacios/guiones)
def validar_cbu(cbu):
    if not isinstance(cbu, str):
        return False
    digits = ''.join(ch for ch in cbu if ch.isdigit())
    return len(digits) == 22