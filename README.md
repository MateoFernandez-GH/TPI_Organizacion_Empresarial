# TPI Organización Empresarial - Sistema de Alta de Proveedores (Banco del Chubut)

Este repositorio contiene el **Trabajo Práctico Integrador (TPI)** desarrollado para la asignatura **Organización Empresarial**, correspondiente al final del primer cuatrimestre de la **Tecnicatura Universitaria en Programación a Distancia (TUPaD)** de la **Universidad Tecnológica Nacional (UTN)**.

El proyecto consiste en el diseño, modelado y desarrollo de un **Chatbot automatizado en Telegram** encargado de gestionar el proceso administrativo de **Alta y Registro de Proveedores**, enfocado institucionalmente en el **Banco del Chubut**, transformando un flujo tradicionalmente manual e ineficiente en un proceso ágil, seguro y estandarizado mediante metodologías de modelado de negocio (BPMN 2.0).

---

## 📌 1. Descripción del Proyecto

El objetivo principal es actuar como consultores tecnológicos para automatizar el alta de proveedores de la entidad financiera. El bot interactúa con el usuario de manera asincrónica, solicitando la información requerida, validando los datos en tiempo real mediante reglas de negocio estrictas, controlando duplicados contra una base de datos persistente y completando el registro de manera exitosa si se cumplen todas las condiciones del "camino feliz", o rechazando el alta en caso de inconsistencias.

---

## ⚙️ 2. Arquitectura y Stack Tecnológico

El software fue desarrollado siguiendo principios de modularización, extensibilidad y robustez, utilizando las siguientes herramientas:

* **Lenguaje de Programación:** Python 3.10+
* **Librería Principal:** `python-telegram-bot` (ApplicationBuilder v20.x, asincrónica para soporte multiusuario simultáneo).
* **Persistencia / Base de Datos:** Base de datos relacional/simulada (módulo `base_datos.py`) para control de persistencia e histórico de proveedores.
* **Gestión de Variables de Entorno:** `python-dotenv` para la carga segura del Token de la API de Telegram.
* **Arquitectura de Software:** Máquina de Estados Finitos (FSM) encargada de la gestión de memoria por usuario.

---

## 🗺️ 3. Modelo de Negocio y Gestión de Estados (BPMN 2.0)

El comportamiento del chatbot se rige de forma estricta por un modelo de procesos en donde se separan las tareas del **Usuario** (entradas de texto) y las tareas del **Sistema/Bot** (validaciones y persistencia).

### Máquina de Estados (FSM)
Para evitar respuestas estáticas y dotar al bot de "memoria" contextual, se implementaron múltiples estados definidos en el módulo `estados.py` y controlados dinámicamente en el ciclo de vida de la interacción (`context.user_data`):

- **INICIO / SOLICITAR_CUIT:** Estado inicial donde se da la bienvenida y se pide el identificador fiscal.
- **VALIDACION_CUIT / CONSULTAR_DUPLICADO:** Compuerta lógica que valida el formato y verifica si el CUIT ya existe en la base de datos (Camino de Rechazo).
- **FIN_RECHAZADA:** Es el estado que cobra el sistema al rechazar por completo la solicitud de carga de un proveedor al Usuario.
- **SOLICITAR_RAZON_SOCIAL:** Captura del nombre legal de la empresa.
- **SOLICITAR_EMAIL / VALIDACION_EMAIL:** Entrada y validación sintáctica del correo electrónico.
- **SOLICITAR_TELEFONO / VALIDACION_TELEFONO:** Entrada y validación de longitud/formato telefónico (mínimo 10 dígitos).
- **SOLICITAR_RUBRO:** Captura del sector económico del proveedor.
- **SOLICITAR_CBU / VALIDACION_CBU:** Entrada y verificación del código bancario único (22 dígitos).
- **REGISTRO_COMPLETO / FIN_APROBADA:** Almacenamiento en la base de datos y confirmación de alta exitosa.

---

## 🛡️ 4. Robustez y Manejo del "Camino Infeliz" (Unhappy Path)

El chatbot cuenta con lógica dedicada para la resiliencia ante errores de entrada del usuario o incumplimiento de reglas de negocio:
* **Validaciones estrictas:** Los módulos `validar_cuit`, `validar_email`, `validar_telefono` y `validar_cbu` interceptan las entradas erróneas, notifican el fallo al usuario de forma clara y lo mantienen retenido en el estado correspondiente hasta que ingrese un dato válido.
* **Control de Duplicados:** Si al ingresar el CUIT la función `existe_proveedor(mensaje)` retorna verdadero, la compuerta lógica deriva el flujo de inmediato al estado `FIN_RECHAZADA`, abortando el proceso para evitar colisiones de datos.

---

## 📂 5. Estructura del Repositorio

El proyecto se encuentra modularizado de la siguiente manera:

```bash
├── main.py              # Núcleo del bot, inicialización de handlers y ciclo principal de ejecución.
├── estados.py           # Definición de las constantes de los estados de la FSM.
├── validaciones.py      # Lógica y expresiones regulares de verificación de datos (CUIT, Email, CBU, Teléfono).
├── base_datos.py        # Creación de tablas, almacenamiento persistente y carga de datos de simulación.
├── .env                 # Archivo de configuración confidencial (Contiene el TELEGRAM_TOKEN).
├── .gitignore           # Exclusión de entornos virtuales y archivos de entorno (.env).
└── README.md            # Documentación general del repositorio (Este archivo).

```

🫵🏻 TE TOCA A VOS ! Interactuá con nuestro Bot 🤖💻 

---> Presiona el siguiente enlace : https://t.me/AltaProveedoresChubutBot
