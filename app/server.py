import asyncio

HOST = "0.0.0.0"
PORT = 12345

clients = {}  # {writer: username}


async def broadcast(message: bytes, sender_writer=None):
    disconnected = []

    for client in clients.copy():
        if client != sender_writer:
            try:
                client.write(message)
                await client.drain()
            except Exception:
                disconnected.append(client)

    for client in disconnected:
        await remove_client(client)


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"New connection from {addr}", flush=True)

    try:
        # Ask for username
        writer.write(b"Enter your username: ")
        await writer.drain()

        data = await reader.readline()

        if not data:
            writer.close()
            await writer.wait_closed()
            return

        username = data.decode().strip()

        if not username:
            writer.close()
            await writer.wait_closed()
            return

        if len(username) > 20:
            writer.write(b"Username too long.\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        if username in clients.values():
            writer.write(
                b"Username already taken! Disconnecting...\n"
            )
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        clients[writer] = username

        print(
            f"Username '{username}' added for {addr}",
            flush=True
        )

        await broadcast(
            f"{username} has joined the chat!\n".encode(),
            writer
        )

        while True:
            data = await reader.readline()

            if not data:
                break

            message = data.decode().strip()

            if not message:
                continue

            print(
                f"{username}: {message}",
                flush=True
            )

            await broadcast(
                f"{username}: {message}\n".encode(),
                writer
            )

    except Exception as e:
        print(
            f"Error with {addr}: {e}",
            flush=True
        )

    finally:
        await remove_client(writer)
        print(
            f"{addr} disconnected",
            flush=True
        )


async def remove_client(writer):
    if writer not in clients:
        return

    username = clients.pop(writer)

    await broadcast(
        f"{username} has left the chat.\n".encode(),
        writer
    )

    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


async def main():
    server = await asyncio.start_server(
        handle_client,
        HOST,
        PORT
    )

    addr = server.sockets[0].getsockname()

    print(
        f"Server started on {addr}",
        flush=True
    )

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(
            "\nServer shutting down...",
            flush=True
        )