import sys, threading

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

import docker

class ContainerItem:
    def __init__(self, container):
        self.icon = QIcon('on.png' if container.status == 'running' else 'off.png')
        self.name = container.name

class Menu:
    def __init__(self, containers):
        self.menu = QMenu()
        self.containers = containers
        self.load()

    def load(self):
        self.menu.clear()
        for container in self.containers:
            print(container.name)
            item = ContainerItem(container)
            self.menu.addAction(item.icon, item.name)

class Application(QSystemTrayIcon):
    message = pyqtSignal(QMenu)
    client = docker.from_env()

    def __init__(self, app):
        super(Application, self).__init__(QIcon('icon.png'), parent=app)
        self.app = app
        self.setToolTip("My Docker")
        self.message.connect(self.setContextMenu)
    
    def close(self):
        raise Exception("Exit")

    def loadMenu(self):
        menu = Menu(self.client.containers.list(all=True)).menu

        menu.addSeparator()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.close)

        self.message.emit(menu)
        threading.Timer(5.0, self.loadMenu).start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trayIcon = Application(app)
    trayIcon.loadMenu()
    trayIcon.show()
    sys.exit(app.exec_())
