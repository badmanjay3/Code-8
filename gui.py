from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QLabel, QVBoxLayout, QWidget, \
    QHBoxLayout, QFileSystemModel
from PyQt5.QtGui import QFont, QTextBlock
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import uic
from utils import load_file, run, save, new
from syntax_highlighter import SyntaxHighlighter
from pathlib import Path


class MainWindow(QMainWindow):
    path = ""
    name = ""
    extension = ""

    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\Jason Chundusu\\Desktop\\Code 8\\Assets\\c8.1.3.ui", self)
        self.setWindowTitle("Code 8")
        self.visible_lines = []

        # Syntax Highlighter
        self.highlighter = SyntaxHighlighter(self.textEditCodeArea.document())
        self.highlighter.set_language(self.extension)

        # Viewport change tracker
        self.textEditCodeArea.updateRequest.connect(self.update_visible_lines)

        # Arranging layout
        self.lineNumber.setReadOnly(True)
        self.lineNumber.setFixedWidth(70)
        code_area_layout = QHBoxLayout()
        code_area_layout.addWidget(self.lineNumber)
        code_area_layout.addWidget(self.textEditCodeArea)
        code_area_widget = QWidget()
        code_area_widget.setLayout(code_area_layout)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(code_area_widget)
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
        splitter.addWidget(self.treeViewWidget)
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

    # Visible blocks
    def update_visible_lines(self, rect, dy):
        if rect.height() == 0 and dy == 0:
            return  # cursor blink only

        block = self.textEditCodeArea.firstVisibleBlock()
        visible = []
        block_number = block.blockNumber()
        top = self.textEditCodeArea.blockBoundingGeometry(block).translated(
            self.textEditCodeArea.contentOffset()
        ).top()
        bottom = self.textEditCodeArea.viewport().height()

        while block.isValid() and top <= bottom:
            visible.append(str(block_number + 1))
            top += self.textEditCodeArea.blockBoundingRect(block).height()
            block = block.next()
            block_number += 1

        if visible != self.visible_lines:
            self.lineNumber.setPlainText('\n'.join(visible))
            self.visible_lines = visible

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
            self.extension = Path(file_info[0]).suffix.lstrip('.')
            self.tree_view()
            self.textEditCodeArea.setPlainText(file)
            self.highlighter.set_language(self.extension)
            self.highlighter.rehighlight()
            self.statusBar().showMessage("File Opened Successfully", 3000)
            self.update_status_bar(self.path)

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
            self.update_status_bar(file[0])

    def new_(self):
        file = QFileDialog.getSaveFileName(self, "New File", self.path, "*.py;; *.cpp;; *.html;; *.css;; *.txt")
        if file[0]:
            new(file[0])
            self.path = file[0]
            self.extension = Path(file[0]).suffix.lstrip('.')
            self.tree_view()
            self.highlighter.set_language(self.extension)
            self.highlighter.rehighlight()
            self.textEditCodeArea.setPlainText('')
            self.update_status_bar(self.path)

    def close_(self):
        self.path = ''
        self.textEditCodeArea.setPlainText('')
        self.update_status_bar("Untitled File")
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

    def update_status_bar(self, text):
        self.statusLabel.setText(text)

    def tree_view(self):
        path = Path(self.path)
        folder = str(path.parent)
        print(folder)
        try:
            model = QFileSystemModel()
            model.setRootPath(folder)

            self.treeViewWidget.setModel(model)
            self.treeViewWidget.setRootIndex(model.index(folder))

            # Hide the header and irrelevant columns
            self.treeViewWidget.setHeaderHidden(True)
            self.treeViewWidget.hideColumn(1)
            self.treeViewWidget.hideColumn(2)
            self.treeViewWidget.hideColumn(3)
        except TypeError as e:
            print(f"type error: {e.with_traceback()}")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    main_window.showMaximized()
    app.exec_()
