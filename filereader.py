# This class handles the reading of the files, i.e. converts data sets
# to a form that the program understands.
import os

from PyQt6.QtWidgets import QFileDialog

# accepts .csv files i.e. the values for different entries are separated with a comma
# the first row includes headers
# each line represents data for a specific year, date, entity etc.

from point import Point


def read_file(file_path):
    if file_path.endswith(".csv"):

        try:
            data = []
            with open(file_path, 'r') as file:
                for row in file:
                    row_data = row.strip().split(",")
                    data.append(row_data)

            x_axis_name = data[0][0]
            y_axis_name = data[0][1]

            data.pop(0)

            data_points = []
            x_values = []

            i = 0
            for data_pair in data:
                data_point = Point(i, float(data_pair[1]))
                x_value = data_pair[0]
                data_points.append(data_point)
                x_values.append(x_value)
                i += 1

            return data_points, x_axis_name, y_axis_name, x_values

        except IndexError:
            print("Warning! The file seems to be empty")
            return [], "", "", []

        except ValueError:
            print("Error in the CSV file, please check the file")

    else:
        print("The file selected was not a csv file. Please try again")
        get_file_name()


def get_file_name():
    file_filter = 'Data File (*.csv)'
    response = QFileDialog.getOpenFileName(
        caption='Select a file',
        directory=os.getcwd(),
        filter=file_filter,
        initialFilter='Data File (*.csv)'
    )
    if response[0]:  # Ensure a file was selected
        file_path = response[0]
        return file_path

