#!/usr/bin/python3
"""
Test suite for Amenity class
"""
import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):

    def setUp(self):
        self.new_user = Amenity()

    def tearDown(self):
        del self.new_user

    def test_user_type(self):
        self.assertEqual(self.new_user.name, "")

    def test_user_attribute(self):
        self.new_user.name = "Root"
        self.assertEqual(self.new_user.name, "Root")


if __name__ == '__main__':
    unittest.main()