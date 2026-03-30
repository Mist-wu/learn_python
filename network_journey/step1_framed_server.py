import socket
import struct


HOST = "127.0.0.1"
PORT = 9002
HEADER_SIZE = 4


def pack_message(text):
    body = text.encode("utf-8")
    header = struct.pack("!I", len(body))
    return header + body


def unpack_messages(buffer):
    messages = []

    while True:
        if len(buffer) < HEADER_SIZE:
            break

        body_length = struct.unpack("!I", buffer[:HEADER_SIZE])[0]
        frame_length = HEADER_SIZE + body_length

        if len(buffer) < frame_length:
            break

        body = buffer[HEADER_SIZE:frame_length]
        messages.append(body.decode("utf-8"))
        buffer = buffer[frame_length:]

    return messages, buffer


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[server] listening on {HOST}:{PORT}")

        conn, addr = server.accept()
        with conn:
            print(f"[server] accepted connection from {addr}")
            buffer = b""

            while True:
                chunk = conn.recv(8)
                if not chunk:
                    print("[server] client closed the connection")
                    break

                print(f"[server] recv chunk: {chunk!r}")
                buffer += chunk
                print(f"[server] current buffer: {buffer!r}")

                messages, buffer = unpack_messages(buffer)
                for message in messages:
                    print(f"[server] unpacked message: {message}")
                    reply = pack_message(f"ack: {message}")
                    conn.sendall(reply)

                print(f"[server] remaining buffer: {buffer!r}")


if __name__ == "__main__":
    main()
