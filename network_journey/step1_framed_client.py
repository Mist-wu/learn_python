import socket
import struct
import time


HOST = "127.0.0.1"
PORT = 9002
HEADER_SIZE = 4


def pack_message(text):
    body = text.encode("utf-8")
    header = struct.pack("!I", len(body))
    return header + body


def recv_exact(sock, size):
    chunks = []
    received = 0

    while received < size:
        chunk = sock.recv(size - received)
        if not chunk:
            raise ConnectionError("socket closed before enough data arrived")
        chunks.append(chunk)
        received += len(chunk)

    return b"".join(chunks)


def recv_message(sock):
    header = recv_exact(sock, HEADER_SIZE)
    body_length = struct.unpack("!I", header)[0]
    body = recv_exact(sock, body_length)
    return body.decode("utf-8")


def send_in_small_chunks(sock, payload, chunk_sizes):
    index = 0

    for size in chunk_sizes:
        if index >= len(payload):
            break

        part = payload[index:index + size]
        sock.sendall(part)
        print(f"[client] sent chunk: {part!r}")
        index += size
        time.sleep(0.2)

    if index < len(payload):
        part = payload[index:]
        sock.sendall(part)
        print(f"[client] sent chunk: {part!r}")


def main():
    messages = [
        "hello",
        "this is a longer message",
        "bye",
    ]

    payload = b"".join(pack_message(message) for message in messages)
    chunk_sizes = [2, 1, 7, 3, 5, 4, 2, 9]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        print(f"[client] connecting to {HOST}:{PORT}")
        client.connect((HOST, PORT))
        print("[client] connected")

        send_in_small_chunks(client, payload, chunk_sizes)

        for _ in messages:
            reply = recv_message(client)
            print(f"[client] recv framed reply: {reply}")


if __name__ == "__main__":
    main()
