import socket
import threading
import tkinter as tk
from tkinter import messagebox

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente")
        self.root.geometry("400x500")
        
        # Campos de entrada para host, porta, username e palavra passe
        self.label_host = tk.Label(root, text="Host:")
        self.label_host.pack()
        self.entry_host = tk.Entry(root)
        self.entry_host.pack()
        
        self.label_port = tk.Label(root, text="Porta:")
        self.label_port.pack()
        self.entry_port = tk.Entry(root)
        self.entry_port.pack()
        
        self.label_username = tk.Label(root, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()
        
        # Botões de controle
        self.button_connect = tk.Button(root, text="Ligar", command=self.connect_server)
        self.button_connect.pack()

        # Caixa de texto para exibir mensagens e botões para MI
        self.message_display = tk.Text(root, height=10, state="disabled")
        self.message_display.pack()

        self.label_dest = tk.Label(root, text="Destinatário (para MI):")
        self.label_dest.pack()
        self.entry_dest = tk.Entry(root)
        self.entry_dest.pack()

        self.entry_message = tk.Entry(root)
        self.entry_message.pack()
        self.button_send = tk.Button(root, text="Enviar Mensagem", command=self.send_message)
        self.button_send.pack()

        self.button_exit = tk.Button(root, text="Sair", command=root.quit)
        self.button_exit.pack()
        
        self.client_socket = None

    def connect_server(self):
        host = self.entry_host.get()
        port = int(self.entry_port.get())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        username = self.entry_username.get()
        self.client_socket.send(username.encode())
        threading.Thread(target=self.receive_messages).start()
        messagebox.showinfo("Cliente", "Conectado ao servidor")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.message_display.config(state="normal")
                    self.message_display.insert("end", message + "\n")
                    self.message_display.config(state="disabled")
            except:
                messagebox.showerror("Erro", "Conexão perdida")
                self.client_socket.close()
                break

    def send_message(self):
        message = self.entry_message.get()
        dest = self.entry_dest.get()
        if message:
            if dest:  # Enviar como MI
                message = f"@{dest}: {message}"
            self.client_socket.send(message.encode())
            self.entry_message.delete(0, "end")

# Inicializar a aplicação do cliente
root = tk.Tk()
app = ClientApp(root)
root.mainloop()
