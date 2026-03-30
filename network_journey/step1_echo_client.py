import socket


HOST = "127.0.0.1"
PORT = 9001


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        print(f"[client] connecting to {HOST}:{PORT}")
        client.connect((HOST, PORT))
        print("[client] connected")

        while True:
            message = input("input message (empty to quit): ").strip()
            if not message:
                print("[client] bye")
                break

            payload = message.encode("utf-8")
            client.sendall(payload)
            print(f"[client] sent: {payload!r}")

            response = client.recv(1024)
            print(f"[client] recv: {response!r}")
            print(f"[client] recv text: {response.decode('utf-8')}")


if __name__ == "__main__":
    main()
