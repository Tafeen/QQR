# Tray
from pystray import MenuItem as item
import pystray

# Dialog box
from tkinter import Tk, Label, Button, Entry

import pyqrcode
from PIL import ImageTk, Image
from os import path, kill
from pynput import keyboard
from multiprocessing import Process

# Set default paths for images
basepath = path.dirname(__file__) 
tray_icon = path.abspath(path.join(basepath, "tray_icon.png"))
transparent = path.abspath(path.join(basepath, "transparent.ico"))
qr_code = path.abspath(path.join(basepath, "current_qr.png"))


class QRdialog:
    def __init__(self, master):
        self.master = master
        master.title("")
        master.geometry('250x250')
        master.iconbitmap(default=transparent)
        master.lift()
        master.focus_force()
        master.resizable(width=False, height=False)

        def showCode():
            print("Showing new code")
            path = qr_code
            img = Image.open(path)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            self.label = Label(master, image=img)
            self.label.img = img
            self.label.pack()
            

        # Set input
        self.entry = Entry(master, )

        def updateCode(event):

            # Generate QR Code
            print(self.entry.get())
            qr = pyqrcode.create(self.entry.get())
            qr.png(qr_code)
            # Update DialogBox
            master.after(300, showCode)

        master.bind('<Return>', updateCode)

        self.label = Label(
            master, text="Enter text to convert", bg="black", fg="white")
        self.label.pack(side="top", fill="both")

        self.label = self.entry
        self.label.pack(side="top", fill="both")

class SettingsDialog:
    def __init__(self, master):
        self.master = master
        master.title("QQR settings")
        master.geometry('350x200')
        master.iconbitmap(default=transparent)
        master.focus_force()
        master.minsize(350, 200)


        self.label = Label(master, text="Quick QR settings",
                           bg="black", fg="white")
        self.label.pack(side="top", fill="both")

        self.close_button = Button(
            master, text="Close application", command=CloseApp())
        self.close_button.pack()

def ShowSettingsDialog():
    root = Tk()
    SettingsDialog(root)
    root.mainloop()

def ShowQRcode():
    root = Tk()
    QRdialog(root)
    root.mainloop()

def CloseApp():
    global _FINISH
    _FINISH = True
    icon.stop()

# Tray
image = Image.open(tray_icon)
menu = (item('Open Settings', ShowSettingsDialog), item(
    'Generate Code', ShowQRcode), item('End QQR', CloseApp))
icon = pystray.Icon("name", image, "QQR", menu)


def openTray(finish):
    print(finish)
    print("Opening tray")
    icon.run()


# Key listener
def key_listener():

    # The key combination to check
    COMBINATION = {keyboard.Key.cmd, keyboard.KeyCode(char='n')}

    # The currently active modifiers
    current = set()

    def on_press(key):
        if key in COMBINATION:
            current.add(key)
            if all(k in current for k in COMBINATION):
                ShowQRcode()
                current.clear()
        if key == keyboard.Key.esc:
            listener.stop()

    def on_release(key):
        try:
            current.remove(key)
        except KeyError:
            pass

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    p1 = Process(target=key_listener)
    p1.start()
    p2 = Process(target=openTray)
    p2.start()
    # p1.join()
    # p2.join()
    # p1.terminate()
    # p2.terminate()

if __name__ == '__main__':
    main()

