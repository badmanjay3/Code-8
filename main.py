from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QPlainTextEdit, QPushButton

class UIMainWindow(QtWidgets.QMainWindow):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Code 8")
        MainWindow.showMaximized()

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Layouts
        main_layout = QVBoxLayout(self.centralwidget)
        button_layout = QHBoxLayout()

        # Buttons
        self.saveBtn = QPushButton("Save")
        self.newBtn = QPushButton("New")
        self.loadBtn = QPushButton("Load")
        self.runBtn = QPushButton("Run")

        for btn in [self.saveBtn, self.newBtn, self.loadBtn, self.runBtn]:
            button_layout.addWidget(btn)

        # Editor & terminal
        self.codeArea = QPlainTextEdit()
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: black; color: white;")

        # Add widgets to main layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.codeArea, 2)   # 2: ratio weight
        main_layout.addWidget(self.terminal, 1)   # 1: ratio weight

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Connect buttons
        self.saveBtn.clicked.connect(self.save_)
        self.loadBtn.clicked.connect(self.load_)
        self.runBtn.clicked.connect(self.run_)

        self.path = ""


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

