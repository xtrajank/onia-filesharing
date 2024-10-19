'''Controls the client side of the platform. Opens the send window, grabs the file and sends it.
Encodes the file name for security. Then, once accepted by the correct desitnation, decodes the filename and sends it to that server.'''

from tkinter import *
from tkinter import filedialog, messagebox
import socket
import os
import threading

class Send:
    def __init__(self, parent, server_ip):
        self.parent = parent
        self.server_ip = server_ip
        self.port = 8880
        self.filename = None

    def window(self):
        '''Opens sending window'''
        window = Toplevel(self.parent)
        window.title('Send')
        window.geometry('450x560+500+200')
        window.configure(bg='black')

        # Main label
        send_label = Label(window, text='Send File', fg='white', bg='black', font=('Arial Black', 30, 'bold'))
        send_label.pack(pady=30)

        # Host label
        host_label = Label(window, text=f'HOST IP: {self.server_ip}', fg='white', bg='black', font=('Arial Black', 12))
        host_label.pack(pady=5)

        # File selection button
        file_button = Button(window, text='+ File', command=self.select_file, fg='white', bg='black', font=('Arial Black', 20), bd=0)
        file_button.place(rely=0.5, relx=0.4)

        # Start sending button
        self.send_button = Button(window, text="Send File", command=self.start_sending_thread, fg='white', bg='green', font=('Arial Black', 20), bd=0)
        self.send_button.place(rely=0.7, relx=0.35)

    def select_file(self):
        '''Opens up the file directory for correct operating system.
        Displays dialog box so user knows correct file was selected.'''
        self.file = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File')
        if self.file:
            self.filename = os.path.basename(self.file)
            messagebox.showinfo('File Selected', f'Selected File: {self.filename}')
        self.window()

    def start_sending_thread(self):
        '''sends the file in its own thread, for efficiency'''
        if self.file:
            self.send_button.config(state=DISABLED) # while file is being sent, send button is turned off so user does not overload the server.
            threading.Thread(target=self.connect).start()
        else:
            messagebox.showwarning('No File Selected', 'Please select file before sending.')

    def connect(self):
        '''connects to server, sends the file name encoded, then sends file by 1024 bit increments'''
        try:
            # Defining the server socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_ip, self.port))
            print(f'Connected to server: {self.server_ip}')

            # Establishes the file name and encodes it to be sent
            filename = os.path.basename(self.file)
            sock.sendall(filename.encode('utf-8') + b'\n') # newline added for simpler file name distinction

            # Send the file
            with open(self.file, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    sock.send(file_data)
                    file_data = file.read(1024)


            print("File sent successfully.")
            messagebox.showinfo('Success', 'File sent successfully!')

        except Exception as e:
            print(f'Error: {e}')
            messagebox.showerror('Error', f'Failed to send file: {e}')

        finally:
            sock.close()
            self.send_button.config(state=NORMAL) # reestablishes the send button to be used for another file
