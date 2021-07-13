import unittest
import os
from unittest import mock
import tkinter

from hellow_world import FileOperator
from hellow_world import DirectoryOperator


class TestDirectoryOperator(unittest.TestCase, DirectoryOperator):
    def setUp(self):
        self.tkinter = mock.MagicMock()

    def test__current_directory(self):
        self.assertEqual(
            os.path.join(os.path.expanduser("~"), "dev", "pytest"),
            self._current_directory,
        )

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
        test_path = os.path.join(self._current_directory, "test")
        self.assertFalse(os.path.exists(test_path))
        self.directory_create(self._current_directory, "test")
        self.assertTrue(os.path.exists(test_path))
        self.directory_remove(test_path)

    """
    def test_directory_remove(self):
        path = self.directory_select("test_directory_select")
        if path != "":
            ret = messagebox.askyesno("確認", "フォルダを削除しますか？")
            self.directory_remove(path, ret)

    def test_directory_move(self):
        move_dic_path = self.directory_select("test_directory_select")

        if move_dic_path != "":
            to_dic_path = self.directory_select("test_directory_select")
            if to_dic_path != "":
                self.directory_move(move_dic_path, to_dic_path)

    def test_directory_copy(self):
        copy_dic_path = self.directory_select("test_directory_select")

        if copy_dic_path != "":
            to_dic_path = self.directory_select("test_directory_select")
            if to_dic_path != "":
                self.directory_copy(copy_dic_path, to_dic_path)

    def test_directory_duplicate_check(self):
        dic_path = self.directory_select("ファイルを選択")
        print(self.directory_duplicate_check(dic_path))
    """


class TestFileOperator(unittest.TestCase, FileOperator):
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
