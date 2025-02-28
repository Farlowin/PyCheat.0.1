import configparser
import sys
import os
import subprocess
import requests
import pymem
from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QProgressBar, QCheckBox, QMenuBar, QMenu
from PySide6 import QtCore
import qt_material
import psutil  

# Создаем папку "cheat" и "Warring", если их нет
os.makedirs("cheat", exist_ok=True)
os.makedirs("Warring", exist_ok=True)

# Файл конфигурации
config = configparser.ConfigParser()
config_path = "config.ini"

if not os.path.exists(config_path):
    config["SETTINGS"] = {
        "version": "1.1",
        "auto_update": "False"
    }
    with open(config_path, "w") as config_file:
        config.write(config_file)
else:
    config.read(config_path)

# Функции логирования
log_file_path = os.path.join("Warring", "log.txt")
error_file_path = os.path.join("Warring", "error.txt")

def log_message(message):
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[INFO] {message}\n")

def log_error(error):
    with open(error_file_path, "a", encoding="utf-8") as error_file:
        error_file.write(f"[ERROR] {error}\n")

class CheatInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyItV1.0.6")
        self.setWindowIcon(QIcon("cheat_icon.png"))
        self.setGeometry(500, 200, 400, 300)
        qt_material.apply_stylesheet(self, theme='dark_amber.xml')

        # Меню
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        settings_menu = QMenu("Настройки", self)
        menu_bar.addMenu(settings_menu)
        
        self.check_update_action = settings_menu.addAction("Проверить обновление (скоро)")

        self.layout = QVBoxLayout()
        self.label = QLabel("Выберите чит:")
        self.layout.addWidget(self.label)

        self.cheat_select = QComboBox(self)
        self.cheat_select.addItem("PyItV1.0.6")
        self.cheat_select.addItem("CS2 Cheat Pro (не доступен)")
        self.layout.addWidget(self.cheat_select)

        self.start_button = QPushButton("Запустить")
        self.start_button.clicked.connect(self.start_cheat)
        self.layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        # Чекбокс автообновления
        self.auto_update_checkbox = QCheckBox("Авто обновление при запуске")
        self.auto_update_checkbox.setChecked(config.getboolean("SETTINGS", "auto_update"))
        self.auto_update_checkbox.stateChanged.connect(self.update_config)
        self.layout.addWidget(self.auto_update_checkbox)

        self.version_label = QLabel(f"v{config['SETTINGS']['version']} версия приложения")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.version_label)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.process = None

    def update_config(self):
        config["SETTINGS"]["auto_update"] = str(self.auto_update_checkbox.isChecked())
        with open(config_path, "w") as config_file:
            config.write(config_file)

    def start_cheat(self):
        try:
            if self.process is None or self.process.state() == QProcess.ProcessState.NotRunning:
                if not self.is_cs2_running():
                    self.run_cs2_and_check()
                else:
                    self.run_cheat()
            else:
                self.stop_cheat()
        except Exception as e:
            log_error(f"Ошибка в start_cheat: {e}")

    def is_cs2_running(self):
        try:
            pm = pymem.Pymem("cs2.exe")
            return True
        except pymem.exception.ProcessNotFound:
            return False
        except Exception as e:
            log_error(f"Ошибка в is_cs2_running: {e}")
            return False

    def run_cs2_and_check(self):
        try:
            log_message("Запуск CS2...")
            subprocess.Popen("cs2.exe")
            QtCore.QTimer.singleShot(5000, self.check_cs2_and_run_cheat)
        except Exception as e:
            log_error(f"Ошибка в run_cs2_and_check: {e}")

    def check_cs2_and_run_cheat(self):
        if self.is_cs2_running():
            self.run_cheat()
        else:
            log_message("CS2 не удалось запустить.")

    def run_cheat(self):
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(50)
            url = "https://raw.githubusercontent.com/Read1dno/PyIt---external-cheat-cs2-in-python/main/PyItV1.0.6.py"
            file_path = "cheat/PyItV1.0.6.py"
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                self.process = QProcess(self)
                self.process.setProgram("python")
                self.process.setArguments([file_path])
                self.process.start()
                self.progress_bar.setValue(100)
            else:
                log_message(f"Ошибка при скачивании: HTTP {response.status_code}")
                self.progress_bar.setValue(0)
        except Exception as e:
            log_error(f"Ошибка в run_cheat: {e}")
            self.progress_bar.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheatInstaller()
    window.show()
    sys.exit(app.exec())
