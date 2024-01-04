import socket
import threading
from tkinter.filedialog import askopenfilename as aof


def receive_messages(client_socket):
    while True:
        try:
            data_size_header = client_socket.recv(4)
            data_size = int.from_bytes(data_size_header, byteorder='big')
            received_data = b""
            while len(received_data) < data_size:
                data = client_socket.recv(4096)
                if not data:
                    break
                received_data += data
            print(f"Received from server: {received_data.decode('utf-8')}")
        except ConnectionResetError:
            print("Connection to server closed.")
            break
        except BaseException:
            print('Your client has been closed.')
            break


def send_messages(client_socket):
    while True:
        message = input()
        if message == 'file':
            file_name = aof()
            file = open(f'{file_name}', 'r')
            content = file.read()
            print(f'READ:{content}')
            message = content
        data_size = len(message).to_bytes(4, byteorder='big')
        client_socket.sendall(data_size)
        client_socket.sendall(message.encode('utf-8'))
        if message.lower() == 'exit':
            break

    client_socket.close()


def main():
    host = '127.0.0.1'
    port = int(input("Plz type in wanted port."))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()
    receive_thread.join()
    send_thread.join()
    client_socket.close()


if __name__ == "__main__":
    main()
