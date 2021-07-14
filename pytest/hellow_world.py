import logging
import tkinter
import shutil
import sys
import os
import re

from tkinter import filedialog


class OsPathAlternative:
    def _is_exists(self, path):
        return os.path.exists(path)

    def _is_not_exists(self, path):
        return False if self._is_exists(path) else True

    def _join_path(self, *path):
        return os.path.join(*path)

    @property
    def _current_directory(self):
        return os.path.abspath(os.path.dirname(__file__))


class Logger:
    def logger_output(self, level, text):
        logger = logging.getLogger(__name__)
        sh = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%S"
        )
        sh.setFormatter(fmt)

        lev = {
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }.get(level)

        print(lev)

        logger.setLevel(lev)
        logger.addHandler(sh)

        logger.log(lev, text)


class DirectoryOperator(OsPathAlternative):
    def _set_tkinter(self):
        if hasattr(self, "_window") is False:
            self._window = tkinter.Tk()
            self._window.withdraw()
        if hasattr(self, "tkinter") is False:
            self.tkinter = tkinter

    def directory_select(self):
        self._set_tkinter()
        return self.tkinter.filedialog.askdirectory(
            title="please select directory", initialdir=self._current_directory
        )

    def directory_create(self, create_dir_path, create_dir_name):
        os.makedirs(self._join_path(create_dir_path, create_dir_name), exist_ok=True)

    def directory_remove(self, target_path, fail_safe=False):
        if fail_safe:
            shutil.rmtree(target_path)

    def directory_move(self, move_dir_path, to_dir_path):
        if self._is_exists(move_dir_path) and self._is_exists(to_dir_path):
            to_new_dir_path = self._join_path(
                to_dir_path, os.path.basename(move_dir_path)
            )
            if self._is_not_exists(to_new_dir_path):
                shutil.move(move_dir_path, to_new_dir_path)
            else:
                print("Already exists.")
                return False
        else:
            print("Not exists.")
            return False

    def directory_copy(self, copy_dir_path, to_dir_path):
        if self._is_exists(copy_dir_path) and self._is_exists(to_dir_path):
            to_new_dir_path = self._join_path(
                to_dir_path, os.path.basename(copy_dir_path)
            )

            if self._is_not_exists(to_new_dir_path):
                shutil.copytree(copy_dir_path, to_new_dir_path)
            else:
                print("Already exists.")
                return False
        else:
            print("Not exists.")
            return False

    def directory_duplicate_check(self, dir_path, count=1):
        if os.path.exists(dir_path):

            dir_name = os.path.basename(dir_path)
            tail_num_split_dir_name = re.sub(r"\(\d+\)$", "", dir_name)
            tail = "(" + str(count) + ")"

            rename_dir_path = dir_path[::-1].replace(
                dir_name[::-1], (tail_num_split_dir_name + tail)[::-1], 1
            )

            return self.directory_duplicate_check(rename_dir_path[::-1], count + 1)

        else:
            return dir_path


class FileOperator:
    def files_select(
        self, title_text, init_path=os.path.abspath(os.path.dirname(__file__))
    ):
        root = tkinter.Tk()
        root.withdraw()
        file_type = [("テキストファイル", "*.txt")]
        select_path = filedialog.askopenfilenames(
            title=title_text, filetypes=file_type, initialdir=init_path, multiple=True
        )
        return select_path

    def file_create(self, create_dir_path, file_name, file_body):
        path = self._join_path(create_dir_path, f"{file_name}.txt")

        check_ok_path = self.file_duplicate_check(path)
        with open(check_ok_path) as f:
            f.write(file_body)

    def file_remove(self, file_path, fail_safe=False):
        if fail_safe:
            os.remove(file_path)

    def file_move(self, move_file_path, to_dir_path):
        if os.path.exists(move_file_path) and os.path.exists(to_dir_path):
            check_ok_path = self.file_duplicate_check(
                self._join_path(to_dir_path, os.path.basename(move_file_path))
            )
            shutil.move(move_file_path, check_ok_path)
        else:
            print("no exists")

    def file_copy(self, copy_file_path, to_dir_path):
        if os.path.exists(copy_file_path) and os.path.exists(to_dir_path):
            check_ok_path = self.file_duplicate_check(
                self._join_path(to_dir_path, os.path.basename(copy_file_path))
            )
            shutil.copy(copy_file_path, check_ok_path)
        else:
            print("no exists")

    def file_rename(self, base_file_path, rename_file_name):
        file_name, ext = os.path.splitext(os.path.basename(base_file_path))

        rename_file_path = base_file_path.replace(
            file_name + ext, rename_file_name + ext
        )
        use_file_path = self.file_duplicate_check(rename_file_path)
        os.rename(base_file_path, use_file_path)

    def file_duplicate_check(self, file_path, count=1):

        if os.path.exists(file_path):

            file_name, ext = os.path.splitext(os.path.basename(file_path))
            tail_num_split_file_name = re.sub(r"\(\d+\)$", "", file_name)

            tail = "(" + str(count) + ")"

            rename_file_path = file_path.replace(
                file_name + ext, tail_num_split_file_name + tail + ext
            )

            return self.file_duplicate_check(rename_file_path, count + 1)

        else:
            return file_path


if __name__ == "__main__":
    f = FileOperator()
    d = DirectoryOperator()

    file_paths = f.files_select("リネームするファイルを選択")
