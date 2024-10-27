import sqlite3
import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Função para configurar a base de dados de utilizadores
def setup_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor")
        self.root.geometry("400x300")
        
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
        
        # Botões para ligar, desligar, adicionar e remover utilizadores, e sair
        self.button_connect = tk.Button(root, text="Ligar", command=self.start_server)
        self.button_connect.pack()
        
        self.button_disconnect = tk.Button(root, text="Desligar", command=self.stop_server)
        self.button_disconnect.pack()
        
        self.button_add_user = tk.Button(root, text="Adicionar Utilizador", command=self.add_user)
        self.button_add_user.pack()
        
        self.button_remove_user = tk.Button(root, text="Remover Utilizador", command=self.remove_user)
        self.button_remove_user.pack()
        
        self.button_exit = tk.Button(root, text="Sair", command=root.quit)
        self.button_exit.pack()
        
        # Inicializar o socket e lista de clientes
        self.server_socket = None
        self.clients = []
        
        # Configurar a base de dados de utilizadores
        setup_database()

    def start_server(self):
        host = self.entry_host.get()
        port = int(self.entry_port.get())
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        threading.Thread(target=self.accept_clients).start()
        messagebox.showinfo("Servidor", "Servidor iniciado")

    def accept_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    self.broadcast(message, client_socket)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                client.send(message.encode())

    def stop_server(self):
        for client in self.clients:
            client.close()
        if self.server_socket:
            self.server_socket.close()
        messagebox.showinfo("Servidor", "Servidor desligado")

    def add_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Servidor", "Utilizador adicionado")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Servidor", "Utilizador já existe")
        conn.close()

    def remove_user(self):
        username = self.entry_username.get()
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Servidor", "Utilizador removido")

# Inicializar a aplicação do servidor
root = tk.Tk()
app = ServerApp(root)
root.mainloop()
