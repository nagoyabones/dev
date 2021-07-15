import logging
import tkinter
import shutil
import sys
import os
import re

import tkinter.filedialog


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
            "%(asctime)s:[%(levelname)s] %(message)s", datefmt="%b %d %H:%M:%S",
        )
        sh.setFormatter(fmt)

        lev = {
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }.get(level)

        logger.setLevel(lev)
        logger.addHandler(sh)

        logger.log(lev, text)


class SetTkinter:
    def _set_tkinter(self):
        if hasattr(self, "_window") is False:
            self._window = tkinter.Tk()
            self._window.withdraw()
        if hasattr(self, "tkinter") is False:
            self.tkinter = tkinter


class DirectoryOperator(OsPathAlternative, Logger, SetTkinter):
    def directory_select(self, title):
        self._set_tkinter()
        select_path = self.tkinter.filedialog.askdirectory(
            title=title, initialdir=self._current_directory
        )
        self.logger_output("DEBUG", f'Select directory path "{select_path}".')
        return select_path

    def directory_create(self, create_dir_path, create_dir_name):
        new_dir_path = self._join_path(create_dir_path, create_dir_name)
        os.makedirs(new_dir_path, exist_ok=True)
        self.logger_output("INFO", f'Create directory "{new_dir_path}".')

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
                self.logger_output(
                    "INFO", f'Move directory "{move_dir_path}" to "{to_new_dir_path}".'
                )
            else:
                self.logger_output("DEBUG", "Already exists.")
                return False
        else:
            self.logger_output("DEBUG", "Not exists.")
            return False

    def directory_copy(self, copy_dir_path, to_dir_path):
        if self._is_exists(copy_dir_path) and self._is_exists(to_dir_path):
            to_new_dir_path = self._join_path(
                to_dir_path, os.path.basename(copy_dir_path)
            )

            if self._is_not_exists(to_new_dir_path):
                shutil.copytree(copy_dir_path, to_new_dir_path)
            else:
                self.logger_output("DEBUG", "Already exists.")
                return False
        else:
            self.logger_output("DEBUG", "Not exists.")
            return False

    def directory_duplicate_check(self, dir_path, count=1):
        if self._is_exists(dir_path):

            dir_name = os.path.basename(dir_path)
            tail_num_split_dir_name = re.sub(r"\(\d+\)$", "", dir_name)
            tail = "(" + str(count) + ")"

            rename_dir_path = dir_path[::-1].replace(
                dir_name[::-1], (tail_num_split_dir_name + tail)[::-1], 1
            )

            return self.directory_duplicate_check(rename_dir_path[::-1], count + 1)

        else:
            return dir_path


class FileOperator(OsPathAlternative, Logger, SetTkinter):
    def files_select(self, title):
        self._set_tkinter()
        file_type = [("テキストファイル", "*.txt")]
        select_path = self.tkinter.filedialog.askopenfilenames(
            title=title,
            filetypes=file_type,
            initialdir=self._current_directory,
            multiple=True,
        )
        self.logger_output("DEBUG", f'Select file path "{select_path}"')
        return select_path

    def file_create(self, create_dir_path, file_name, file_body):
        file_path = self._join_path(create_dir_path, f"{file_name}.txt")

        if self._is_not_exists(file_path):
            self.logger_output("INFO", f'Create text file "{file_path}".')

            with open(file_path, "w") as f:
                f.write(file_body)

        else:
            self.logger_output("DEBUG", "Same name text files already exists.")
            return False

    def file_remove(self, file_path, fail_safe=False):
        if fail_safe and self._is_exists(file_path):
            os.remove(file_path)
            self.logger_output("INFO", f'Remove "{file_path}".')

    def file_move(self, move_file_path, to_dir_path):
        if self._is_exists(move_file_path) and self._is_exists(to_dir_path):
            to_new_file_path = self._join_path(
                to_dir_path, os.path.basename(move_file_path)
            )
            if self._is_not_exists(to_new_file_path):
                shutil.move(move_file_path, to_new_file_path)
                self.logger_output(
                    "INFO",
                    f'Moved directory "{move_file_path}" to "{to_new_file_path}".',
                )
            else:
                self.logger_output("DEBUG", "Already exists.")
                return False
        else:
            self.logger_output("DEBUG", "Not exists.")
            return False

    def file_copy(self, copy_file_path, to_dir_path):
        if self._is_exists(copy_file_path) and self._is_exists(to_dir_path):
            to_new_file_path = self._join_path(
                to_dir_path, os.path.basename(copy_file_path)
            )
            if self._is_not_exists(to_new_file_path):
                shutil.copy(copy_file_path, to_new_file_path)
                self.logger_output(
                    "INFO",
                    f'Copied directory "{copy_file_path}" to "{to_new_file_path}".',
                )
            else:
                self.logger_output("DEBUG", "Already exists.")
                return False
        else:
            self.logger_output("DEBUG", "Not exists.")
            return False

    def file_rename(self, base_file_path, rename_file_name):
        file_name, ext = os.path.splitext(os.path.basename(base_file_path))

        rename_file_path = base_file_path.replace(
            file_name + ext, rename_file_name + ext
        )
        if self._is_not_exists(rename_file_path):
            os.rename(base_file_path, rename_file_path)
            self.logger_output(
                "INFO", f'Renamed "{base_file_path}" to "{rename_file_path}".',
            )
        else:
            self.logger_output("DEBUG", "Already exists.")
            return False

    def file_duplicate_check(self, file_path, count=1):

        if self._is_exists(file_path):

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
    d = DirectoryOperator()
    f = FileOperator()

    # file_paths = d.directory_select("フォルダを選択")
    file_paths = f.files_select("フォルダを選択")
