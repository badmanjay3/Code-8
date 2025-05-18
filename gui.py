from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFileDialog, QLabel, QVBoxLayout, QWidget, \
    QHBoxLayout, QFileSystemModel, QTextEdit, QPlainTextEdit, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
from utils import load_file, run, save, new
from syntax_highlighter import SyntaxHighlighter
from pathlib import Path
import webbrowser
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\Jason Chundusu\\Desktop\\Code 8\\Assets\\c8.1.3.ui", self)
        self.setWindowTitle("Code 8")
        self.server_thread = None
        self.httpd = None

        self.tabs = {}  # Maps tab index to editor-related data
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.switch_tab)

        # Output area setup
        self.textEditOutput.setReadOnly(True)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.tab_widget)
        splitter1.addWidget(self.textEditOutput)
        splitter1.setStretchFactor(0, 3)
        splitter1.setStretchFactor(1, 2)

        layout = QVBoxLayout()
        layout.addWidget(self.btnRun)
        layout.addWidget(splitter1)
        container = QWidget()
        container.setLayout(layout)

        splitter = QSplitter()
        splitter.addWidget(self.treeViewWidget)
        splitter.addWidget(container)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        self.setCentralWidget(splitter)

        # Status bar
        self.autoSaveLabel = QLabel("Auto Save: Off")
        self.statusLabel = QLabel("Untitled File")
        self.statusBar().addPermanentWidget(self.autoSaveLabel)
        self.statusBar().addPermanentWidget(self.statusLabel)

        # Connect actions
        self.btnRun.clicked.connect(self.run_)
        self.actionSave.triggered.connect(self.save_)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionNew.triggered.connect(self.new_)
        self.actionOpen.triggered.connect(self.open_)
        self.actionClose.triggered.connect(self.close_)
        self.actionAuto_save.setCheckable(True)
        self.actionAuto_save.toggled.connect(self.toggle_auto_save)

        # Add default tab
        self.add_tab("Untitled", '', '', '')

    def add_tab(self, name, content, path, extension):
        line_number = QTextEdit()
        line_number.setReadOnly(True)
        line_number.setFixedWidth(70)

        code_area = QPlainTextEdit()
        code_area.setPlainText(content)
        code_area.updateRequest.connect(lambda rect, dy: self.update_line_numbers(code_area, line_number, rect, dy))

        highlighter = SyntaxHighlighter(code_area.document())
        highlighter.set_language(extension)

        wrapper_layout = QHBoxLayout()
        wrapper_layout.addWidget(line_number)
        wrapper_layout.addWidget(code_area)
        wrapper = QWidget()
        wrapper.setLayout(wrapper_layout)

        index = self.tab_widget.addTab(wrapper, name)
        self.tabs[index] = {
            "editor": code_area,
            "line_number": line_number,
            "path": path,
            "extension": extension,
            "highlighter": highlighter
        }
        self.tab_widget.setCurrentIndex(index)

    def current_tab_data(self):
        index = self.tab_widget.currentIndex()
        return self.tabs.get(index, {})

    def switch_tab(self, index):
        path = self.tabs.get(index, {}).get("path", "Untitled File")
        self.statusLabel.setText(path)

    def update_line_numbers(self, editor, line_number_widget, rect, dy):
        if rect.height() == 0 and dy == 0:
            return
        block = editor.firstVisibleBlock()
        visible = []
        block_number = block.blockNumber()
        top = editor.blockBoundingGeometry(block).translated(editor.contentOffset()).top()
        bottom = editor.viewport().height()

        while block.isValid() and top <= bottom:
            visible.append(str(block_number + 1))
            top += editor.blockBoundingRect(block).height()
            block = block.next()
            block_number += 1

        line_number_widget.setPlainText('\n'.join(visible))

    def toggle_auto_save(self, checked):
        editor = self.current_tab_data().get("editor")
        if editor:
            if checked:
                editor.textChanged.connect(self.auto_save)
                self.autoSaveLabel.setText("Auto Save: On")
            else:
                editor.textChanged.disconnect(self.auto_save)
                self.autoSaveLabel.setText("Auto Save: Off")

    def auto_save(self):
        data = self.current_tab_data()
        if data.get("path"):
            save(data["editor"].toPlainText(), data["path"])
            self.statusBar().showMessage("Auto-saved", 2000)

    def open_(self):
        file_info = QFileDialog.getOpenFileName(self, "Open File", "", "*.py *.cpp *.html *.css *.txt *.js *.json")
        if file_info[0]:
            content = load_file(file_info[0])
            extension = Path(file_info[0]).suffix.lstrip('.')
            name = Path(file_info[0]).name
            self.add_tab(name, content, file_info[0], extension)
            self.tree_view(file_info[0])
            self.statusBar().showMessage("File Opened Successfully", 3000)

    def save_(self):
        data = self.current_tab_data()
        print(data)
        if data.get("path"):
            save(data["editor"].toPlainText(), data["path"])
            self.statusBar().showMessage("File Saved Successfully", 3000)

    def save_as(self):
        data = self.current_tab_data()
        file = QFileDialog.getSaveFileName(self, "Save File As", data.get("path", ""), "*.py;; *.cpp;; *.html;; *.css;; *.txt")
        if file[0]:
            save(data["editor"].toPlainText(), file[0])
            data["path"] = file[0]
            data["extension"] = Path(file[0]).suffix.lstrip('.')
            self.statusLabel.setText(file[0])
            highlighter = data.get("highlighter")
            highlighter.set_language(data["extension"])
            highlighter.rehighlight()

    def new_(self):
        file = QFileDialog.getSaveFileName(self, "New File", "", "*.py;; *.cpp;; *.html;; *.css;; *.txt")
        if file[0]:
            new(file[0])
            extension = Path(file[0]).suffix.lstrip('.')
            name = Path(file[0]).name
            self.add_tab(name, '', file[0], extension)
            self.tree_view(file[0])

    def close_(self):
        index = self.tab_widget.currentIndex()
        if index >= 0:
            self.tab_widget.removeTab(index)
            self.tabs.pop(index, None)
            if self.tab_widget.count() == 0:
                self.add_tab("Untitled", '', '', '')

    def run_(self):
        data = self.current_tab_data()
        if not data.get("path"):
            self.statusBar().showMessage("No file to run", 2000)
            return

        extension = data["extension"]
        file_path = data["path"]

        if extension in ["html", "htm"]:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            port = 8000

            # Stop previous server if running
            if self.httpd:
                self.httpd.shutdown()
                self.httpd = None

            def start_server():
                os.chdir(directory)
                self.httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
                self.httpd.serve_forever()

            self.server_thread = threading.Thread(target=start_server, daemon=True)
            self.server_thread.start()

            # Open the file in browser via localhost
            webbrowser.open(f"http://localhost:{port}/{filename}")
            self.textEditOutput.clear()
            self.textEditOutput.append(f"Serving {filename} at http://localhost:{port}/")

        elif extension in ["css", "js"]:
            self.textEditOutput.clear()
            self.textEditOutput.append("Please run the HTML file that links to this CSS/JS.")

        elif extension in ["py", "cpp"]:
            result = run(file_path)
            self.textEditOutput.clear()
            self.textEditOutput.append(result)

        else:
            self.textEditOutput.clear()
            self.textEditOutput.append("Cannot run this file type.")

    def tree_view(self, path):
        folder = str(Path(path).parent)
        try:
            model = QFileSystemModel()
            model.setRootPath(folder)
            self.treeViewWidget.setModel(model)
            self.treeViewWidget.setRootIndex(model.index(folder))
            self.treeViewWidget.setHeaderHidden(True)
            self.treeViewWidget.hideColumn(1)
            self.treeViewWidget.hideColumn(2)
            self.treeViewWidget.hideColumn(3)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec_()
