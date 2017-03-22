#importing modules required
from ttk import *
from Tkinter import *
from PIL import Image, ImageTk
import tkFont
import cv2
import os
import numpy as np
import socket
import cv2
import threading
import pickle

# TCP address and port
TCP_IP = socket.gethostbyname_ex(socket.gethostname())[2][0]
TCP_PORT = 5001

# AF_INET -> IPv4, SOCK_STREAM -> TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((TCP_IP, TCP_PORT))
print 'Socket bind complete'
server.listen(5)
print 'Socket now listening'

# flag for terminating
EXIT = False
pickle.dump(EXIT, open("exit_server.txt", "w"))

#function to receive image from odroid
def recvall(server, count):
    buf = b''
    while count:
        newbuf = server.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#function to show the received image
def show_vid(): 
    label_img = Label(frame_img)
    label_img.grid(row=0, column=0, padx=100, pady=5)       
    
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    pic = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    label_img.imgtk = imgtk
    label_img.configure(image=imgtk)
    label_img.after(10, show_vid)   
	
    if cv2.waitKey(5) & 0xFF == 27:
            print("Exit the program")
            EXIT = True
            pickle.dump(EXIT, open("exit_server.txt", "w"))

#function to set up the control UI
def ui_init():
    helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
    frame_btn.rowconfigure((0,4), weight=1)  # make buttons stretch when
    frame_btn.columnconfigure((0,2), weight=1)  # when window is resized

    #show local ip address
    label_ip = Label(frame_btn, text="IP:"+TCP_IP, fg="dark green",font=helv36)
    label_ip.grid(row=0, column=1, columnspan=2)

    #a label to split the label_ip and the button below
    label = Label(frame_btn,font=(None, 36), height=3, width=20)
    label.grid(row=1, column=1, columnspan=2)

    #forward button
    button_fwd = Button(frame_btn,text="Forward",borderwidth=4, command=forward, height = 2, width = 20,font=helv36) 
    button_fwd.grid(row=2, column=1, columnspan=2)

    #backward button
    button_bwd = Button(frame_btn,text="Backward",borderwidth=4,command=backward, height = 2, width = 20,font=helv36) 
    button_bwd.grid(row=4, column=1, columnspan=2)

    #left button
    button_left = Button(frame_btn,text="Left",borderwidth=4,command=left, height = 2, width = 10,font=helv36)
    button_left.grid(row=3, column=0, columnspan=2)

    #right button
    button_right = Button(frame_btn,text="Right",borderwidth=4,command=right, height = 2, width = 10,font=helv36) 
    button_right.grid(row=3, column=2, columnspan=2)

#functions for click reactions of buttons
def forward(): 
    print "fwd-pressed"
    conn.send('F')
    print "fwd-send"

def backward(): 
    print "bwd-pressed"
    conn.send('B')
    print "bwd-send"

def left(): 
    print "left-pressed"
    conn.send('L')
    print "left-send"
    
def right(): 
    print "right-pressed"
    conn.send('R')
    print "right-send"  


if __name__ == '__main__':
    conn, addr = server.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    root = Tk(className ="Server GUI")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(str(width) + "x" + str(height))
    
    frame_img = Frame(root)
    frame_btn = Frame(root)
    frame_img.pack(side = LEFT)
    frame_btn.pack(side = RIGHT)
    
    chatThread = threading.Thread(name='chat', target=ui_init)
    imageThread = threading.Thread(name='image', target=show_vid)
    chatThread.start()
    print 'chatThread created'
    imageThread.start()
    print 'imageThread created'
	
    if cv2.waitKey(5) & 0xFF == 27:
            print("Client disconnect!")
            Leaving = pickle.load(open("exit_server.txt", "r"))
            if Leaving:
               os.exit()

    root.mainloop()                                  #keeps the application in an infinite loop so it works continuosly

server.close()
cv2.destroyAllWindows() 