# This class is used to initialize the PyQt application, main window, scene etc.
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
import os

from pieDiagramPlotter import PieChartView
from histogramPlotter import HistogramView
from filereader import read_file, get_file_name
from linePlot import LinePlotView
from createTable import CSVTableViewer


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pie_diagram = None
        self.histogram = None
        self.line_plot = None
        self.data_path = None
        self.file_name = None
        self.data = None
        self.x_axis = None
        self.y_axis = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        self.setGeometry(560, 140, 1200, 800)
        self.setWindowTitle("Data Visualization Library")

        self.init_file_button()

    def init_file_button(self):
        button = QPushButton('Open file')
        button.clicked.connect(self.get_file_name)
        self.layout.addWidget(button)

    def init_line_plot_button(self):
        line_button = QPushButton('Create Line Plot')
        line_button.clicked.connect(self.show_line_plot_view)
        self.layout.addWidget(line_button)

    def init_pie_chart_button(self):
        pie_button = QPushButton('Create Pie Chart')
        pie_button.clicked.connect(self.show_pie_diagram)
        self.layout.addWidget(pie_button)

    def init_histogram_button(self):
        histogram_button = QPushButton('Create a Histogram')
        histogram_button.clicked.connect(self.show_histogram_view)
        self.layout.addWidget(histogram_button)

    def show_line_plot_view(self):
        self.line_plot = LinePlotView(self.data_path)
        self.line_plot.showMaximized()

    def show_histogram_view(self):
        self.histogram = HistogramView(self.data_path)
        self.histogram.showMaximized()

    def show_pie_diagram(self):
        self.pie_diagram = PieChartView(self.data_path)
        self.pie_diagram.showMaximized()

    def get_file_name(self):
        self.data_path = get_file_name()
        if self.data_path is not None:
            path_text = QLabel("Current file path: " + self.data_path)
            self.file_name = os.path.basename(self.data_path)
            file_name_text_element = QLabel("Current file: " + self.file_name)
            text_layout = QHBoxLayout()

            text_layout.addWidget(path_text)
            text_layout.addWidget(file_name_text_element)
            self.layout.addLayout(text_layout)

            viewer = CSVTableViewer(self.data_path)
            self.data = read_file(self.data_path)[0]

            self.layout.addWidget(viewer)

            self.init_line_plot_button()
            self.init_histogram_button()
            self.init_pie_chart_button()
        else:
            self.get_file_name()
