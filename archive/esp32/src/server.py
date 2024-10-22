# This code runs on the server

import socket

# Recommend 0.0.0.0 to broadcast across network
HOST: str = "0.0.0.0"
PORT: int = 65432


def setupTCPServer(host: str, port: int) -> list[socket.socket, socket.socket]:
    """
    Sets up a TCP server with the specified host and port.
    Returns a tuple containing the server socket, client connection socket, and client IP.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    client_socket, addr = server_socket.accept()

    return [server_socket, client_socket, addr]


def sendCode(conn: socket.socket) -> None:
    """
    Sends user input Python code to the server.
    """
    while True:
        code = input("\nCode >> ")
        conn.sendall(bytes(code, "utf-8"))


def main() -> None:

    global HOST, PORT

    print("\nWelcome to ReRo Server :)")

    print("\nQuit the server anytime using CTRL-C")

    try:

        if HOST == "" or PORT is None:
            HOST = input("\nServer Host: ")
            PORT = input("Server Port : ")

        print(f"\nListening on {HOST}:{PORT}...")
        server_socket, client_socket, client_ip = setupTCPServer(HOST, PORT)
        if client_ip:
            print(f"\nConnected to by {client_ip}")

        sendCode(client_socket)

    except KeyboardInterrupt:
        print("\nExiting...")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:

        try:
            client_socket.close()
        except Exception:
            pass

        try:
            server_socket.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
