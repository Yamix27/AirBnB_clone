#!/usr/bin/python3
"""
Test suite for console.py
"""
import sys
import io
import unittest

from unittest import TestCase
from unittest.mock import patch
from console import HBNBCommand


class TestHBNBCommand(TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, expected_output, mock_stdout):
        HBNBCommand().onecmd(expected_output)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

    def test_create_instance(self):
        self.assert_stdout("create BaseModel\n")
        self.assert_stdout("create User\n")

    def test_show_instance(self):
        self.assert_stdout("show BaseModel 1-234\n")
        self.assert_stdout("show User 5-678\n")

    def test_count_instance(self):
        self.assert_stdout("count BaseModel\n")
        self.assert_stdout("count User\n")

    def test_update_instance(self):
        self.assert_stdout("update BaseModel 1-234 name 'New Name'\n")
        self.assert_stdout("update User 5-678 email 'new_email@example.com'\n")

    def test_all_instance(self):
        self.assert_stdout("all\n")
        self.assert_stdout("all BaseModel\n")
        self.assert_stdout("all User\n")

    def test_destroy_instance(self):
        self.assert_stdout("destroy BaseModel 1-234\n")
        self.assert_stdout("destroy User 5-678\n")

    def test_quit_instance(self):
        with self.assertRaises(SystemExit):
            self.assert_stdout("quit\n")

    def test_blank_line_instance(self):
        self.assert_stdout("\n")

    def test_EOF_instance(self):
        with self.assertRaises(SystemExit):
            self.assert_stdout("EOF\n")

    def test_EOF_instance(self):
        with self.assertRaises(SystemExit):
            self.assert_stdout("EOF\n")


if __name__ == "__main__":
    unittest.main()