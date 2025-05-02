from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from utils import load_file, run, save, new
from time import sleep


class MainWindow(QMainWindow):
    path = ""
    name = ""
    extension = ""

    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\Jason Chundusu\\Desktop\\Code 8\\Assets\\c8.1.3.ui", self)
        self.setWindowTitle("Code 8")

        # Layout and Splitter
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.textEditCodeArea)
        splitter1.addWidget(self.textEditOutput)
        self.textEditOutput.setReadOnly(True)
        splitter1.setStretchFactor(0, 3)
        splitter1.setStretchFactor(1, 2)

        layout = QVBoxLayout()
        layout.addWidget(self.btnRun)
        layout.addWidget(splitter1)
        widget = QWidget()
        widget.setLayout(layout)

        splitter = QSplitter()
        splitter.addWidget(self.treeWidget)
        splitter.addWidget(widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        self.setCentralWidget(splitter)

        # Status bar widgets
        self.autoSaveLabel = QLabel("Auto Save: Off")
        self.statusLabel = QLabel("Untitled File")
        self.statusBar().addPermanentWidget(self.autoSaveLabel)
        self.statusBar().addPermanentWidget(self.statusLabel)

        # Linking buttons and their functions
        self.btnRun.clicked.connect(self.run_)
        self.actionSave.triggered.connect(self.save_)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionNew.triggered.connect(self.new_)
        self.actionOpen.triggered.connect(self.open_)
        self.actionClose.triggered.connect(self.close_)

        self.actionAuto_save.setCheckable(True)
        self.actionAuto_save.toggled.connect(self.toggle_auto_save)

    def toggle_auto_save(self, checked):
        if checked:
            self.textEditCodeArea.textChanged.connect(self.auto_save)
            self.autoSaveLabel.setText("Auto Save: On")
        else:
            try:
                self.textEditCodeArea.textChanged.disconnect(self.auto_save)
            except TypeError:
                pass
            self.autoSaveLabel.setText("Auto Save: Off")

    def auto_save(self):
        if self.path:
            content = self.textEditCodeArea.toPlainText()
            save(content, self.path)
            self.statusBar().showMessage("Auto-saved", 2000)

    def open_(self):
        file_info = QFileDialog.getOpenFileName(self, "Open File", "", "*.py *.cpp *.html *.css *.txt")
        if file_info[0]:
            file = load_file(file_info[0])
            self.path = file_info[0]
            self.extension = file_info[1]
            self.textEditCodeArea.setPlainText(file)
            self.statusBar().showMessage("File Opened Successfully", 3000)
            self.updateStatusBar(self.path)

    def save_(self):
        if self.path:
            content_ = self.textEditCodeArea.toPlainText()
            save(content_, self.path)
            self.statusBar().showMessage("File Saved Successfully", 3000)

    def save_as(self):
        file = QFileDialog.getSaveFileName(self, "Save File As", self.path, "*.py;; *.cpp;; *.html;; *.css;; *.txt")
        if file[0]:
            save(self.textEditCodeArea.toPlainText(), file[0])
            self.path = file[0]
            self.updateStatusBar(file[0])

    def new_(self):
        file = QFileDialog.getSaveFileName(self, "New File", self.path, "*.py;; *.cpp;; *.html;; *.css;; *.txt")
        if file[0]:
            new(file[0])
            self.path = file[0]
            self.extension = file[1]
            self.textEditCodeArea.setPlainText('')
            self.updateStatusBar(self.path)

    def close_(self):
        self.path = ''
        self.textEditCodeArea.setPlainText('')
        self.updateStatusBar("Untitled File")
        self.statusBar().showMessage("File Closed Successfully", 3000)

    def run_(self):
        if self.path:
            result = run(self.path)
            self.textEditOutput.clear()
            self.textEditOutput.append(result)

    def theme(self, colour):
        self.textEditCodeArea.setStyleSheet(f"background-color: {colour};")
        self.textEditOutput.setStyleSheet(f"background-color: {colour};")
        self.statusLabel.setStyleSheet(f"background-color: {colour};")
        self.statusBar().setStyleSheet(f"background-color: {colour};")
        self.treeWidget.setStyleSheet(f"background-color: {colour};")
        self.btnRun.setStyleSheet(f"background-color: {colour};")
        self.centralwidget.setStyleSheet(f"background-color: {colour};")
        font = QFont("Consolas", 10)
        self.textEditCodeArea.setFont(font)

    def updateStatusBar(self, text):
        self.statusLabel.setText(text)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    main_window.showMaximized()
    app.exec_()
