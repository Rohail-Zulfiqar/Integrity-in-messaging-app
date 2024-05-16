import socket
import threading

# Real server details
REAL_SERVER_HOST = 'localhost'
REAL_SERVER_PORT = 5555

# Dictionary to map client names to their socket objects
clients = {}

def modify_message_content(content):
    # Function to modify the message content based on user input
    print("Select modification option:")
    print("1. Uppercase")
    print("2. Lowercase")
    print("3. Reverse")
    print("4. Modfying by its own")
    choice = input("Enter your choice: ")
    if choice == '1':
        return content.upper()
    elif choice == '2':
        return content.lower()
    elif choice == '3':
        return content[::-1]  # Reverse the content
    elif choice == '4':
        content= input("Enter Modfying message: ")
        return content
    else:
        print("Invalid choice. Using original content.")
        return content
    
def receive_messages(client_socket, sender_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Parse the message to extract recipient, content, and hash
            parts = message.split('~')
            if len(parts) != 3:
                print(f"Invalid message format from {sender_name}: {message}")
                continue

            recipient, content, received_hash = parts

            # If the recipient is 'server', forward the message to the real server
            if recipient.lower() == 'server':
                # Modify the message content 
                modified_content = modify_message_content(content)
                print(modified_content)
                # Forward the modified message to the real server
                real_server_socket.send(f"{sender_name}~{modified_content}~{received_hash}".encode())
            else:
                # Forward the message to the intended recipient client
                if recipient in clients:
                    recipient_socket = clients[recipient]
                    # Modify the message content 
                    modified_content =modify_message_content(content)
                    print(modified_content)
                    # Forward the modified message to the recipient client
                    recipient_socket.send(f"{sender_name}~{modified_content}~{received_hash}".encode())
                else:
                    client_socket.send("Recipient not found or offline".encode())

        except Exception as e:
            print(f"Error receiving message from {sender_name}: {e}")
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
    global real_server_socket
    real_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    real_server_socket.connect((REAL_SERVER_HOST, REAL_SERVER_PORT))
    print("Connected to real server.")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 6666))  # MITM server listens on a different port
    server_socket.listen(5)
    print("MITM Server is listening for incoming connections...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection established with {address}")
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    main()
