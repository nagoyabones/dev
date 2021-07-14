import unittest
import os
from unittest import mock
import tkinter

from hellow_world import FileOperator
from hellow_world import DirectoryOperator
from hellow_world import OsPathAlternative
from hellow_world import Logger


class DummyUnittest(unittest.TestCase, OsPathAlternative):
    def assertExists(self, path):
        self.assertTrue(self._is_exists(path))

    def assertNotExists(self, path):
        return self.assertFalse(self._is_exists(path))


class TestOsPathAlternative(unittest.TestCase, DirectoryOperator):
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

    def test_join_path(self):
        self.assertEqual(
            os.path.join(os.path.expanduser("~"), "dev", "pytest"),
            self._join_path(os.path.expanduser("~"), "dev", "pytest"),
        )

    def test__current_directory(self):
        self.assertEqual(
            self._join_path(os.path.expanduser("~"), "dev", "pytest"),
            self._current_directory,
        )


class TestLogger(DummyUnittest, Logger):
    def test_logger_output(self):
        self.logger_output("DEBUG", "Logger test.")


class TestDirectoryOperator(DummyUnittest, DirectoryOperator):
    def setUp(self):
        self.tkinter = mock.MagicMock()

    def test__set_tkinter(self):
        del self.tkinter
        self.assertFalse(hasattr(self, "_window"))
        self.assertFalse(hasattr(self, "tkinter"))
        self._set_tkinter()
        self.assertIsInstance(self._window, tkinter.Tk)
        self.assertIs(self.tkinter, tkinter)

    def test_directory_select(self):
        def askdirectory(title, initialdir):
            return initialdir

        self.tkinter.filedialog.askdirectory = askdirectory
        self.assertEqual(self._current_directory, self.directory_select())

    def test_directory_create(self):
        test_path = self._join_path(self._current_directory, "test")
        self.assertNotExists(test_path)
        self.directory_create(self._current_directory, "test")
        self.assertTrue(os.path.exists(test_path))
        self.directory_remove(test_path, True)

    def test_directory_remove(self):
        test_path = self._join_path(self._current_directory, "test")
        self.directory_create(self._current_directory, "test")
        self.assertTrue(os.path.exists(test_path))
        self.directory_remove(test_path, True)
        self.assertFalse(os.path.exists(test_path))

    def test_directory_move(self):
        test_path = self._join_path(self._current_directory, "test")
        target_path = self._join_path(self._current_directory, "target")
        result_path = self._join_path(test_path, "target")
        self.directory_create(self._current_directory, "test")
        self.directory_create(self._current_directory, "target")

        self.assertTrue(os.path.exists(test_path))
        self.assertTrue(os.path.exists(target_path))

        self.directory_move(target_path, test_path)

        self.assertFalse(os.path.exists(target_path))
        self.assertTrue(os.path.exists(result_path))

        self.assertFalse(self.directory_move(target_path, test_path))

        self.directory_create(self._current_directory, "target")
        self.assertFalse(self.directory_move(target_path, test_path))

        self.directory_remove(test_path, True)
        self.assertFalse(os.path.exists(test_path))

    def test_directory_copy(self):
        test_path = self._join_path(self._current_directory, "test")
        target_path = self._join_path(self._current_directory, "target")
        result_path = self._join_path(test_path, "target")
        self.directory_create(self._current_directory, "test")
        self.directory_create(self._current_directory, "target")

        self.assertTrue(os.path.exists(test_path))
        self.assertTrue(os.path.exists(target_path))

        self.directory_copy(target_path, test_path)

        self.assertTrue(os.path.exists(target_path))
        self.assertTrue(os.path.exists(result_path))

        self.assertFalse(self.directory_copy(target_path, test_path))

        self.directory_remove(test_path, True)
        self.directory_remove(target_path, True)
        self.assertFalse(self.directory_copy(target_path, test_path))

    def test_directory_duplicate_check(self):
        test_path = self._join_path(self._current_directory, "test")
        print(self.directory_duplicate_check(test_path))


class TestFileOperator(DummyUnittest, FileOperator):

    """
    def test_files_select(self):
        path = self.files_select("test_file_select")
        print(path)

    def test_file_create(self):
        d = DirectoryOperator()
        dic_path = d.directory_select("test_directory_select")
        self.file_create(dic_path, "ファイルテスト", "テスト")

    def test_file_remove(self):
        file_paths = self.files_select("ファイルを選択")
        if file_paths != "":
            ret = messagebox.askyesno("確認", "ファイルを削除しますか？")
            for file in file_paths:
                self.file_remove(file, ret)

    def test_file_move(self):
        d = DirectoryOperator()
        file_paths = self.files_select("ファイルを選択")
        if file_paths != "":
            to_dic_path = d.directory_select("test_directory_select")
            if to_dic_path != "":
                for file in file_paths:
                    self.file_move(file, to_dic_path)

    def test_file_copy(self):
        d = DirectoryOperator()
        file_paths = self.files_select("ファイルを選択")
        if file_paths != "":
            to_dic_path = d.directory_select("test_directory_select")
            if to_dic_path != "":
                for file in file_paths:
                    self.file_copy(file, to_dic_path)

    def test_file_rename(self):
        file_paths = self.files_select("ファイルを選択")
        for file in file_paths:
            self.file_rename(file, "test")

    def test_file_duplicate_check(self):
        file_paths = self.files_select("ファイルを選択")

        for file in file_paths:
            print(self.file_duplicate_check(file))
    """


if __name__ == "__main__":
    unittest.main()
