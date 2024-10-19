'''receive.py, establishes the receive window for a server. Once receive initialized, client can send files.
Recieves and decodes file name for security. Then receives the rest of the file in 1024 bits.'''

import socket
import threading
from tkinter import *
from tkinter import filedialog, messagebox

class Receive:
    def __init__(self, parent):
        self.parent = parent
        # Recieve class handles its own hostname and port
        self.hostname = socket.gethostbyname(socket.gethostname())
        self.port = 8880

    def window(self):
        window = Toplevel(self.parent)
        window.title('Receive')
        window.geometry('450x560+500+200')
        window.configure(bg='black')

        # Main label
        receive_label = Label(window, text='Receive File', fg='white', bg='black', font=('Arial Black', 30, 'bold'))
        receive_label.pack(pady=30)

        # Host label
        host_label = Label(window, text=f'HOST IP: {self.hostname}', fg='white', bg='black', font=('Arial Black', 12))
        host_label.pack(pady=5)

        # Start receiving button
        receive_button = Button(window, text="Start Receiving", command=self.start_receiving, fg='white', bg='green', font=('Arial Black', 20), bd=0)
        receive_button.place(rely=0.5, relx=0.21)

    def _receive_until(self, conn, delimiter):
        '''recieves bits until reaches new line delimiter sent with file name. This is to help the system only recieve file name and not file data.'''
        data = bytearray()
        while True:
            part = conn.recv(1)
            if part == delimiter:
                break
            data.extend(part)
        return data


    def start_receiving_thread(self):
        '''recieves the file thread for efficiency'''
        threading.Thread(target=self.start_receiving).start()

    def start_receiving(self):
        '''establishes connection with socket and correct client. Once client sends the file, file name decoded with recieve until function.
        Asks where in directory it will be saved, once selected saves the rest of the data to that location'''
        try:
            # Establish connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.hostname, self.port))
            sock.listen(1)
            print(f"Waiting for connection on {self.hostname}:{self.port}...")

            # Once client is also online, the connection is established and ready to receive
            conn, addr = sock.accept()
            print(f"Connection established with {addr}")

            # Ensures only the file name is received and decoded for security
            filename_bytes = self._receive_until(conn, b'\n')
            filename = filename_bytes.decode('utf-8').strip()
            print(f'Receiving file: {filename}')

            # Opens file directory for server to save file
            save_path = filedialog.asksaveasfilename(initialfile=filename, title="Save Received File", filetypes=[("All Files", "*.*")])

            # Saves file 1024 bit increments
            if save_path:
                with open(save_path, 'wb') as file:
                    file_data = conn.recv(1024)
                    while file_data:
                        file.write(file_data)
                        file_data = conn.recv(1024)

                # Message box to show file saved
                print("File received successfully.")
                messagebox.showinfo('Success', 'File saved successfully!')
            else:
                print('Save operation canceled.')
            
            # Close connection with client
            conn.close()
        
        except Exception as e:
            print(f'An error occured: {e}')

        finally:
            sock.close()