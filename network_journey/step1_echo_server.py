import socket


HOST = "127.0.0.1"
PORT = 9001


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[server] listening on {HOST}:{PORT}")

        conn, addr = server.accept()
        with conn:
            print(f"[server] accepted connection from {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("[server] client closed the connection")
                    break

                text = data.decode("utf-8")
                print(f"[server] recv raw bytes: {data!r}")
                print(f"[server] recv text: {text}")

                reply = f"server got: {text}".encode("utf-8")
                conn.sendall(reply)
                print(f"[server] sent reply: {reply!r}")


if __name__ == "__main__":
    main()
