import sys
import unittest

from PyQt6.QtWidgets import QApplication

from filereader import read_file
import linePlot
from gui import MainMenu


class UnitTests(unittest.TestCase):
    def test_read_file_correct_data(self):
        # Creating a fake file with content
        with open('../Documents/fake_file.csv', 'w') as file:
            file.write('x,y\n'
                       '1,2\n'
                       '2,4')

        data_points, x_axis_name, y_axis_name, x_values = read_file('../Documents/fake_file.csv')
        self.assertEqual(x_axis_name, 'x')
        self.assertEqual(y_axis_name, 'y')
        self.assertEqual(x_values, ['1', '3'])
        self.assertEqual(data_points[0].get_y(), 2)

    def test_read_file_empty_data(self):
        # Testing with an empty file
        with open('../Documents/empty_file.csv', 'w') as file:
            file.write('')

        data_points, x_axis_name, y_axis_name, x_values = read_file('../Documents/empty_file.csv')
        self.assertEqual([data_points, x_axis_name, y_axis_name, x_values], [[], "", "", []])

    def test_gui_creation(self):
        app = QApplication(sys.argv)
        myApp = MainMenu()
        self.assertEqual(myApp.line_plot, None)
        self.assertEqual(myApp.windowTitle(), "Data Visualization Library")

    def test_line_plot_draw(self):
        app = QApplication(sys.argv)
        line_plot_app = linePlot.LinePlotView("../Documents/fake_file.csv")
        self.assertEqual(line_plot_app.max_y, 4)


if __name__ == '__main__':
    unittest.main()
