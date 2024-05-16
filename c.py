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





import socket
import threading
import hashlib

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"{message}")
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break

def send_message(client_socket):
    while True:
        recipient = input("Enter recipient's name (or 'exit' to disconnect): ")
        if recipient.lower() == 'exit':
            # break
            client_socket.close()
            break
        else:
            message = input("Enter message: ")

        # Hash the message content
            message_hash = hashlib.sha256(message.encode()).hexdigest()

        # Send the recipient, message content, and message hash to the server
            full_message = f"{recipient}~{message}~{message_hash}"
            client_socket.send(full_message.encode())

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    print("Connected to server.")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(client_socket,))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client_socket.close()

if __name__ == "__main__":
    main()
