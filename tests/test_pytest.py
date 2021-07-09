import unittest
import os
from hellowworld import HellowWorld
from hellowworld import FileOperator
from hellowworld import DirectoryOperator


class TestHellowWorld(unittest.TestCase, HellowWorld):
    def test_main(self):
        self.assertEqual(2, self.main(1))


class TestFileOperator(unittest.TestCase, FileOperator):
    def test_file_select(self):
        init_dir = os.path.abspath(os.path.dirname(__file__))
        self.files_select(init_dir, "test_file_select")


class TestDirectoryOperator(unittest.TestCase, DirectoryOperator):
    def test_directory_select(self):
        init_dir = os.path.abspath(os.path.dirname(__file__))
        self.directory_select(init_dir, "test_directory_select")


if __name__ == "__main__":
    unittest.main()
