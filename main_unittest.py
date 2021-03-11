#!/usr/bin/env python
# coding: utf-8

# In[3]:


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
        self.assertEqual(main.read_address(address1), {'x': -71.15493, 'y': 42.33858})
        self.assertEqual(main.read_address(address2), {'x': -73.985344, 'y': 40.748756})

    def test_distance(self):
        #test distance to see whether it can get the right distance between two coordinates
        x_coordinates = {'x': -71.15493, 'y': 42.33858}
        y_coordinates = {'x': -73.985344, 'y': 40.748756}
        self.assertEqual(int(main.distance(x_coordinates, y_coordinates)), 198)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


# In[ ]:




