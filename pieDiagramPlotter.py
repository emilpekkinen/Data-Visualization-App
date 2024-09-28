# This class draws a pie diagram based on the data it receives.
import random

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPen, QTransform, QColor, QFont, QBrush
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QPushButton, QLabel, QInputDialog, QGraphicsEllipseItem

from filereader import read_file

COLORS = [QColor('black'), QColor('red'), QColor('blue'), QColor('green'), QColor('orange'), QColor('brown'),
          QColor('magenta')]


def define_total_sum(data_points):
    total = 0
    for data_point in data_points:
        total += data_point.Y
    return total


class PieChartView(QMainWindow):
    def __init__(self, first_line_plot_csv_path):
        super().__init__()
        self.setWindowTitle("Pie Chart View")
        self.setGeometry(0, 0, 1200, 800)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.view.scale(1, -1)

        self.plot_title = QLabel("Long Placeholder text to ensure that wanted content fits in here", self)
        self.plot_font = QFont("Arial", 16)
        self.plot_font.setBold(True)
        self.plot_title.setFont(self.plot_font)
        self.plot_title.raise_()
        self.plot_title.setMinimumSize(200, 0)
        self.plot_title.move(1000, 100)
        self.scene.addWidget(self.plot_title)

        self.rename_plot_title_button = QPushButton('Rename Plot Title', self)
        self.rename_plot_title_button.move(1500, 150)
        self.rename_plot_title_button.clicked.connect(self.rename_plot_title)
        self.scene.addWidget(self.rename_plot_title_button)

        # Keep track of data labels on the pie_chart:
        self.data_labels = []

        # Pie chart parameters
        self.total = None
        self.start_angle = 0
        self.pie_rect = QRectF(100, 100, 300, 300)

        # Create the Pie chart
        self.add_data(first_line_plot_csv_path)

        self.show()

    def add_data(self, first_line_plot_csv_path):
        data_points, x_axis_name, y_axis_name, x_values = read_file(first_line_plot_csv_path)
        file_name = first_line_plot_csv_path.split('/')[-1]
        self.total = define_total_sum(data_points)
        self.plot_title.setText(file_name)
        self.plot_data(data_points, file_name, x_values)

    def plot_data(self, data_points, file_name, x_values):
        pie_chart_items = []
        data_labels = []
        if not data_points:
            print("No data points provided.")
            return

        i = 1
        j = 0
        for data_point in data_points:
            # Handle the line thickness and the color of the data series
            pie_segment_pen = QPen()
            pie_segment_pen.setWidth(3)
            color = random.choice(COLORS)
            pie_segment_pen.setColor(color)

            pie_segment_fill = QBrush()
            pie_segment_fill.setColor(color)
            pie_segment_fill.setStyle(Qt.BrushStyle.SolidPattern)

            COLORS.remove(color)  # Ensures that there are no same colors graphics

            # Create the data series legend for a segment
            legend_font = QFont()
            legend_font.setPointSize(16)
            legend_font.setBold(True)
            legend = QGraphicsTextItem(f"{x_values[j]}")
            legend.setDefaultTextColor(color)  # Set the color of the to be the same as the segment
            legend.setFont(legend_font)
            legend.setTransform(QTransform().scale(1, -1))

            self.scene.addItem(legend)  # Add the legend to the graphics view

            # Position the label
            legend.setPos(1000, 50*i)

            pie_chart_items.append(legend)  # Save the legend that is associated with a histogram plot

            x_value = x_values[j]
            self.draw_segment(data_point, pie_segment_pen, pie_segment_fill, i, x_value, legend_font)

            self.show()

            i += 1
            j += 1

    def rename_plot_title(self):
        text, ok = QInputDialog.getText(self, 'Change plot title', 'Enter new title')
        if ok:
            self.plot_title.setText(text)

    def draw_segment(self, data_point, pen, fill, i, x_value, font):
        y_value = data_point.Y
        segment_percentage = y_value / self.total  # Calculate how much a certain segment is from the total
        segment_span_angle = int(segment_percentage * 360 * 16)

        # Create a segment of the pie chart
        segment = QGraphicsEllipseItem(200, 50, 400, 400)
        segment.setPen(pen)
        segment.setBrush(fill)
        segment.setStartAngle(self.start_angle)
        segment.setSpanAngle(segment_span_angle)

        label = QGraphicsTextItem(f"{segment_percentage*100:.2f} %")
        text_align_value = 1000 + len(x_value) * 20 if 1000 + len(x_value) * 40 < 1300 else 1150
        label.setPos(text_align_value, 50*i)
        label.setTransform(QTransform().scale(1, -1))
        label.setFont(font)

        self.scene.addItem(segment)
        self.scene.addItem(label)

        self.start_angle += segment_span_angle
