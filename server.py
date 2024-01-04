import socket
import threading


def send_data_to_clients(client_sockets, sender_socket, data):
    for client in client_sockets:
        if not client == sender_socket:
            try:
                data_size = len(data).to_bytes(4, byteorder='big')
                client.sendall(data_size)
                client.sendall(data.encode('utf-8'))
            except Exception as e:
                print(f"Error sending data to client: {e}")


def handle_client(client_socket, client_address, client_sockets):
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            data_size_header = client_socket.recv(4)
            data_size = int.from_bytes(data_size_header, byteorder='big')
            received_data = b""
            while len(received_data) < data_size:
                data = client_socket.recv(4096)
                if not data:
                    break
                received_data += data
            data_decode = received_data.decode('utf-8')
            if data_decode.lower() == 'exit':
                # 判断用户是否输入了exit，若是，则跳出当前socket的监听循环并关闭关闭当前socket
                print(f"Connection from {client_address} closed.")
                break
            print(f"Received from {client_address}: {data_decode}")
            send_data_to_clients(client_sockets, client_socket, data_decode)
    except ConnectionResetError:
        print(f'Connection from {client_address} aborted.')
    finally:
        client_sockets.remove(client_socket)
        client_socket.close()


def main():
    host = '127.0.0.1'
    port = int(input("Plz type in wanted port."))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")
    client_sockets = []
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_sockets.append(client_socket)
            client_handler = threading.Thread(target=handle_client,
                                              args=(client_socket, client_address, client_sockets))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
