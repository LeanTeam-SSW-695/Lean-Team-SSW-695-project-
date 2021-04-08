"""
    authors:
    Abdulellah Shahrani, Chengyi Zhang, Haoran Li, and Sachin Paramesha
    the code:
    The unittest for main.py
"""
import unittest
import hotel_restaurant_api

class TestAPP(unittest.TestCase):

    def test_restaurant(self):
        result = [{'Name': 'Pinwheel Garden Dumpling & Noodle Bar',
  'Rating': 4.5,
  'Address': '318 Communipaw Ave Jersey City, NJ 07304',
  'Phone': '+12014135333',
  'Review': {'User': 'Vikram G.',
   'Rating': 5,
   'Text': "Full 5 star, I wonder I could give 6 star. Hands down the best Asian American fusion as far as I recall. It's a covid times take out review - the pick was..."}},
 {'Name': 'Bobwhite Counter',
  'Rating': 4.5,
  'Address': '150 Warren St Jersey City, NJ 07302',
  'Phone': '+12014346267',
  'Review': {'User': 'Alyssa G.',
   'Rating': 5,
   'Text': 'Got delivery last night & WOW we have been missing out by not ordering from Bobwhite earlier! It was so good we forget to take pics & dove right in. We...'}},
 {'Name': 'Torta Truck',
  'Rating': 4.5,
  'Address': '31st St & Bergenline Ave Union City, NJ 07087',
  'Phone': '+12014849046',
  'Review': {'User': 'Terri K.',
   'Rating': 5,
   'Text': 'Make sure to check their instagram page before making the trip because their location is subject to change from union city to Jersey city. \n\nI ordered 6...'}},
 {'Name': 'Prince & I',
  'Rating': 4.5,
  'Address': '80 Wayne St Jersey City, NJ 07302',
  'Phone': '+12014233838',
  'Review': {'User': 'Vick V.',
   'Rating': 5,
   'Text': 'The owner is a salt of the earth kinda guy. Thanks us 4x for coming in during the pandemic. Food is wonderfully prepared. Space is cool. BYOW. Stop reading...'}},
 {'Name': 'DOMODOMO Jersey City',
  'Rating': 4.5,
  'Address': '200 Greene St Jersey City, NJ 07302',
  'Phone': '+12012670222',
  'Review': {'User': 'Victoria N.',
   'Rating': 5,
   'Text': 'This spot is offering really cute takeout boxes! I love the way they maintain high quality food as well as aesthetic especially right now. \n\nWe had the...'}}]
        self.assertEqual(hotel_restaurant_api.find_restaurant("jersey city"), result)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
