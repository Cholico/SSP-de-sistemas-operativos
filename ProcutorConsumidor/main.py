# Arrglar scroll
from PyQt6.QtWidgets import QApplication

from controllers.main_window import MainForm
import sys


if __name__ == '__main__':
    # Aplicación de Qt
    app = QApplication(sys.argv)
    window = MainForm()
    # Se hace visible el botón
    window.show()
    # Qt loopb
    sys.exit(app.exec())