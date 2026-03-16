from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
import sys
import matplotlib as mpl

# Optimize Matplotlib rendering speed
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0
mpl.rcParams['agg.path.chunksize'] = 10000

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    
    window.show()
    app.exec()

