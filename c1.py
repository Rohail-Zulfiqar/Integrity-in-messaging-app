# import socket
# import threading
# import hashlib

# #recieving message
# def receive_messages(client_socket):
#     while True:
#         try:
#             message = client_socket.recv(1024).decode()
#             if not message:
#                 break
#             print(f"{message}")
#         except Exception as e:
#             print(f"Error receiving message from server: {e}")
#             break

# #sending msg
# def send_message(client_socket):
#     while True:
#         recipient = input("Enter recipient's name (or 'exit' to disconnect): ")
#         if recipient.lower() == 'exit':
#             break
#         message = input("Enter message: ")
#         full_message = f"{recipient}~{message}"
#         client_socket.send(full_message.encode())


# #
# def main():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('localhost', 5555))
#     print("Connected to server.")

#     #thread to recieve msg
#     receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
#     receive_thread.start()

#     #thread to send msg
#     send_thread = threading.Thread(target=send_message, args=(client_socket,))
#     send_thread.start()

#     receive_thread.join()
#     send_thread.join()


#     client_socket.close()

# if __name__ == "__main__":
#     main()





# import socket
# import threading
# import hashlib

# def receive_messages(client_socket):
#     while True:
#         try:
#             message = client_socket.recv(1024).decode()
#             if not message:
#                 break
#             print(f"{message}")
#         except Exception as e:
#             print(f"Error receiving message from server: {e}")
#             break

# def send_message(client_socket):
#     while True:
#         recipient = input("Enter recipient's name (or 'exit' to disconnect): ")
#         if recipient.lower() == 'exit':
#             break
#         message = input("Enter message: ")

#         # Hash the message content
#         message_hash = hashlib.sha256(message.encode()).hexdigest()

#         # Send the recipient, message content, and message hash to the server
#         full_message = f"{recipient}~{message}~{message_hash}"
#         client_socket.send(full_message.encode())

# def main():
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('localhost', 6666))
#     print("Connected to server.")

#     receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
#     receive_thread.start()

#     send_thread = threading.Thread(target=send_message, args=(client_socket,))
#     send_thread.start()

#     receive_thread.join()
#     send_thread.join()

#     client_socket.close()

# if __name__ == "__main__":
#     main()


import socket
import threading

def custom_hash(message):
    # Convert the message to bytes
    message_bytes = message.encode()

    # Initialize the hash value
    hash_value = 0

    # Iterate over each byte in the message
    for byte in message_bytes:
        # Update the hash value using a simple bitwise XOR operation
        hash_value ^= byte

        # Perform additional mixing operations (you can customize this part)
        hash_value = (hash_value << 1) | (hash_value >> 7)  # Rotate left by 1 bit

    # Convert the hash value to hexadecimal representation
    hex_hash = hex(hash_value)

    return hex_hash[2:]  # Remove '0x' prefix

def receive_messages(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Parse the received message to extract sender, content, and hash
            parts = message.split('~')
            if len(parts) != 3:
                print(f"Invalid message format received: {message}")
                continue

            sender, content, received_hash = parts
            calculated_hash = custom_hash(content)

            # Compare the received hash with the calculated hash
            if received_hash == calculated_hash:
                print("Integrity verified: Message is not tampered.")
            else:
                print("Integrity compromised: Message may have been tampered.")

            # Print the message content and sender
            print(f"From {sender}: {content}")

        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break



def send_message(client_socket):
    while True:
        recipient = input("Enter recipient's name (or 'exit' to disconnect): ")
        if recipient.lower() == 'exit':
            break
        message = input("Enter message: ")

        # Hash the message content
        message_hash = custom_hash(message)

        # Send the recipient, message content, and message hash to the server
        full_message = f"{recipient}~{message}~{message_hash}"
        client_socket.send(full_message.encode())

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 6666))
    print("Connected to server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, "server"))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()

if __name__ == "__main__":
    main()

