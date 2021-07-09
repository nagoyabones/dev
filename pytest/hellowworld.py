import shutil
import os
import re
import tkinter
from tkinter import filedialog
from tkinter import messagebox


class HellowWorld:
    def main(self, int_):
        return int_ + 1


class DirectoryOperator:
    def directory_select(self, init_path, title_text):
        root = tkinter.Tk()
        root.withdraw()
        dic_path = tkinter.filedialog.askdirectory(
            title=title_text, initialdir=init_path
        )
        return dic_path

    def directory_create(self, create_dic_path, create_dic_name):
        new_dic_path = create_dic_path + "\\" + create_dic_name
        os.makedirs(new_dic_path, exist_ok=True)

    def directory_remove(self, target_path):
        ret = messagebox.askyesno("確認", "フォルダを削除しますか？")
        if ret:
            shutil.rmtree(target_path)

    def directory_move(self, move_dic_paths, to_dir_path):
        for file_path in move_dic_paths:
            if os.path.exists(file_path) and os.path.exists(to_dir_path):
                shutil.move(file_path, to_dir_path)
            else:
                print("no exists")

    def directory_copy(self, copy_dic_paths, to_dir_path):
        for file_path in copy_dic_paths:
            if os.path.exists(file_path) and os.path.exists(to_dir_path):
                shutil.copy(file_path, to_dir_path)
            else:
                print("no exists")


class FileOperator:
    def files_select(self, init_path, title_text):
        root = tkinter.Tk()
        root.withdraw()
        file_type = [("テキストファイル", "*.txt")]
        select_path = filedialog.askopenfilenames(
            title=title_text, filetypes=file_type, initialdir=init_path, multiple=True
        )
        print(select_path)
        return select_path

    def file_create(self, create_dic_path, file_name, file_body):
        path = create_dic_path + "\\" + file_name + ".txt"
        f = open(path, "w")
        f.write(file_body)
        f.close()

    def files_remove(self, target_paths):
        ret = messagebox.askyesno("確認", "ファイルを削除しますか？")
        if ret:
            for file_path in target_paths:
                os.remove(file_path)

    def files_move(self, move_file_paths, to_dir_path):
        for file_path in move_file_paths:
            if os.path.exists(file_path) and os.path.exists(to_dir_path):
                shutil.move(file_path, to_dir_path)
            else:
                print("no exists")

    def files_copy(self, copy_file_paths, to_dir_path):
        for file_path in copy_file_paths:
            if os.path.exists(file_path) and os.path.exists(to_dir_path):
                shutil.copy(file_path, to_dir_path)
            else:
                print("no exists")

    def files_rename(self, base_file_path, rename_file_name):
        file_name, ext = os.path.splitext(os.path.basename(base_file_path))

        rename_file_path = base_file_path.replace(
            file_name + ext, rename_file_name + ext
        )
        use_file_path = self.files_duplicate(rename_file_path)
        os.rename(base_file_path, use_file_path)

    def files_duplicate(self, file_path, count=1):

        if os.path.exists(file_path):

            file_name, ext = os.path.splitext(os.path.basename(file_path))
            tail_num_split_file_name = re.sub(r"\(\d+\)$", "", file_name)

            tail = "(" + str(count) + ")"

            rename_file_path = file_path.replace(
                file_name + ext, tail_num_split_file_name + tail + ext
            )

            return self.files_duplicate(rename_file_path, count + 1)

        else:
            return file_path


if __name__ == "__main__":
    init_dir = os.path.abspath(os.path.dirname(__file__))
    f = FileOperator()
    d = DirectoryOperator()

    file_paths = f.files_select(init_dir, "リネームするファイルを選択")
