import sys, docker, threading
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMenu, QMessageBox, QSystemTrayIcon, QVBoxLayout, QWidget, qApp

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app):
        super(TrayIcon, self).__init__(QIcon('icon.png'), parent=app)
        self.setToolTip("My Docker")

class Details(QWidget):
    def __init__(self):
        super(Details, self).__init__()
        self.setWindowTitle("My Docker")
        self.setGeometry(300, 300, 640, 480)
        layout = Layout()

        self.setLayout(layout)
        # self.list.itemClicked.connect(self.list.clicked)

class Layout(QHBoxLayout):
    def __init__(self):
        super(Layout, self).__init__()
        self.list = ContainerList()
        self.list.setMaximumWidth(200)
        self.addWidget(self.list)
        self.load_list()

        vbox = QGridLayout()
        vbox.addWidget(QLabel("A"), 1, 3)
        vbox.addWidget(QLabel("B"))
        vbox.addWidget(QLabel("C"))
        vbox.addWidget(QLabel("D"))
        vbox.addWidget(QLabel("E"))

        self.addLayout(vbox)

    def load_list(self):
        docker = Docker()
        self.list.clear()
        for container in docker.containers:
            self.list.addItem(QListWidgetItem(QIcon('on.png' if container.status == 'running' else 'off.png'), container.name))
        
        threading.Timer(5.0, self.load_list).start()

class ContainerList(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "Aviso", "Você clicou em " + item.text())

class Docker:
    def __init__(self):
        self.client = docker.from_env()
        self.containers = self.client.containers.list(all=True)

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