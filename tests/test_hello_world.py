import unittest
import tkinter
import os
import logging
import sys
from io import StringIO

from hello_world import (
    DirectoryOperator,
    OsPathAlternative,
    FileOperator,
    SetTkinter,
    Logger,
)
from unittest import mock


class UnittestFunctions(unittest.TestCase, OsPathAlternative):
    def assertExists(self, path):
        return self.assertTrue(self._is_exists(path))

    def assertNotExists(self, path):
        return self.assertFalse(self._is_exists(path))

    def assertCreateTestFiles(self, *paths):
        d = DirectoryOperator()
        f = FileOperator()
        for path in paths:
            dir_name, base_name = os.path.split(path)

            if self._is_not_exists(path):
                filename_and_ext = os.path.splitext(base_name)

                if filename_and_ext[1] == "":
                    d.directory_create(dir_name, base_name)

                else:
                    f.file_create(dir_name, filename_and_ext[0], "file_body")

            self.assertExists(path)

    def assertRemoveTestFiles(self, *paths):
        d = DirectoryOperator()
        f = FileOperator()
        for path in paths:
            if os.path.isdir(path):
                d.directory_remove(path, True)
            else:
                f.file_remove(path, True)

            self.assertNotExists(path)


class TestOsPathAlternative(mock.MagicMock, DirectoryOperator):
    def test__is_exists(self):
        test_path = self._join_path(self._current_directory, "test")
        self.directory_create(self._current_directory, "test")
        self.assertTrue(self._is_exists(test_path))
        self.directory_remove(test_path, True)
        self.assertFalse(self._is_exists(test_path))

    def test__is_not_exists(self):
        test_path = self._join_path(self._current_directory, "test")
        self.directory_create(self._current_directory, "test")
        self.assertFalse(self._is_not_exists(test_path))
        self.directory_remove(test_path, True)
        self.assertTrue(self._is_not_exists(test_path))

    def test__join_path(self):
        self.assertEqual(
            os.path.join(os.path.expanduser("~"), "dev", "pytest"),
            self._join_path(os.path.expanduser("~"), "dev", "pytest"),
        )

    def test__split_path(self):
        dir_test_path = self._join_path(self._current_directory, "test")
        file_test_path = self._join_path(self._current_directory, "test_text.txt")

        self.assertEqual(
            self._split_path(dir_test_path), [self._current_directory, "test", ""]
        )
        self.assertEqual(
            self._split_path(file_test_path),
            [self._current_directory, "test_text", ".txt"],
        )

    def test__current_directory(self):
        self.assertEqual(
            self._join_path(os.path.expanduser("~"), "dev", "pytest"),
            self._current_directory,
        )


class TestLogger(UnittestFunctions, Logger):
    def test__init(self):
        self.assertFalse(hasattr(self, "_logger"))
        self.assertFalse(hasattr(self, "_lev"))
        self._init()
        self.assertIsInstance(self._logger, logging.Logger)
        self.assertEqual(
            {
                "ERROR": logging.ERROR,
                "WARNING": logging.WARNING,
                "INFO": logging.INFO,
                "DEBUG": logging.DEBUG,
            },
            self._lev,
        )

    def test_logger_output(self):
        sys.stdout = StringIO()
        self._init()
        self.logger_output("DEBUG", "Logger test.")
        self.assertTrue("[DEBUG] Logger test." in sys.stdout.getvalue())


class TestSetTkinter(mock.MagicMock, SetTkinter):
    def setUp(self):
        self.tkinter = mock.MagicMock()

    def test__set_tkinter(self):
        del self.tkinter
        self.assertFalse(hasattr(self, "_window"))
        self.assertFalse(hasattr(self, "tkinter"))
        self._set_tkinter()
        self.assertTrue(hasattr(self, "_window"))
        self.assertTrue(hasattr(self, "tkinter"))
        self.assertIsInstance(self._window, tkinter.Tk)
        self.assertIs(self.tkinter, tkinter)

        self._set_tkinter()


class TestDirectoryOperator(mock.MagicMock, DirectoryOperator):
    def setUp(self):
        self.tkinter = mock.MagicMock()

    def test_directory_select(self):
        def askdirectory(title, initialdir):
            return initialdir

        self.tkinter.filedialog.askdirectory = askdirectory
        self.assertEqual(
            self._current_directory, self.directory_select("Directory_select_test")
        )

    def test_directory_create(self):
        test_path = self._join_path(self._current_directory, "test")
        self.assertRemoveTestFiles(test_path)

        self.directory_create(self._current_directory, "test")
        self.assertExists(test_path)

        self.assertFalse(self.directory_create(self._current_directory, "test"))

        self.assertRemoveTestFiles(test_path)

    def test_directory_remove(self):
        test_path = self._join_path(self._current_directory, "test")
        self.assertRemoveTestFiles(test_path)
        self.assertCreateTestFiles(test_path)

        self.assertFalse(self.directory_remove(test_path, False))

        self.directory_remove(test_path, True)
        self.assertNotExists(test_path)

    def test_directory_move(self):
        test_path = self._join_path(self._current_directory, "test")
        target_path = self._join_path(self._current_directory, "target")
        result_path = self._join_path(test_path, "target")
        self.assertRemoveTestFiles(test_path, target_path, result_path)
        self.assertCreateTestFiles(test_path, target_path)

        self.assertNotExists(result_path)

        self.directory_move(target_path, test_path)
        self.assertExists(result_path)
        self.assertNotExists(target_path)

        self.assertFalse(self.directory_move(target_path, test_path))

        self.directory_create(self._current_directory, "target")
        self.assertFalse(self.directory_move(target_path, test_path))

        self.assertRemoveTestFiles(test_path, target_path)

    def test_directory_copy(self):
        test_path = self._join_path(self._current_directory, "test")
        target_path = self._join_path(self._current_directory, "target")
        result_path = self._join_path(test_path, "target")
        self.assertRemoveTestFiles(test_path, target_path, result_path)
        self.assertCreateTestFiles(test_path, target_path)

        self.assertNotExists(result_path)

        self.directory_copy(target_path, test_path)
        self.assertExists(target_path)
        self.assertExists(result_path)

        self.assertFalse(self.directory_copy(target_path, test_path))

        self.assertRemoveTestFiles(test_path, target_path)
        self.assertFalse(self.directory_copy(target_path, test_path))

    def test_directory_rename(self):
        rename = "test_2"
        test_path = self._join_path(self._current_directory, "test")
        rename_path = self._join_path(self._current_directory, f"{rename}")
        self.assertRemoveTestFiles(test_path, rename_path)
        self.assertCreateTestFiles(test_path)

        self.assertNotExists(rename_path)

        self.directory_rename(test_path, rename)
        self.assertNotExists(test_path)
        self.assertExists(rename_path)

        self.directory_create(self._current_directory, "test")
        self.assertFalse(self.directory_rename(test_path, rename))

        self.assertRemoveTestFiles(test_path, rename_path)

    def test_directory_duplicate_check(self):
        test_path = self._join_path(self._current_directory, "test")
        test_check_path = self._join_path(self._current_directory, "test(1)")
        self.assertRemoveTestFiles(test_path, test_check_path)
        self.assertCreateTestFiles(test_path)

        test_check_ok_path = self.directory_duplicate_check(test_path)
        self.assertEqual(test_check_path, test_check_ok_path)

        self.directory_remove(test_path, True)

        test_check_ok_path = self.directory_duplicate_check(test_path)
        self.assertEqual(test_path, test_check_ok_path)


class TestFileOperator(mock.MagicMock, FileOperator):
    def setUp(self):
        self.tkinter = mock.MagicMock()

    def test_files_select(self):
        test_path = self._join_path(self._current_directory, "test_text.txt")
        self.assertRemoveTestFiles(test_path)
        self.assertCreateTestFiles(test_path)

        def askopenfilenames(title, filetypes, initialdir, multiple):
            return test_path

        self.tkinter.filedialog.askopenfilenames = askopenfilenames
        file_path = self.files_select("File_select_test")

        self.assertEqual(test_path, file_path)

        self.assertRemoveTestFiles(test_path)

    def test_file_create(self):
        test_path = self._join_path(self._current_directory, "test_text.txt")
        self.assertRemoveTestFiles(test_path)

        self.file_create(self._current_directory, "test_text", "text_body")
        self.assertExists(test_path)

        self.assertFalse(
            self.file_create(self._current_directory, "test_text", "text_body")
        )

        self.assertRemoveTestFiles(test_path)

    def test_file_remove(self):
        test_path = self._join_path(self._current_directory, "test_text.txt")
        self.assertRemoveTestFiles(test_path)
        self.assertCreateTestFiles(test_path)

        self.assertFalse(self.file_remove(test_path, False))

        self.file_remove(test_path, True)
        self.assertNotExists(test_path)

    def test_file_move(self):
        test_path = self._join_path(self._current_directory, "test_text.txt")
        to_path = self._join_path(self._current_directory, "test_in")
        result_path = self._join_path(to_path, "test_text.txt")
        self.assertRemoveTestFiles(test_path, to_path, result_path)
        self.assertCreateTestFiles(test_path, to_path)

        self.assertNotExists(result_path)

        self.file_move(test_path, to_path)
        self.assertExists(result_path)
        self.assertNotExists(test_path)

        self.assertFalse(self.file_move(test_path, to_path))

        self.file_create(self._current_directory, "test_text", "")
        self.assertFalse(self.file_move(test_path, to_path))

        self.assertRemoveTestFiles(test_path, to_path)

    def test_file_copy(self):
        test_path = self._join_path(self._current_directory, "test_text.txt")
        to_path = self._join_path(self._current_directory, "test_in")
        result_path = self._join_path(to_path, "test_text.txt")
        self.assertRemoveTestFiles(test_path, to_path, result_path)
        self.assertCreateTestFiles(test_path, to_path)

        self.assertNotExists(result_path)

        self.file_copy(test_path, to_path)
        self.assertExists(result_path)
        self.assertExists(test_path)

        self.assertFalse(self.file_copy(test_path, to_path))

        self.assertRemoveTestFiles(test_path, to_path)
        self.assertFalse(self.file_copy(to_path, test_path))

    def test_file_rename(self):
        rename = "test_text_2"
        test_path = self._join_path(self._current_directory, "test_text.txt")
        rename_path = self._join_path(self._current_directory, f"{rename}.txt")
        self.assertRemoveTestFiles(test_path, rename_path)
        self.assertCreateTestFiles(test_path)

        self.assertNotExists(rename_path)

        self.file_rename(test_path, rename)
        self.assertNotExists(test_path)
        self.assertExists(rename_path)

        self.file_create(self._current_directory, "test_text", "text_body")
        self.assertFalse(self.file_rename(test_path, rename))

        self.assertRemoveTestFiles(test_path, rename_path)

    def test_file_duplicate_check(self):
        test_path = self._join_path(self._current_directory, "test.txt")
        test_check_path = self._join_path(self._current_directory, "test(1).txt")
        self.assertRemoveTestFiles(test_path, test_check_path)
        self.assertCreateTestFiles(test_path)

        test_check_ok_path = self.file_duplicate_check(test_path)
        self.assertEqual(test_check_path, test_check_ok_path)

        self.file_remove(test_path, True)

        test_check_ok_path = self.file_duplicate_check(test_path)
        self.assertEqual(test_path, test_check_ok_path)


if __name__ == "__main__":
    unittest.main()
