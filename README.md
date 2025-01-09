# OSD (On-Screen Display)

**Versión 1.0**

Un proyecto de utilidad para mostrar mensajes en pantalla como un Overlay transparente. Este script, escrito en Python, permite personalizar el texto, la posición y la apariencia del mensaje, ofreciendo una experiencia de notificación simple y configurable.

---

## Características

- **Personalización total:**
  - Fuente, tamaño y color del texto.
  - Posición horizontal (izquierda, centro, derecha) y vertical (arriba, centro, abajo).
  - Margen personalizado para alineaciones específicas.
- **Compatibilidad multi-pantalla:**
  - Calcula automáticamente las dimensiones de texto y pantalla para adaptarse a cualquier resolución.
- **Autocierre:**
  - Configurable mediante un temporizador que cierra automáticamente el mensaje tras un tiempo especificado.
- **Interfaz amigable:**
  - Incluye argumentos por línea de comandos y un archivo `config.ini` para ajustes predeterminados.

---

## Requisitos

- **Python 3.7 o superior**
- Dependencias:
  - `PyQt5`

Instalar dependencias con:

```bash
pip install PyQt5
```

---

## Uso

### Desde el código fuente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/osd.git
   cd osd
   ```
2. Ejecuta el script:
   ```bash
   python osd.py "Texto a mostrar" -t 5000
   ```
   Ejemplo:
   ```bash
   python osd.py "Bienvenido al sistema" --timeout 3000
   ```

### Argumentos disponibles

- `text`: El texto a mostrar en la pantalla. (Opcional: Por defecto muestra "OSD by @trystan4861\n[run OSD -h]")
- `-t, --timeout`: Tiempo en milisegundos antes de cerrar el OSD. (Opcional: Por defecto es 3000 ms)
- `-h, --help`: Muestra ayuda sobre cómo usar el script.

### Configuración avanzada

El archivo `config.ini` se genera automáticamente al ejecutar el script por primera vez. Puedes personalizar los valores predeterminados:

```ini
[OSD]
font = Arial
color = rgba(255, 255, 255, 255)
background = rgba(0, 0, 0, 128)
size = 24
align = center
v_align = center
v_padding = 10
h_padding = 50
```
```
font = FontName de la fuente a usar, Arial, Calibri, Tahoma, Lucide Sans, etc
color = rgba(), nombre de color como red, white, black, etc.
backgrond = rgba(), nombre de color como red, white, black, etc.
size = Tamaño de la fuente en puntos
align = left, center, right
v_align = top, center, bottom
v_padding = Padding vertical en pixeles (referido al espacio entre el OSD y el borde de la pantalla en los modos align top y bottom)
h_padding = Padding horizontal en pixeles (referido al espacio entre el OSD y el borde de la pantalla en los modos align left y right)
```
---

## Compilación a ejecutable

Si deseas convertir el script en un archivo ejecutable para Windows:

1. Instala PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Genera el ejecutable:
   ```bash
   pyinstaller --onefile --noconsole osd.py
   ```
3. Encuentra el archivo `osd.exe` en la carpeta `dist/`.

### Evitar la consola emergente

Para evitar que se abra una ventana de consola al ejecutar el ejecutable:

```bash
pyinstaller --onefile --noconsole osd.py
```

---

## Solución a falsos positivos de antivirus

Si el ejecutable es detectado como un virus:

1. Asegúrate de usar la última versión de PyInstaller.
2. Usa la opción `--clean` durante la compilación.
3. Considera firmar digitalmente el ejecutable.
4. Reporta el falso positivo al proveedor del antivirus.

---

## Contribuciones

¡Este proyecto está abierto a mejoras! Si tienes ideas o encuentras algún problema, no dudes en crear un issue o enviar un pull request.

---

## Créditos

- Autor: **@trystan4861**
- Versión: 1.0

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

---

## Capturas de pantalla

<img src="https://raw.githubusercontent.com/Trystan4861/OSD/refs/heads/main/screenshot.jpg" />
