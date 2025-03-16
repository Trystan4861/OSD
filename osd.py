import os
import sys
import configparser
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QFont, QFontDatabase, QTextDocument
import argparse

# Valores predeterminados globales
default_config = {
    "font": "Arial",
    "font_color": "rgba(255, 255, 255, 255)",
    "background_color": "rgba(0, 0, 0, 128)",
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
        font_color = config.get("OSD", "font_color", fallback=default_config["font_color"])
        background_color = config.get("OSD", "background_color", fallback=default_config["background_color"])
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

        # Configurar fuente usando QFontDatabase
        font_db = QFontDatabase()

        # Intentar cargar la fuente por su nombre exacto
        exact_font_name = None
        for family in font_db.families():
            if family.lower() == font_name.lower():
                exact_font_name = family
                print(f"Fuente encontrada: {exact_font_name}")
                break

        if exact_font_name is None:
            print(f"No se encontró la fuente '{font_name}'. Usando Arial.")
            exact_font_name = "Arial"
            font = QFont("Arial", size)
        else:
            # Crear la fuente con configuración específica
            font = QFont(exact_font_name, size)
            font.setStyleStrategy(QFont.PreferAntialias | QFont.PreferQuality)

            # Verificar si la fuente se cargó correctamente
            if not font.exactMatch():
                print("Advertencia: La fuente no coincide exactamente.")
                print(f"Familia solicitada: {exact_font_name}")
                print(f"Familia actual: {font.family()}")

        self.setFont(font)

        # Crear el documento de texto con configuración específica
        text_document = QTextDocument()
        text_document.setDefaultFont(font)
        text_document.setHtml(text)

        # Calcular dimensiones
        text_width = text_document.idealWidth()
        text_height = text_document.size().height()

        # Obtener tamaño de pantalla
        screen = QApplication.primaryScreen().size()
        screen_width = screen.width()
        screen_height = screen.height()

        # Calcular posición X en función de align y ancho del texto
        if align == "center":
            x_position = (screen_width - text_width) // 2
        elif align == "left":
            x_position = h_padding
        else:  # right
            x_position = screen_width - text_width - h_padding

        # Calcular posición Y en función de v_align y altura del texto
        if v_align == "top":
            y_position = v_padding
        elif v_align == "center":
            y_position = (screen_height - text_height) // 2
        else:  # bottom
            y_position = screen_height - text_height - v_padding

        # Convertir a enteros
        x_position = int(x_position)
        y_position = int(y_position)
        text_width = int(text_width)
        text_height = int(text_height)

        # Configuración de la ventana
        self.setWindowTitle("OSD Display")
        self.setGeometry(x_position, y_position, text_width + 20, text_height + 20)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Etiqueta para mostrar el texto con configuración específica
        self.label = QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(
            f"font-family: '{exact_font_name}'; font-size: {size}px; color: {font_color}; "
            f"background: {background_color};"
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, text_width + 20, text_height + 20)

        # Temporizador para autocerrar
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.timer.start(timeout)

        # Mostrar la ventana
        self.show()

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """Sobrescribes el método error para mostrar mensajes personalizados."""
        message="Argumentos incorrectos"
        print(f"Error: {message}")
        self.print_help()
        sys.exit(2)

def ensure_config_file():
    """Crea el archivo config.ini con valores predeterminados si no existe.
    Devuelve un objeto ConfigParser cargado.
    """
    # Obtener la ruta del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.ini")
    config = configparser.ConfigParser(allow_no_value=True)  # Permitir comentarios sin valor
    config_error = False

    if not os.path.exists(config_file): # si no existe el archivo de configuración marcamos error de configuración
        config_error = True
    else:
        config.read(config_file, encoding="utf-8") # si la configuración no dispone de la sección OSD, marcamos error de configuración
        if "OSD" not in config:
            config_error = True

    if config_error: # si hubo error en el archivo de configuración lo regeneramos
        print(f"Archivo config.ini creado con valores predeterminados en {config_file}")
        config["OSD"] = {}

        # Agregar comentarios explicativos
        config.set("OSD", "; Configuración de la fuente")
        config.set("OSD", "; font: Nombre de la fuente (ej: Arial, Times New Roman, Alone in the Dark)")
        config.set("OSD", "font", "Arial")

        config.set("OSD", "\n; Colores en formato rgba(red, green, blue, alpha)")
        config.set("OSD", "; font_color: Color del texto")
        config.set("OSD", "font_color", "rgba(255, 255, 255, 255)")
        config.set("OSD", "; background_color: Color del fondo")
        config.set("OSD", "background_color", "rgba(0, 0, 0, 128)")

        config.set("OSD", "\n; Tamaño de la fuente en píxeles")
        config.set("OSD", "size", "24")

        config.set("OSD", "\n; Alineación horizontal del texto")
        config.set("OSD", "; align: Valores posibles: left, center, right")
        config.set("OSD", "align", "center")

        config.set("OSD", "\n; Alineación vertical del texto")
        config.set("OSD", "; v_align: Valores posibles: top, center, bottom")
        config.set("OSD", "v_align", "center")

        config.set("OSD", "\n; Márgenes en píxeles")
        config.set("OSD", "; v_padding: Margen vertical")
        config.set("OSD", "v_padding", "10")
        config.set("OSD", "; h_padding: Margen horizontal")
        config.set("OSD", "h_padding", "50")

        with open(config_file, "w", encoding="utf-8") as file:
            config.write(file)

    config.read(config_file, encoding="utf-8")

    updated = False
    # Verificar valores faltantes o inválidos y corregirlos
    for key, value in default_config.items():
        if key not in config["OSD"] or not config["OSD"][key].strip():
            config["OSD"][key] = str(value)
            updated = True

    if updated: # si hubo correciones en los valores guardamos el archivo de configuración
        with open(config_file, "w", encoding="utf-8") as file:
            config.write(file)

    return config

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
        help="Tiempo en milisegundos antes de cerrar el OSD (valor predeterminado: 3000 ms)."
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
