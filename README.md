# Monitor de Batería para Linux

## Descripción del Proyecto

Este proyecto consiste en un script diseñado para monitorear el estado de la batería de una laptop que utiliza el sistema operativo Linux. El script verifica periódicamente el nivel de la batería y envía notificaciones cuando el nivel de carga es crítico, ayudando a prevenir apagones inesperados y permitiendo al usuario concentrarse en su trabajo sin preocuparse por la duración de la batería.

## Motivación

Como programador, a menudo me encuentro absorto en mi trabajo, lo que me lleva a perder de vista el estado de la batería de mi laptop. Para evitar interrupciones en mi flujo de trabajo debido a una batería agotada, desarrollé este script que me avisa cuando la carga de la batería es baja, permitiéndome prevenir apagones innecesarios. Este proyecto surge de la necesidad de automatizar esta tarea y mejorar mi productividad.

## Instrucciones para la Instalación y Configuración

### Requisitos Previos

- Python 3 instalado en tu sistema.
- Dependencias de Python: `psutil` y `notify_py`.
- `systemd` instalado y configurado en tu sistema.

### Paso 1: Clonar el repositorio y configurar el entorno

1. Clona el repositorio en una ubicación deseada (por ejemplo, `/opt`):
    ```bash
    sudo git clone https://github.com/brianmrdev/check_low_battery.git /opt
    ```
   
2. Crea y activa un entorno virtual en la carpeta del proyecto:
    ```bash
    cd /opt/check_low_battery
    python3 -m venv env
    source env/bin/activate
    ```

3. Instala las dependencias:
    ```bash
    pip install psutil notify_py
    ```
### Paso 2: Crear el archivo systemd para el servicio

1. Crea un archivo de servicio en `/etc/systemd/system/battery-monitor.service`:
    ```bash
    sudo nano /etc/systemd/system/battery-monitor.service
    ```
   
2. Añade la siguiente configuración en el archivo:

    ```ini
    [Unit]
    Description=Battery Monitor Script
    After=multi-user.target

    [Service]
    Type=simple
    ExecStart=/opt/check_low_battery/env/bin/python3 /opt/check_low_battery/main.py
    Restart=always
    User=tu_usuario

    [Install]
    WantedBy=default.target
    ```

   > **Nota**: Cambia `tu_usuario` por tu nombre de usuario de Linux.

3. Guarda el archivo y recarga los servicios de **systemd** para aplicar los cambios:
    ```bash
    sudo systemctl daemon-reload
    ```

4. Habilita y ejecuta el servicio:
    ```bash
    sudo systemctl enable battery-monitor.service
    sudo systemctl start battery-monitor.service
    ```
### Paso 3: Verificar el estado del servicio

Para comprobar si el servicio está funcionando correctamente, usa el siguiente comando:

```bash
systemctl status battery-monitor.service
```
### Paso 4: Ajustar configuración

- Puedes personalizar las notificaciones y sonidos modificando los archivos correspondientes en la carpeta `utils`.
- Para ajustar el idioma, modifica la variable `LANGUAGE` en el archivo `main.py`:
    ```python
    LANGUAGE = "es"  # Las opciones posibles son "es" para español o "en" para inglés
    ```
- Para cambiar el umbral de alerta de batería, modifica la constante `BATTERY_LOW_THRESHOLD` en el archivo `main.py`:
    ```python
    BATTERY_LOW_THRESHOLD = 30  # Porcentaje de batería baja
    ```
- Para ajustar el intervalo de chequeo, modifica la constante `CHECK_INTERVAL` en el archivo `main.py`:
    ```python
    CHECK_INTERVAL = 600  # Intervalo de tiempo en segundos (10 minutos)
    ```
## Desinstalación

Para deshabilitar y eliminar el servicio:

1. Detén y deshabilita el servicio:
    ```bash
    sudo systemctl stop battery-monitor.service
    sudo systemctl disable battery-monitor.service
    ```

2. Elimina el archivo de servicio:
    ```bash
    sudo rm /etc/systemd/system/battery-monitor.service
    ```

3. Recarga los demonios de **systemd**:
    ```bash
    sudo systemctl daemon-reload
    ```
## Contribuir

Las contribuciones son bienvenidas. Si deseas agregar nuevas características o corregir errores, por favor, abre un **pull request** o inicia una discusión.

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz commit (`git commit -m "Descripción de los cambios"`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un **pull request**.

## MIT License

Este proyecto está licenciado bajo los términos de la [MIT License](./LICENSE).