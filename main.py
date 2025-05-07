from gui import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication([])
main_window = MainWindow()
main_window.show()
main_window.showMaximized()
app.exec_()