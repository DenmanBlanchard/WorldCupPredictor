# Only needed for command line arguments
import sys

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import parsedata as prd


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadPool = QThreadPool()

        global mainLayout

        self.setWindowTitle("World Cup Predictor")

        mainLayout = QVBoxLayout()
        headerL = QHBoxLayout()

        headerLabel = QLabel("World Cup Predictor")
        headerF = headerLabel.font()
        headerF.setBold(True)
        headerF.setPointSize(30)
        headerLabel.setFont(headerF)
        headerLabel.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )

        headerL.addWidget(headerLabel)

        loadDataB = QPushButton("Load Data")
        loadDataB.clicked.connect(self.loadData)

        mainLayout.addLayout(headerL)
        mainLayout.addWidget(loadDataB)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def loadData(self):
        worker = prd.Main()
        self.threadPool.start(worker)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
