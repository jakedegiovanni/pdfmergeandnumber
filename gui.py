import typing

import tkscrolledframe as tksf
import tkinter as tk
from tkinter import filedialog as fd

import merge


class Application(tk.Frame):
    quit: tk.Button
    import_files: tk.Button
    merge_and_save: tk.Button
    scroll_frame: tksf.ScrolledFrame
    file_container: tk.Frame
    scrollbar: tk.Scrollbar

    files: typing.Set
    to_save: typing.List

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.files = set()
        self.to_save = []

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

        self.scroll_frame = tksf.ScrolledFrame(self.master)
        self.scroll_frame.pack(side="top", expand=True, fill="both")
        self.scroll_frame.bind_scroll_wheel(self.master)
        self.scroll_frame.bind_arrow_keys(self.master)

        self.file_container = self.scroll_frame.display_widget(tk.Frame)

    # https://stackoverflow.com/questions/44887576/how-can-i-create-a-drag-and-drop-interface
    def draggable(self, widget: tk.Widget):
        widget.bind("<Button-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        # you could use this method to create a floating window
        # that represents what is being dragged.
        pass

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, event):
        widget: tk.Widget = event.widget

        x, y = widget.winfo_pointerxy()
        target: tk.Widget = event.widget.winfo_containing(x, y)

        widget_container = widget.nametowidget(widget.winfo_parent())
        target_container = target.nametowidget(target.winfo_parent())

        widget_container_grid_info = widget_container.grid_info()
        target_container_grid_info = target_container.grid_info()

        widget_grid_keys = widget_container_grid_info.keys()
        if "row" not in widget_grid_keys or "column" not in widget_grid_keys:
            return

        target_grid_keys = target_container_grid_info.keys()
        if "row" not in target_grid_keys or "column" not in target_grid_keys:
            return

        widget_children = widget_container.winfo_children()
        if len(widget_children) < 3 or "text" not in widget_children[0].keys():
            return

        target_children = target_container.winfo_children()
        if len(target_children) < 3 or "text" not in target_children[0].keys():
            return

        try:
            widget_container.grid(row=target_container_grid_info["row"], column=target_container_grid_info["column"])
            target_container.grid(row=widget_container_grid_info["row"], column=widget_container_grid_info["column"])

            widget_children[0]["text"] = target_container_grid_info["row"] + 1
            target_children[0]["text"] = widget_container_grid_info["row"] + 1

            temp = self.to_save[target_container_grid_info["row"]]
            self.to_save[target_container_grid_info["row"]] = self.to_save[widget_container_grid_info["row"]]
            self.to_save[widget_container_grid_info["row"]] = temp
        except Exception as e:
            print(e)

    def save(self):
        f = fd.asksaveasfile(mode="wb", filetypes=[("PDF Files", ".pdf")])
        if f is None:
            return

        merge.merge_and_number(self.to_save, f)

        f.close()

        for x in self.file_container.winfo_children():
            x.destroy()

        self.to_save = []

    def files_chooser(self):
        file_paths = fd.askopenfilenames(filetypes=[("PDF Files", ".pdf")])
        self.files.update(file_paths)
        self.to_save = self.to_save + ([None] * len(file_paths))
        self.display_files()

    def display_files(self):
        if len(self.files) == 0:
            return

        for x in self.file_container.winfo_children():
            x.destroy()

        for i, f in enumerate(self.files):
            container = tk.Frame(self.file_container, borderwidth=2, relief="sunken")

            pos = tk.Label(container, text=f"{i + 1}")
            pos.grid(row=0, column=0)

            label = tk.Label(container, text=f)
            label.grid(row=0, column=1)
            self.draggable(label)

            remove = tk.Button(master=container)
            remove["text"] = "Delete"
            remove["command"] = self.remove_file(f, container)
            remove.grid(row=0, column=2)

            self.to_save[i] = f

            container.grid(row=i)

    def remove_file(self, file, container):
        def inner_func():
            self.files.remove(file)
            self.to_save.remove(file)
            container.destroy()

        return inner_func


def launch() -> Application:
    root = tk.Tk()
    root.geometry("500x500")
    return Application(master=root)
