import time
import json
import psutil
from notifypy import Notify
from pathlib import Path

# Constantes
BATTERY_LOW_THRESHOLD = 30
CHECK_INTERVAL = 600  # 10 minutos
LANGUAGE = "en"  # Las opciones posibles son "es" para español o "en" para inglés



# Cargar la configuración desde el archivo JSON
def load_config(language=LANGUAGE):
    try:
        language_file_path = Path("utils/language.json").resolve()
        with open(language_file_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Fallback al inglés si el idioma no está disponible
            return config.get(language, config["en"])
    except FileNotFoundError:
        print("Error: El archivo de configuración no se encontró.")
        return {}


class CustomNotify(Notify):
    def __init__(self, title=None, message=None, icon=None, audio=None):
        super().__init__()
        if title:
            self.title = title
        if message:
            self.message = message
        if icon:
            self.icon = str(Path(icon).resolve())
        if audio:
            self.audio = str(Path(audio).resolve())


def notify_battery_low(config, percent):
    notification = CustomNotify(
        title=config["battery_low_title"],
        message=config["battery_low_message"].format(percent=percent),
        icon="utils/low-battery.png",
        audio=config["battery_low_audio"]
    )
    notification.send()


def notify_battery_error(config):
    notification = CustomNotify(
        title=config["battery_error_title"],
        message=config["battery_error_message"],
        icon="utils/error.png",
        audio=config["battery_error_audio"]
    )
    notification.send()


def check_battery(last_notified, config):
    battery = psutil.sensors_battery()
    if battery is None:
        notify_battery_error(config)
        return last_notified

    plugged = battery.power_plugged
    percent = battery.percent

    # Enviar notificación solo si batería es <= 30%, no está enchufada y aún no se ha notificado
    if percent <= BATTERY_LOW_THRESHOLD and not plugged and not last_notified:
        notify_battery_low(config, percent)
        last_notified = True
    elif percent > BATTERY_LOW_THRESHOLD or plugged:
        last_notified = False

    return last_notified


def main():
    config = load_config()
    notified = False

    while True:
        notified = check_battery(notified, config)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
