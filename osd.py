import os
import sys
import configparser
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont, QTextDocument
import argparse

# Valores predeterminados globales
default_config = {
    "font": "Arial",
    "color": "white",
    "background": "rgba(0, 0, 0, 128)",
    "size": 24,
    "align": "center",
    "v_align": "center",
    "v_padding": 10,
    "h_padding": 50
}
# Texto por defecto si no se proporciona texto en los argumentos
default_text = "OSD by @trystan4861<br><br>[run OSD -h]"

class OSDWindow(QWidget):
    def __init__(self, text, timeout, config):
        super().__init__()

        # Leer configuraciones del archivo config.ini
        font_name = config.get("OSD", "font", fallback=default_config["font"])
        font_color = config.get("OSD", "font_color", fallback=default_config["color"])
        background_color = config.get("OSD", "background_color", fallback=default_config["background"])
        size = config.getint("OSD", "size", fallback=default_config["size"])
        align = config.get("OSD", "align", fallback=default_config["align"]).lower()
        v_align = config.get("OSD", "v_align", fallback=default_config["v_align"]).lower()
        v_padding = config.getint("OSD", "v_padding", fallback=default_config["v_padding"])
        h_padding = config.getint("OSD", "h_padding", fallback=default_config["h_padding"])

        # Validar align y v_align
        if align not in ["center", "left", "right"]:
            align = default_config["align"]
        if v_align not in ["top", "center", "bottom"]:
            v_align = default_config["v_align"]

        # Configurar fuente
        font = QFont(font_name, size)
        self.setFont(font)

       # Crear el documento de texto
        text_document = QTextDocument()
        text_document.setHtml(text)
        text_document.setDefaultFont(font)

        # Calcular ancho del texto
        text_width = text_document.documentLayout().blockBoundingRect(text_document.firstBlock()).width()
        text_height = text_document.documentLayout().documentSize().height()

        # Obtener tamaño de pantalla
        screen = QApplication.primaryScreen().size()
        screen_width = screen.width()
        screen_height = screen.height()

        # Calcular posición X en función de align y ancho del texto
        if align == "center":
            x_position = (screen_width - text_width) // 2
        elif align == "left":
            x_position = h_padding  # Margen izquierdo
        else:  # right
            x_position = screen_width - text_width - h_padding  # Margen derecho

        # Calcular posición Y en función de v_align y altura del texto
        if v_align == "top":
            y_position = v_padding  # Margen superior
        elif v_align == "center":
            y_position = (screen_height - text_height) // 2
        else:  # bottom
            y_position = screen_height - text_height - v_padding  # Margen inferior

        # Convertir a enteros
        x_position = int(x_position)
        y_position = int(y_position)
        text_width = int(text_width)
        text_height = int(text_height)

        # Configuración de la ventana
        self.setWindowTitle("OSD Display")
        self.setGeometry(x_position, y_position, text_width + 20, text_height + 20)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Fondo transparente

        # Etiqueta para mostrar el texto
        self.label = QLabel(text, self)
        self.label.setWordWrap(True)  # Permite que el texto se ajuste y tenga saltos de línea
        self.label.setStyleSheet(
            f"font-family: {font_name}; font-size: {size}px; color: {font_color}; "
            f"background: {background_color};"
        )
        self.label.setAlignment(Qt.AlignCenter)

        # Ajustar tamaño y posición de la etiqueta
        self.label.setGeometry(0, 0, text_width + 20, text_height + 20)

        # Temporizador para autocerrar
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.timer.start(timeout)  # Inicia el temporizador con el tiempo especificado

        # Mostrar la ventana
        self.show()
def ensure_config_file():
    """Crea el archivo config.ini con valores predeterminados si no existe.
    Devuelve un objeto ConfigParser cargado.
    """
    config_file = "config.ini"
    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        print("Archivo config.ini creado con valores predeterminados.")
        config["OSD"] = default_config
        with open(config_file, "w") as file:
            config.write(file)
    else:
        config.read(config_file)

    # Verificar valores faltantes o inválidos y corregirlos
    updated = False
    if "OSD" not in config:
        config["OSD"] = default_config
        updated = True
    else:
        for key, value in default_config.items():
            if key not in config["OSD"] or not config["OSD"][key].strip():
                config["OSD"][key] = value
                updated = True

    if updated:
        with open(config_file, "w") as file:
            config.write(file)

    return config

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """Sobrescribe el método error para mostrar mensajes personalizados."""
        message="Argumentos incorrectos"
        print(f"Error: {message}")
        self.print_help()
        sys.exit(2)

def main():
    # Parsear los argumentos desde la terminal
    parser = CustomArgumentParser(
        description="Mostrar un texto en pantalla (OSD) con cierre automático.\n"
                    "Ejemplo de uso:\n"
                    "  python osd.py 'Texto a mostrar' -t 3000\n"
                    "  python osd.py 'Texto en pantalla' --timeout 5000",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False  # Desactivamos la ayuda automática
    )
    parser.add_argument("text", nargs="?", default=default_text, help="El texto a mostrar en la pantalla.")
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Muestra este mensaje de ayuda y termina."
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=3000,
        help="Tiempo en milisegundos antes de cerrar el OSD (valor predeterminado: 5000 ms)."
    )
    args = parser.parse_args()

    # Cargar configuraciones
    config = ensure_config_file()

    # Crear la aplicación
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana OSD
    osd = OSDWindow(args.text, args.timeout, config)

    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
