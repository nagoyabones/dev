import shutil
import os
import re
import tkinter
from tkinter import filedialog


class DirectoryOperator:
    def directory_select(
        self, title_text, init_path=os.path.abspath(os.path.dirname(__file__))
    ):
        root = tkinter.Tk()
        root.withdraw()
        dir_path = tkinter.filedialog.askdirectory(
            title=title_text, initialdir=init_path
        )
        return dir_path

    def directory_create(self, create_dir_path, create_dir_name):
        new_dir_path = os.path.join(create_dir_path, create_dir_name)
        check_ok_path = self.directory_duplicate_check(new_dir_path)
        os.makedirs(check_ok_path, exist_ok=True)

    def directory_remove(self, target_path, ret=False):
        if ret:
            shutil.rmtree(target_path)

    def directory_move(self, move_dir_path, to_dir_path):
        if os.path.exists(move_dir_path) and os.path.exists(to_dir_path):
            to_dir_path = os.path.join(to_dir_path, os.path.basename(move_dir_path))
            check_ok_path = self.directory_duplicate_check(to_dir_path)
            shutil.move(move_dir_path, check_ok_path)
        else:
            print("no exists")

    def directory_copy(self, copy_dir_path, to_dir_path):
        if os.path.exists(copy_dir_path) and os.path.exists(to_dir_path):
            to_dir_path = os.path.join(to_dir_path, os.path.basename(copy_dir_path))
            check_ok_path = self.directory_duplicate_check(to_dir_path)
            shutil.copytree(copy_dir_path, check_ok_path)

        else:
            print("no exists")

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
        path = os.path.join(create_dir_path, f"{file_name}.txt")

        check_ok_path = self.file_duplicate_check(path)
        with open(check_ok_path) as f:
            f.write(file_body)

    def file_remove(self, file_path, ret=False):
        if ret:
            os.remove(file_path)

    def file_move(self, move_file_path, to_dir_path):
        if os.path.exists(move_file_path) and os.path.exists(to_dir_path):
            check_ok_path = self.file_duplicate_check(
                os.path.join(to_dir_path, os.path.basename(move_file_path))
            )
            shutil.move(move_file_path, check_ok_path)
        else:
            print("no exists")

    def file_copy(self, copy_file_path, to_dir_path):
        if os.path.exists(copy_file_path) and os.path.exists(to_dir_path):
            check_ok_path = self.file_duplicate_check(
                os.path.join(to_dir_path, os.path.basename(copy_file_path))
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
