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
from validaciones import validar_cuit
from base_datos import existe_proveedor, crear_base_datos


#=======================================================================================================================================#

# Ingresamos el Token provisto por Telegram al crear nuestro Bot
TOKEN = "8706747633:AAFFfGz2QINndaWmoJ0z8IsJEsjV3IU1GIA"

# Incluimos un "manejador de comandos" asincronico (para que el bot pueda manejar multiples usuarios simultaneamente sin
# bloquear la ejecucion ) para dar la buenvenida al Usuario con el que interactuamos...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["estado"] = "ESPERANDO_CUIT"

    await update.message.reply_text(
        "Bienvenido al Sistema de Alta de Proveedores.\n\nIngrese su CUIT:"
    )

# Funcion para recibir mensajes, cambiar los estados del programa, y segun ellos, imprimir un mensaje u otro.
async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):

    estado = context.user_data.get("estado")

    mensaje = update.message.text

    if estado == "ESPERANDO_CUIT":

        # 1er GATEWAY DE NUESTRO BPMN
        if validar_cuit(mensaje):
            if existe_proveedor(mensaje):

                await update.message.reply_text(    
                    f"El CUIT ya se encuentra registrado.\n\n Solicitud Rechazada."
                )

                context.user_data["estado"] = "FINALIZADO"
        else: 
            await update.message.reply_text( 
                "CUIT valido.\nProveedor no registrado.\n\nIngrese Razon Social: " 
                )
            context.user_data["cuit"] = mensaje
            context.user_data["estado"] = "ESPERANDO_RAZON_SOCIAL"

    else:

        await update.message.reply_text(
            "Estado no reconocido."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,recibir_mensaje))



# Ejecutamos la creacion de la base de datos de la que se va a valer el bot
crear_base_datos()

print("Bot iniciado...")


# Ejecutamos una funcion que inicia el bot y lo mantiene ejecutándose continuamente escuchando mensajes de los usuarios.
app.run_polling()