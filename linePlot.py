import random

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QTransform, QColor, QFont
from PyQt6.QtWidgets import QMainWindow, QGraphicsLineItem, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QPushButton, \
    QSlider, QLabel, QInputDialog

from filereader import read_file, get_file_name

COLORS = [QColor('black'), QColor('red'), QColor('blue'), QColor('green'), QColor('orange'), QColor('brown'),
          QColor('magenta')]


class LinePlotView(QMainWindow):
    def __init__(self, first_line_plot_csv_path):
        super().__init__()

        self.x_title = QGraphicsTextItem("X")
        self.y_title = QGraphicsTextItem("Y")
        self.grid_lines = []
        self.setWindowTitle("Line Plot View")
        self.setGeometry(0, 0, 1200, 800)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.view.scale(1, -1)

        self.add_file_button = QPushButton("Add new file", self)
        self.add_file_button.clicked.connect(self.add_new_data)
        self.scene.addWidget(self.add_file_button)

        self.plot_title = QLabel("", self)
        self.plot_font = QFont("Arial", 16)
        self.plot_font.setBold(True)
        self.plot_title.setFont(self.plot_font)
        self.plot_title.raise_()
        self.plot_title.setMinimumSize(300, 0)
        self.plot_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.plot_title.move(1000, 150)
        self.scene.addWidget(self.plot_title)

        # Create buttons to control the grid
        self.grid_size_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.grid_size_slider.setMinimum(1)
        self.grid_size_slider.setMaximum(10)
        self.grid_size_slider.setValue(5)
        self.grid_size_slider.move(100, 300)
        self.scene.addWidget(self.grid_size_slider)

        self.grid_button = QPushButton('Show Grid', self)
        self.grid_button.clicked.connect(self.show_grid)
        self.grid_button.move(100, 100)
        self.scene.addWidget(self.grid_button)

        self.delete_grid_button = QPushButton("Hide grid", self)
        self.delete_grid_button.clicked.connect(self.delete_grid)
        self.delete_grid_button.move(100, 150)
        self.scene.addWidget(self.delete_grid_button)

        self.grid_size = 5

        self.grid_size_slider.valueChanged.connect(self.update_grid)

        self.grid_label = QLabel("Change grid size", self)
        self.grid_label.setFont(QFont("Arial", 10))
        self.grid_label.move(104, 260)
        self.grid_size_label = QLabel(f"Grid size: {self.grid_size}", self)
        self.grid_size_label.move(117, 325)

        # Create buttons to control the axes and title names
        self.rename_x_axis_titles_button = QPushButton('Rename x-axis', self)
        self.rename_x_axis_titles_button.move(1500, 200)
        self.rename_x_axis_titles_button.clicked.connect(self.rename_x_axis_title)
        self.scene.addWidget(self.rename_x_axis_titles_button)

        self.rename_y_axis_titles_button = QPushButton('Rename y-axis', self)
        self.rename_y_axis_titles_button.move(1500, 250)
        self.rename_y_axis_titles_button.clicked.connect(self.rename_y_axis_title)
        self.scene.addWidget(self.rename_y_axis_titles_button)

        self.rename_plot_title_button = QPushButton('Rename Plot Title', self)
        self.rename_plot_title_button.move(1500, 150)
        self.rename_plot_title_button.clicked.connect(self.rename_plot_title)
        self.scene.addWidget(self.rename_plot_title_button)

        # Axes Graphics
        self.axis_pen = QPen()
        self.axis_pen.setWidth(3)

        # Keep track of lines:
        self.lines = []

        # Keep track of data labels on the axes:
        self.data_labels = []

        # Axes parameters
        self.range_x = 0
        self.range_y = 0
        self.desired_range_x = 500
        self.desired_range_y = 500
        self.scale_x = 0
        self.scale_y = 0

        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

        # Axes
        self.x_axis = None
        self.y_axis = None

        # Plot the initial Line Plot
        self.add_initial_data(first_line_plot_csv_path)

        self.show()

    def add_initial_data(self, first_line_plot_csv_path):
        data_points, x_axis_name, y_axis_name, x_values = read_file(first_line_plot_csv_path)
        file_name = first_line_plot_csv_path.split('/')[-1]
        self.plot_title.setText(file_name)
        self.plot_data(data_points, file_name)

    def add_new_data(self):
        new_file_path = get_file_name()
        data_points, x_axis_name, y_axis_name, x_values = read_file(new_file_path)
        file_name = new_file_path.split('/')[-1]
        self.delete_labels()
        self.update_title_names()
        self.plot_data(data_points, file_name)
        self.update_grid()

    def plot_data(self, data_points, file_name):
        plot_lines = []
        data_labels = []
        if not data_points:
            print("No data points provided.")
            return

        # Handle the line thickness and the color of the data series
        line_pen = QPen()
        line_pen.setWidth(3)
        color = random.choice(COLORS)
        line_pen.setColor(color)

        # Create the data series legend
        legend_font = QFont()
        legend_font.setPointSize(12)
        legend = QGraphicsTextItem(f"{file_name}")
        legend.setDefaultTextColor(color)  # Set the color of the to be the same as the line
        legend.setFont(legend_font)
        legend.setTransform(QTransform().scale(1, -1))

        COLORS.remove(color) # Ensures that there are no same colors graphics

        self.scene.addItem(legend)  # Add the legend to the graphics view

        # Find min and max values for X and Y in the data
        min_x = max_x = data_points[0].X
        min_y = max_y = data_points[0].Y

        # Loop through each point in the list
        for point in data_points:
            # Update min and max for X
            if point.X < min_x:
                min_x = point.X
            if point.X > max_x:
                max_x = point.X

            # Update min and max for Y
            if point.Y < min_y:
                min_y = point.Y
            if point.Y > max_y:
                max_y = point.Y

        # Determine the range of data to calculate scaling factor
        range_x = max_x - min_x
        range_y = max_y - min_y
        scale_x = self.desired_range_x / range_x if range_x != 0 else 1
        scale_y = self.desired_range_y / range_y if range_y != 0 else 1

        if scale_x > self.scale_x:
            self.scale_x = scale_x

        if scale_y > self.scale_y:
            self.scale_y = scale_y

        if min_x < self.min_x:
            self.min_x = min_x

        if min_y < self.min_y:
            self.min_y = min_y

        if max_x > self.max_x:
            self.max_x = max_x

        if max_y > self.max_y:
            self.max_y = max_y

        if range_x > self.range_x:
            self.range_x = range_x

        if range_y > self.range_y:
            self.range_y = range_y

        # Create axes
        self.x_axis = QGraphicsLineItem(min_x * self.scale_x - min_x * self.scale_x, 0, max_x * self.scale_x, 0)
        self.y_axis = QGraphicsLineItem(0, min_y * self.scale_y - min_y * self.scale_y, 0, max_y * self.scale_y)
        self.x_axis.setPen(self.axis_pen)
        self.y_axis.setPen(self.axis_pen)

        self.scene.addItem(self.x_axis)
        self.scene.addItem(self.y_axis)

        # Draw data labels for the X axis
        x_increment = (self.range_x + min_x) / len(data_points)  # Set the increment value
        x_value = 0.0
        while x_value <= max_x:
            label = QGraphicsTextItem(f"{x_value:.1f}")
            label.setPos(x_value * self.scale_x, -30)  # Positioning label at x_value slightly below the axis
            label.setTransform(QTransform().scale(1, -1))
            self.scene.addItem(label)
            data_labels.append(label)  # Save the label object
            x_value += x_increment

        # Draw data labels for the Y axis
        y_increment = (self.range_y + min_y) / len(data_points)
        y_value = 0.0
        while y_value <= max_y:
            label = QGraphicsTextItem(f"{y_value:.1f}")
            label.setPos(-60, y_value * self.scale_y)  # Positioning label slightly left of the axis
            label.setTransform(QTransform().scale(1, -1))
            self.scene.addItem(label)
            data_labels.append(label)
            y_value += y_increment

        # Create a font for the titles
        title_font = QFont("Arial", 10)
        title_font.setBold(True)

        # Draw titles for the axis
        self.x_title.setFont(title_font)
        self.x_title.setPos(self.max_x * self.scale_x + 10, 12)
        self.x_title.setTransform(QTransform().scale(1, -1))
        self.scene.addItem(self.x_title)

        self.y_title.setFont(title_font)
        self.y_title.setPos(-7, self.max_y * self.scale_y + 30)
        self.y_title.setTransform(QTransform().scale(1, -1))
        self.scene.addItem(self.y_title)

        # Position the legend label according to the axis
        legend.setPos(max_x * self.scale_x, (max_y / 2) * self.scale_y)

        plot_lines.append(legend)  # Save the legend that is associated with a plot

        # Draw line plot of the data from a given file
        for i in range(len(data_points) - 1):
            current_point = data_points[i]
            next_point = data_points[i + 1]
            line = QGraphicsLineItem(current_point.X * self.scale_x, current_point.Y * self.scale_y,
                                     next_point.X * self.scale_x,
                                     next_point.Y * self.scale_y)
            plot_lines.append(line)  # Save each line to list
            line.setPen(line_pen)
            self.scene.addItem(line)

        self.lines.append(plot_lines)  # Save the legend and the lines as a list
        self.data_labels.append(data_labels)

        self.show()

    def delete_labels(self):
        for label in self.data_labels[0]:
            self.scene.removeItem(label)  # Properly remove the item from the scene
            label.deleteLater()  # Schedule the item for deletion
        self.data_labels[0].clear()  # Clear the list after deleting all items
        print("Labels removed successfully!")

    def update_grid(self):
        self.grid_size = self.grid_size_slider.value()
        self.grid_size_label.setText(f"Grid size: {self.grid_size}")
        print("New grid size: ", self.grid_size)
        self.delete_grid()
        self.show_grid()

    def show_grid(self):
        print("Grid shown")

        x_value = 0.0

        x_value_max = self.max_x
        y_value_max = self.max_y
        print("Max x:", x_value_max)

        while x_value <= self.max_x:
            line = QGraphicsLineItem(x_value * self.scale_x, 0, x_value * self.scale_x, y_value_max * self.scale_y)
            pen = QPen(QColor('gray'))  # Gray color
            pen.setStyle(Qt.PenStyle.DashLine)  # Set the pen style to dashed
            pen.setWidth(2)  # Set the width of the pen
            line.setPen(pen)
            line.setZValue(-1)
            self.scene.addItem(line)
            self.grid_lines.append(line)
            x_value += self.grid_size

        y_value = 0.0
        while y_value <= self.max_y:
            line = QGraphicsLineItem(0, y_value * self.scale_y, x_value_max * self.scale_x, y_value * self.scale_y)
            pen = QPen(QColor('gray'))  # Gray color
            pen.setStyle(Qt.PenStyle.DashLine)  # Set the pen style to dashed
            pen.setWidth(1)  # Set the width of the pen
            line.setPen(pen)
            line.setZValue(-1)
            self.scene.addItem(line)
            self.grid_lines.append(line)
            y_value += self.grid_size

    def delete_grid(self):
        for line in self.grid_lines:
            self.scene.removeItem(line)  # Properly remove the item from the scene
        self.grid_lines.clear()  # Clear the list after deleting all items
        print("Grid removed successfully!")

    def rename_x_axis_title(self):
        text, ok = QInputDialog.getText(self, 'Change x-axis title', 'Enter new name')
        if ok:
            self.x_title.setPlainText(text)

    def rename_y_axis_title(self):
        text, ok = QInputDialog.getText(self, 'Change y-axis title', 'Enter new name')
        if ok:
            self.y_title.setPlainText(text)

    def rename_plot_title(self):
        text, ok = QInputDialog.getText(self, 'Change plot title', 'Enter new title')
        if ok:
            self.plot_title.setText(text)

    def update_title_names(self):
        self.scene.removeItem(self.x_title)
        self.scene.removeItem(self.y_title)
