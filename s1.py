# import socket
# import threading
# import hashlib

# #dictionary to map client names
# clients = {}


# def receive_messages(client_socket, client_name):
#     while True:
#         try:
            
#             message = client_socket.recv(1024).decode()
#             if not message:
#                 break
            
#             #parsing message to get recipient and content
#             recipient, content = message.split('~', 1)
            
#             #checking if recipient is connected
#             if recipient in clients:
#                 #forward msg

#                 recipient_socket = clients[recipient]
#                 recipient_socket.send(f"{client_name}: {content}".encode())
#             else:
#                 client_socket.send("Recipient not found or offline".encode())

#         except Exception as e:
#             print(f"Error receiving message from {client_name}: {e}")
#             break

# # Function to handle client connections
# def handle_client(client_socket, address):
#     try:
#         #assigning unique names
#         client_name = f"client{len(clients)+1}"
#         clients[client_name] = client_socket
#         print(f"Client connected: {client_name}")

#         receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_name))
#         receive_thread.start()

#     except Exception as e:
#         print(f"Error handling client {address}: {e}")


# def main():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('localhost', 5555))
#     server_socket.listen(5)
#     server_socket.settimeout(None)
#     print("Server is listening for incoming connections...")

#     while True:
#         client_socket, address = server_socket.accept()
#         print(f"Connection established with {address}")
#         threading.Thread(target=handle_client, args=(client_socket, address)).start()

# if __name__ == "__main__":
#     main()







import socket
import threading

# Dictionary to map client names to their socket objects
clients = {}


def receive_messages(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Parse the message to extract recipient, content, and hash
            parts = message.split('~')
            if len(parts) != 3:
                print(f"Invalid message format from {client_name}: {message}")
                continue

            recipient, content = parts
            
            if recipient in clients:
                    # Forward the message to the recipient
                    recipient_socket = clients[recipient]
                    recipient_socket.send(f"{client_name}: {content}".encode())
            else:
                    client_socket.send("Recipient not found or offline".encode())
        except Exception as e:
            print(f"Error receiving message from {client_name}: {e}")
            break

def handle_client(client_socket, address):
    try:
        # Assign a unique client name
        client_name = f"client{len(clients)+1}"
        clients[client_name] = client_socket
        print(f"Client connected: {client_name}")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_name))
        receive_thread.start()

    except Exception as e:
        print(f"Error handling client {address}: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(5)
    print("Server is listening for incoming connections...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection established with {address} and client socket {client_socket}")
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
if __name__ == "__main__":
    main()
