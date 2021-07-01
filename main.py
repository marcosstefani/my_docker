import sys, time

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
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
            item = ContainerItem(container)
            self.menu.addAction(item.icon, item.name)
        
        self.menu.addSeparator()


        updateAction = self.menu.addAction("Update")
        updateAction.triggered.connect(self.load)

        exitAction = self.menu.addAction("Close")
        exitAction.triggered.connect(app.quit)

app = QApplication(sys.argv)
client = docker.from_env()

trayIcon = QSystemTrayIcon(QIcon('icon.png'), parent=app)
trayIcon.setToolTip('My Docker')
trayIcon.show()

menu = Menu(client.containers.list(all=True)).menu

trayIcon.setContextMenu(menu)
sys.exit(app.exec_())
