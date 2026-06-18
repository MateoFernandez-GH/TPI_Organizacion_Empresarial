# En este archivo, definimos los estados coincidentes con nuestra "maquina de estados", de los cuales se va a valer el programa para cumplir 
# con su condicion de "estado unico".

INICIO = 1

SOLICITAR_CUIT = 2

VALIDACION_CUIT = 3

CONSULTAR_DUPLICADO = 4

FIN_RECHAZADA = 5  # Estado en el que el sistema corta su ejecucion, rechazando el proceso de carga del usuario.

SOLICITAR_RAZON_SOCIAL = 6

SOLICITAR_EMAIL = 7

VALIDACION_EMAIL = 8

SOLICITAR_TELEFONO = 9 

VALIDACION_TELEFONO = 10

SOLICITAR_RUBRO = 11

SOLICITAR_CBU = 12 

VALIDACION_CBU = 13

REGISTRO_COMPLETO = 14

FIN_APROBADA = 15

