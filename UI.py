from Tkinter import *
import tkFont
import socket


def act(): # defines an event function - for click of button
    print "I-M-pressed"
	
root = Tk(className ="Server GUI")
frame_img = Frame(root)
frame_btn = Frame(root)
frame_img.pack( side = LEFT)
frame_btn.pack( side = RIGHT)

helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
frame_btn.rowconfigure((0,4), weight=1)  # make buttons stretch when
frame_btn.columnconfigure((0,2), weight=1)  # when window is resized

#show local ip address
myaddr=socket.gethostbyname_ex(socket.gethostname())[2][0]
label_ip = Label(frame_btn, text="IP:"+myaddr, fg="dark green",font=helv36)
label_ip.grid(row=0, column=1, columnspan=2)

#a label to split the label_ip and the button below
label = Label(frame_btn,font=helv36)
label.grid(row=1, column=1, columnspan=2)

#forward button
button_fwd = Button(frame_btn,text="Forward",borderwidth=4, command=act, height = 2, width = 20,font=helv36) # create & configure widget 'button"
button_fwd.grid(row=2, column=1, columnspan=2)

#backward button
button_bwd = Button(frame_btn,text="Backward",borderwidth=4,command=act, height = 2, width = 20,font=helv36) # create & configure widget 'button"
button_bwd.grid(row=4, column=1, columnspan=2)

#left button
button_left = Button(frame_btn,text="Left",borderwidth=4,command=act, height = 2, width = 10,font=helv36) # create & configure widget 'button"
button_left.grid(row=3, column=0, columnspan=2)

#right button
button_right = Button(frame_btn,text="Right",borderwidth=4,command=act, height = 2, width = 10,font=helv36) # create & configure widget 'button"
button_right.grid(row=3, column=2, columnspan=2)


width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(str(width) + "x" + str(height))
root.mainloop()