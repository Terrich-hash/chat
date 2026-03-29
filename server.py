import asyncio

clients = {}  # {writer: username}

# Broadcast message to all clients except sender
async def broadcast(message, sender_writer=None):
    for client in list(clients):
        if client != sender_writer:
            try:
                client.write(message)
                await client.drain()
            except Exception as e:
                print(f"Broadcast error: {e}")
                await remove_client(client)

# Handle each client
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    try:
        # Ask for username
        writer.write("Enter your username: ".encode())
        await writer.drain()

        data = await reader.readline()
        username = data.decode().strip()

        if not username:
            writer.close()
            await writer.wait_closed()
            return

        # Check duplicate username
        if username in clients.values():
            writer.write("Username already taken! Disconnecting...\n".encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        clients[writer] = username
        print(f"Username {username} added for {addr}")

        # Notify others
        await broadcast(f"{username} has joined the chat!\n".encode(), writer)

        # Listen for messages
        while True:
            data = await reader.readline()
            if not data:
                break

            message = data.decode().strip()
            if message:
                print(f"{username}: {message}")
                await broadcast(f"{username}: {message}\n".encode(), writer)

    except Exception as e:
        print(f"Error with {addr}: {e}")

    finally:
        await remove_client(writer)
        print(f"{addr} disconnected")

# Remove client safely
async def remove_client(writer):
    if writer in clients:
        username = clients[writer]
        del clients[writer]

        await broadcast(f"{username} has left the chat.\n".encode(), writer)

        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

# Start server
async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 12345)
    addr = server.sockets[0].getsockname()
    print(f"Server started on {addr}")

    async with server:
        await server.serve_forever()

# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down.")