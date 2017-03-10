#importing modules required
from ttk import *
import Tkinter as tk
import tkFont
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
import socket
import cv2

# TCP address and port
TCP_IP = socket.gethostbyname_ex(socket.gethostname())[2][0]
TCP_PORT = 5001

# AF_INET -> IPv4, SOCK_STREAM -> TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
server.bind((TCP_IP, TCP_PORT))
print 'Socket bind complete'
server.listen(True)
print 'Socket now listening'
conn, addr = server.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

def recvall(server, count):
    buf = b''
    while count:
        newbuf = server.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def show_vid(): 
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    pic = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_vid)	

if __name__ == '__main__':
    root=tk.Tk()                                     #assigning root variable for Tkinter as tk
    lmain = tk.Label(master=root)
    lmain.grid(column=0, rowspan=4, padx=5, pady=5)
    root.title("Odroid Server")                      #you can give any title
    show_vid()
    root.mainloop()                                  #keeps the application in an infinite loop so it works continuosly

server.close()
cv2.destroyAllWindows() 