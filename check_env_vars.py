import os

# Variables de entorno relevantes
variables = [
    "DISPLAY",
    "XAUTHORITY",
    "DBUS_SESSION_BUS_ADDRESS",
    "XDG_RUNTIME_DIR"
]

# Imprimir las variables
for var in variables:
    value = os.getenv(var, "No definida")
    print(f"{var} = {value}")
