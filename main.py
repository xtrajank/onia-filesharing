'''main.py is designed to launch the application'''
'''onia is an application designed to show my understanding of both aspects of how computers can talk to each other, and how to keep files secure while transferring'''
'''server has to be online and ready to receive to establish port and socket, then client can establish their connection and send the file'''

from tkinter import *
import tkinter.font as tkFont
from send import Send
from receive import Receive

def main():
    #launch app; name, window size, color
    root = Tk()
    root.title('onia')
    root.geometry('450x560+500+200')
    root.configure(bg='black')

    #set main font
    main_font = tkFont.Font(family= 'Arial Black', size = 12, weight = tkFont.NORMAL)

    #home frame
    home_frame = Frame(root, bg='black')
    home_frame.pack(fill='both', expand=True)

    #display title of app
    main_title = Label(home_frame, text = 'onia file transfer', font=(main_font, 35, 'bold'), fg = 'white', bg = 'black')
    main_title.place(relx=0.5, rely=0.15, anchor=CENTER)

    #recieve
    receive=Receive(root)
    receiveb=Button(root, text='RECIEVE FILE', command=receive.window, font=(main_font, 18, 'bold'), bg='black', fg='white', bd=0)
    receiveb.place(relx=0.26, rely=0.7)

    #send
    send=Send(root, receive.hostname)
    sendb=Button(root, text='SEND FILE', command=send.window, font=(main_font, 18, 'bold'), bg='black', fg='white', bd=0)
    sendb.place(relx=0.3, rely=0.5)

    root.mainloop()

if __name__ == '__main__':
    main()