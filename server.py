import socket, threading

server_ip = '127.0.0.1'
server_port = 999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = {}

server.bind((server_ip,server_port))

server.listen()
print("Waiting for connections\n")

def redirect(client_socket):
    while(True):
        print("redirect messaging")
        message = str(client_socket.recv(1024).decode())
        print(message)

        if(message.startswith("DEVELOPER") and "DEVELOPER" in clients.keys()):
            sock = clients.get("DEVELOPER")
            sock.send(1024).encode()

        elif(message.startswith("MANAGER") and "MANAGER" in clients.keys()):
            sock = clients.get("MANAGER")
            sock.send(1024).encode()
        
        elif(message.startswith("TESTER") and "TESTER" in clients.keys("TESTER")):
            sock = clients.get("TESTER")
            sock.send(1024).encode()

        else:
            print("The client you want to contact is offline")
        

while(True):
    client_socket, client_address = server.accept()
    print(client_address," is connected")
    client_name = client_socket.recv(1024).decode()
    print(client_name)
    clients.update({client_name : client_socket})
    print(clients.keys())
    client_socket.send("Connected to server successfully".encode())

    thread = threading.Thread(target=redirect, args=(client_socket,))
    thread.start()