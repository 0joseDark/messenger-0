import socket
import threading
import tkinter as tk
from tkinter import messagebox

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente")
        self.root.geometry("400x400")
        
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
        
        self.label_password = tk.Label(root, text="Palavra Passe:")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()
        
        # Botões de controle
        self.button_connect = tk.Button(root, text="Ligar", command=self.connect_server)
        self.button_connect.pack()
        
        self.button_add_user = tk.Button(root, text="Adicionar Utilizador", command=self.add_user)
        self.button_add_user.pack()
        
        self.button_remove_user = tk.Button(root, text="Remover Utilizador", command=self.remove_user)
        self.button_remove_user.pack()
        
        # Caixa de texto para mensagens e botão para enviar
        self.message_display = tk.Text(root, height=10, state="disabled")
        self.message_display.pack()
        
        self.entry_message = tk.Entry(root)
        self.entry_message.pack()
        self.button_send = tk.Button(root, text="Enviar Mensagem", command=self.send_message)
        self.button_send.pack()

        self.button_exit = tk.Button(root, text="Sair", command=root.quit)
        self.button_exit.pack()
        
        # Inicializar o socket
        self.client_socket = None

    def connect_server(self):
        host = self.entry_host.get()
        port = int(self.entry_port.get())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
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
        if message and self.client_socket:
            self.client_socket.send(message.encode())
            self.entry_message.delete(0, "end")

    def add_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        messagebox.showinfo("Cliente", f"Utilizador {username} adicionado")

    def remove_user(self):
        username = self.entry_username.get()
        messagebox.showinfo("Cliente", f"Utilizador {username} removido")

# Inicializar a aplicação do cliente
root = tk.Tk()
app = ClientApp(root)
root.mainloop()
