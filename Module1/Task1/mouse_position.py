from tkinter import *

window = Tk()

#win.geometry("750x250")
def callback(e):
   x= e.x
   y= e.y
   print("Pointer is currently at %d, %d" %(x,y))

window.bind('<Motion>', callback)
window.bind('<Space>', callback)

window.mainloop()