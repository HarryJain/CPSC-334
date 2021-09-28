from tkinter import *
import tkSnack
import os

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

root = Tk()
tkSnack.initializeSnack(root)

snd = tkSnack.Sound()
snd.read('beatles/eleanor_rigby.mp3')
print('playing sound')
snd.play(blocking = 1)
