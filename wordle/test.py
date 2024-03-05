from frontend import Frontend
from frontend.keyboard import Key
from tkinter import Tk

handle = lambda x: None
root = Tk()
key = Key(root, 'a', handle)
root.mainloop()