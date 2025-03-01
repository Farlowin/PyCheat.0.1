import os
import sys
import logging
import subprocess
import configparser
import requests
import psutil
log_dir = "Logs"
log_file = os.path.join(log_dir, "log.txt")
os.makedirs(log_dir, exist_ok=True)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                               QPushButton, QLabel, QComboBox, QProgressBar, QCheckBox, QMenuBar, QMenu, QMessageBox)
import qt_material
import psutil  

CONFIG_URL = "https://raw.githubusercontent.com/Farlowin/PythoCheats/main/config.ini"
UPDATE_URL = "https://raw.githubusercontent.com/Farlowin/PythoCheats/main/PYCHEAT.exe"
LOCAL_CONFIG = "config.ini"
LOCAL_EXECUTABLE = "PYCHEAT.exe"

CHEAT_URL_CS2ESP = "https://raw.githubusercontent.com/Read1dno/CS2ESP-external-cheat/main/CS2ESP.py"
CHEAT_PATH_CS2ESP = "bin/CS2ESP.py"


CHEAT_URL_06 = "https://raw.githubusercontent.com/Read1dno/PyIt---external-cheat-cs2-in-python/main/PyItV1.0.6.py"
CHEAT_PATH_06 = "bin/PyItV1.0.6.py"
REQUIRED_LIBRARIES = [
    "PySide6",
    "requests",
    "pymem",
    "pywin132",
    "pynput",
    "qt_material"
]

def check_missing_libraries():
    """Проверяет отсутствующие библиотеки, если проверка включена в config.ini."""
    if not check_libraries:
        logger.info("Проверка библиотек отключена в настройках.")
        return []

    missing = []
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib)
        except ImportError:
            missing.append(lib)
    return missing

def install_libraries(libraries):
    """Устанавливает недостающие библиотеки."""
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + libraries)

    

os.makedirs("Logs", exist_ok=True)
os.makedirs("bin", exist_ok=True)
text = """
Если чит  PyItV1.0.6 не запускается, выполните следующие шаги:

 
1. Установите необходимые библиотеки, введя в терминале:  
   pip install PySide6 requests pymem pywin32 pynput qt_material  
2 если не помогло то обновите Pythjn
3 Или свяжитесь с разрабочиком Discord jacklats TG jacklats
После этого запустите CS2.  
Выберите чит.  
Нажмите "Запустить".  

Важно:  
- В CS2 должно быть включено разрешение "В окне".  
- Чит запускать только во время катки, иначе WH не будет работать.  

Разработчик: JackLat.  
Помощник: Meetlat Show.  
"""

if not os.path.exists("info.txt"):
    with open("info.txt", "w", encoding="utf-8") as file:
        file.write(text)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("Logs/log.txt", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

config_path = "config.ini"
config = configparser.ConfigParser()

if not os.path.exists(config_path):
    config["SETTINGS"] = {"auto_update": "False", "version": "1.1", "check_libraries": "False"}
    with open(config_path, "w") as config_file:
        config.write(config_file)
else:
    config.read(config_path)


check_libraries = config.getboolean("SETTINGS", "check_libraries", fallback=True)


def get_remote_version():
    try:
        response = requests.get(CONFIG_URL, timeout=5)
        if response.status_code == 200:
            remote_config = configparser.ConfigParser()
            remote_config.read_string(response.text)
            return remote_config.get("SETTINGS", "version", fallback="0.0")
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении версии: {e}")
    return None

def get_local_version():
    return config.get("SETTINGS", "version", fallback="0.0")

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
    except requests.RequestException as e:
        logging.error(f"Ошибка загрузки {filename}: {e}")
    return False

def kill_process(name):
    """Закрывает все процессы с указанным именем."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == name.lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def update_files():
    if download_file(CONFIG_URL, LOCAL_CONFIG) and download_file(UPDATE_URL, LOCAL_EXECUTABLE):
        QMessageBox.information(None, "Обновление", "Обновление успешно установлено. Перезапуск...")


        kill_process("PYCHEAT.exe")


        subprocess.Popen([LOCAL_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)


        sys.exit()

def is_cs2_running():
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'].lower() == "cs2.exe":
            return True
    return False
def show_info():
    info_path = "info.txt"
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as file:
            info_text = file.read()
        QMessageBox.information(None, "Как пользоваться", info_text)
    else:
        QMessageBox.warning(None, "Ошибка", "Файл info.txt не найден!")

class CheatInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCheat CS2")
        self.setWindowIcon(QIcon("cheat_icon.png"))
        self.setGeometry(500, 200, 400, 300)
        qt_material.apply_stylesheet(self, theme='dark_amber.xml')

        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        settings_menu = QMenu("Меню", self)
        menu_bar.addMenu(settings_menu)
        self.check_update_action = settings_menu.addAction("Проверить обновление")
        self.check_update_action.triggered.connect(self.check_for_update)

        self.layout = QVBoxLayout()
        self.label = QLabel("Выберите чит:")
        self.layout.addWidget(self.label)

        self.cheat_select = QComboBox(self)
        self.cheat_select.addItem("PyItV1.0.6")        
        self.cheat_select.addItem("CS2ESP")
        self.layout.addWidget(self.cheat_select)

        self.start_button = QPushButton("Запустить")
        self.start_button.clicked.connect(self.toggle_cheat)
        self.layout.addWidget(self.start_button)

        self.info_button = QPushButton("Как пользоваться")
        self.info_button.clicked.connect(show_info)
        self.layout.addWidget(self.info_button)
        
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.setVisible(False)

        self.status_label = QLabel("Готово")
        self.layout.addWidget(self.status_label)

        self.auto_update_checkbox = QCheckBox("Авто обновление при запуске")
        self.auto_update_checkbox.setChecked(config.getboolean("SETTINGS", "auto_update", fallback=True))
        self.auto_update_checkbox.stateChanged.connect(self.update_config)
        self.layout.addWidget(self.auto_update_checkbox)

        self.version_label = QLabel(f"v{get_local_version()} версия приложения")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.version_label)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        if self.auto_update_checkbox.isChecked():
            self.check_for_update()

    def check_for_update(self):
        remote_version = get_remote_version()
        local_version = get_local_version()

        if remote_version and remote_version > local_version:
            reply = QMessageBox.question(self, "Обновление доступно",
                                        f"Доступна новая версия ({remote_version}). Обновить?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                update_files()

    def update_config(self, state):
        config["SETTINGS"]["auto_update"] = str(bool(state))
        with open(config_path, "w") as config_file:
            config.write(config_file)

    def toggle_cheat(self):
        global cheat_process
        if self.start_button.text() == "Запустить":
            self.start_cheat()
        else:
            self.stop_cheat()
    def closeEvent(self, event):

        self.stop_cheat()
        event.accept()
    def check_python_version(self):
        """Проверяет наличие Python и его версию."""
        if sys.version_info < (3, 8):
            self.show_python_error()
            return False
        return True

    def show_python_error(self):
        """Выводит сообщение об ошибке и предлагает скачать Python."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ошибка Python")
        layout = QVBoxLayout()

        label = QLabel("У вас не установлен Python или его версия ниже 3.8.\n"
                       "Перейдите в папку установки Python или скачайте новую версию.")
        layout.addWidget(label)

        download_button = QPushButton("Скачать Python")
        close_button = QPushButton("Закрыть")

        download_button.clicked.connect(lambda: webbrowser.open("https://www.python.org/downloads/"))
        close_button.clicked.connect(dialog.close)

        layout.addWidget(download_button)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.exec()



    def start_cheat(self):
        """Запускает чит, если все условия соблюдены."""
        global cheat_process

        if not self.check_python_version():
            return  

        if check_libraries:  
            missing_libraries = check_missing_libraries()
            if missing_libraries:
                reply = QMessageBox.question(
                    self, "Отсутствуют библиотеки",
                    f"Не найдены библиотеки: {', '.join(missing_libraries)}\nУстановить их?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    install_libraries(missing_libraries)
                else:
                    return

        if not is_cs2_running():
            QMessageBox.warning(self, "Ошибка", "Запустите CS2 перед запуском чита.")
            return

        cheat_name = self.cheat_select.currentText()
        cheat_path = None

        if cheat_name == "CS2ESP":
            cheat_path = os.path.join("bin", "CS2ESP.py")
            download_function = self.download_cheat_CS2ESP
        elif cheat_name == "PyItV1.0.6":
            cheat_path = os.path.join("bin", "PyItV1.0.6.py")
            download_function = self.download_cheat_06
        else:
            QMessageBox.warning(self, "Ошибка", "Выбранный чит не поддерживается.")
            return

        if not os.path.exists(cheat_path):
            download_function()
        
        self.active_cheat_file = cheat_path  
        self.status_label.setText("Запуск чита...")
        cheat_process = subprocess.Popen(["python", cheat_path], shell=True)
        self.start_button.setText("Отключить")
        self.status_label.setText(f"Чит {cheat_name} запущен.")
        QMessageBox.information(self, "Запуск", f"Чит {cheat_name} успешно запущен!")


    def stop_cheat(self):
        global cheat_process
        if cheat_process and self.active_cheat_file:

            cheat_process.terminate()
            cheat_process = None

    
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if "python" in process.info['name'].lower() or "python.exe" in process.info['name'].lower():
                    process.terminate()  

            self.start_button.setText("Запустить")
            self.status_label.setText(f"Чит {self.active_cheat_file} отключен.")
            QMessageBox.information(self, "Отключение", f"Чит {self.active_cheat_file} успешно отключен!")
            self.active_cheat_file = None 



    def download_cheat_CS2ESP(self):
        self.status_label.setText("Скачивание чита...")
        response = requests.get(CHEAT_URL_CS2ESP, stream=True)
        with open(CHEAT_PATH_CS2ESP, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        self.status_label.setText("Чит успешно скачан.")

    def download_cheat_06(self):
        self.status_label.setText("Скачивание чита...")
        response = requests.get(CHEAT_URL_06, stream=True)
        with open(CHEAT_PATH, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        self.status_label.setText("Чит успешно скачан.")        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheatInstaller()
    window.show()
    sys.exit(app.exec())
