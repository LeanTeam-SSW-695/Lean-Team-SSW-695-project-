"""
    authors:
    Abdulellah Shahrani, Chengyi Zhang, Haoran Li, and Sachin Paramesha
    the code:
    The unittest for main.py
"""
import unittest
import main

class TestAPP(unittest.TestCase):

    def test_coordinates(self):
        #test read_address to see whether it can get right coordinates
        address1 = "1925 Commonwealth Avenue, Boston, MA 02135"
        address2 = "20 W 34th St, New York, NY 10001"
        self.assertEqual(main.read_address(address1), {'lat': 42.338842, 'lng': -71.15455279999999})
        self.assertEqual(main.read_address(address2), {'lat': 40.748558, 'lng': -73.9857578})

    def test_distance(self):
        #test distance to see whether it can get the right distance between two coordinates
        x_coordinates = {'lat': 42.338842, 'lng': -71.15455279999999}
        y_coordinates = {'lat': 40.748558, 'lng': -73.9857578}
        self.assertEqual(main.distance(x_coordinates, y_coordinates), ('211 mi', '3 hours 31 mins'))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
