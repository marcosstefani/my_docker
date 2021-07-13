import sys, docker, threading
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QListWidget, QMainWindow, QMenu, QMessageBox, QSystemTrayIcon, qApp

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app):
        super(TrayIcon, self).__init__(QIcon('icon.png'), parent=app)
        self.setToolTip("My Docker")

class Details(QMainWindow):
    def __init__(self):
        super(Details, self).__init__()
        self.setWindowTitle("My Docker")
        self.setGeometry(300, 300, 640, 480)
        self.list = ContainerList()
        self.setCentralWidget(self.list)
        self.load_list()
        self.list.itemClicked.connect(self.list.clicked)

    def load_list(self):
        docker = Docker()
        self.list.clear()
        for container in docker.containers:
            self.list.addItem(container.name)
        threading.Timer(5.0, self.load_list).start()

class ContainerList(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "Aviso", "Você clicou em " + item.text())

class Docker:
    def __init__(self):
        self.client = docker.from_env()
        self.containers = self.client.containers.list(all=False)

class Application:
    def __init__(self):
        app = QApplication(sys.argv)
        QApplication.setQuitOnLastWindowClosed(False)
        self.trayIcon = TrayIcon(app)
        self.menu = QMenu()
        self.trayIcon.setContextMenu(self.menu)
        self.details_action = self.menu.addAction('Details')
        self.details_action.triggered.connect(self.show_details)
        self.exit_action = self.menu.addAction("Exit")
        self.exit_action.triggered.connect(qApp.quit)

        self.trayIcon.show()
        sys.exit(app.exec_())

    def show_details(self):
        self.details = Details()
        self.details.show()


if __name__ == '__main__':
    Application()