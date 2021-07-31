import typing

import tkinter as tk
from tkinter import filedialog as fd

import merge


class Application(tk.Frame):
    quit: tk.Button
    import_files: tk.Button
    merge_and_save: tk.Button
    file_container: tk.LabelFrame

    files: typing.Set

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.files = set()

    def create_widgets(self):
        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit.grid(row=0, column=0)

        self.import_files = tk.Button(self)
        self.import_files["text"] = "Open files"
        self.import_files["command"] = self.files_chooser
        self.import_files.grid(row=0, column=1)

        self.merge_and_save = tk.Button(self)
        self.merge_and_save["text"] = "Merge, Number and Save"
        self.merge_and_save["command"] = self.save
        self.merge_and_save.grid(row=0, column=2)

        self.file_container = tk.LabelFrame(self.master, text="Selected files for merging:")
        self.file_container.pack(side="top", fill="both", expand="yes")

    def save(self):
        f = fd.asksaveasfile(mode="wb", filetypes=[("PDF Files", ".pdf")])
        if f is None:
            return

        files = [x.winfo_children()[1]["text"] for x in self.file_container.winfo_children()]
        merge.merge_and_number(files, f)

        f.close()

    def files_chooser(self):
        file_paths = fd.askopenfilenames(filetypes=[("PDF Files", ".pdf")])
        self.files.update(file_paths)
        self.display_files()

    def display_files(self):
        if len(self.files) == 0:
            return

        for x in self.file_container.winfo_children():
            x.destroy()

        for i, f in enumerate(self.files):
            container = tk.Frame(self.file_container)

            pos = tk.Label(container, text=f"{i}")
            pos.grid(row=0, column=0)

            label = tk.Label(container, text=f)
            label.grid(row=0, column=1)

            remove = tk.Button(master=container)
            remove["text"] = "Delete"
            remove["command"] = self.remove_file(f, container)
            remove.grid(row=0, column=2)

            container.pack()

    def remove_file(self, file, container):
        def inner_func():
            self.files.remove(file)
            container.destroy()

        return inner_func


def launch() -> Application:
    root = tk.Tk()
    root.geometry("500x500")
    return Application(master=root)
