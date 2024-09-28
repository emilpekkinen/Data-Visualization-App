from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel
from filereader import read_file


class CSVTableViewer(QMainWindow):
    def __init__(self, csv_path):
        super().__init__()
        self.setWindowTitle("CSV Data Viewer")
        self.setGeometry(100, 100, 600, 400)

        # Read the CSV data
        data_points, x_axis_name, y_axis_name, x_values = read_file(csv_path)

        headers = [x_axis_name, y_axis_name]

        # Create and configure the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(data_points))
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        i = 0
        for x_value in x_values:
            self.table_widget.setItem(i, 0, QTableWidgetItem(str(x_value)))
            i += 1

        for row_num, point in enumerate(data_points):
            self.table_widget.setItem(row_num, 1, QTableWidgetItem(str(point.get_y())))

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
