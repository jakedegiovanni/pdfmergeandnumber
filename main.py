import merge
import gui


def launch():
    app = gui.launch(merge.merge_and_number)
    app.mainloop()


if __name__ == "__main__":
    launch()
