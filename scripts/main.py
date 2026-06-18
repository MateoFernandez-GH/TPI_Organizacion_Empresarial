#Este es el archvio del programa principal, desde donde se ejecutarán los procesos principales.

#Importamos las bibliotecas necesarias para intercomunicar nuestro codigo con el Bot creado en Telegram.
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from validaciones import validar_cuit, validar_email, validar_telefono, validar_cbu
from base_datos import existe_proveedor, crear_base_datos, cargar_datos_prueba, guardar_proveedor
import os 
from dotenv import load_dotenv
from estados import *


#=======================================================================================================================================#
# Carga las variables de entorno desde .env
load_dotenv()

# Lee el token desde la variable de entorno, de manera Segura - sin riesgos de exponerlo
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Incluimos un "manejador de comandos" asincronico (para que el bot pueda manejar multiples usuarios simultaneamente sin
# bloquear la ejecucion ) para dar la buenvenida al Usuario con el que interactuamos...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["estado"] = ESTADO_ESPERANDO_CUIT

    await update.message.reply_text(
        "Bienvenido al Sistema de Alta de Proveedores.\n\nIngrese su CUIT:"
    )

# Funcion para recibir mensajes, cambiar los estados del programa, y segun ellos, imprimir un mensaje u otro.
async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):

    estado = context.user_data.get("estado")

    mensaje = update.message.text

    if estado == ESTADO_ESPERANDO_CUIT:
        if not validar_cuit(mensaje):
            await update.message.reply_text("CUIT inválido. Intente nuevamente:")
        elif existe_proveedor(mensaje):
            await update.message.reply_text("El CUIT ya se encuentra registrado. Ingrese otro CUIT:")
            context.user_data["estado"] = ESTADO_ESPERANDO_CUIT
        else:
            await update.message.reply_text("CUIT válido. Proveedor no registrado.\n\nIngrese Razon Social:")
            context.user_data["cuit"] = mensaje
            context.user_data["estado"] = ESTADO_ESPERANDO_RAZON_SOCIAL

    elif estado == ESTADO_ESPERANDO_RAZON_SOCIAL:
        await update.message.reply_text("Ingrese Email:")
        context.user_data["razon_social"] = mensaje
        context.user_data["estado"] = ESTADO_ESPERANDO_EMAIL

    elif estado == ESTADO_ESPERANDO_EMAIL:
        if not validar_email(mensaje):
            await update.message.reply_text("Email inválido. Ingrese Email válido:")
            context.user_data["estado"] = ESTADO_ESPERANDO_EMAIL
        else:
            context.user_data["email"] = mensaje
            await update.message.reply_text("Ingrese Telefono:")
            context.user_data["estado"] = ESTADO_ESPERANDO_TELEFONO

    elif estado == ESTADO_ESPERANDO_TELEFONO:
        if not validar_telefono(mensaje):
            await update.message.reply_text("Teléfono inválido. Debe contener al menos 10 dígitos. \n\nIngrese Teléfono:")
            context.user_data["estado"] = ESTADO_ESPERANDO_TELEFONO
        else:
            context.user_data["telefono"] = mensaje
            await update.message.reply_text("Ingrese Rubro:")
            context.user_data["estado"] = ESTADO_ESPERANDO_RUBRO

    elif estado == ESTADO_ESPERANDO_RUBRO:
        context.user_data["rubro"] = mensaje
        context.user_data["estado"] = ESTADO_ESPERANDO_CBU
        await update.message.reply_text("Ingrese CBU:")

    elif estado == ESTADO_ESPERANDO_CBU:
        if not validar_cbu(mensaje):
            await update.message.reply_text("CBU inválido. Ingrese CBU válido (22 dígitos):")
            context.user_data["estado"] = ESTADO_ESPERANDO_CBU
        else:
            context.user_data["cbu"] = mensaje
            guardar_proveedor(
                context.user_data["cuit"],
                context.user_data["razon_social"],
                context.user_data["email"],
                context.user_data["telefono"],
                context.user_data["rubro"],
                context.user_data["cbu"]
            )
            await update.message.reply_text(f"""¡Proveedor registrado exitosamente!
Estamos felices de empezar a trabajar juntos 💪🏻 \n\nMuchos Exitos {context.user_data["razon_social"]}!""")
            context.user_data["estado"] = ESTADO_FINALIZADO

    else:
        await update.message.reply_text("Estado no reconocido.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,recibir_mensaje))



# Ejecutamos la creacion de la base de datos de la que se va a valer el bot
crear_base_datos()
# Ejecutamos la carga de datos prueba a insertar en la base de datos para la simulacion del funcionamiento del bot
cargar_datos_prueba()

print("Bot iniciado...")


# Ejecutamos una funcion que inicia el bot y lo mantiene ejecutándose continuamente escuchando mensajes de los usuarios.
app.run_polling()