import asyncio

# Receive messages from server
async def receive_messages(reader):
    while True:
        try:
            data = await reader.readline()
            if not data:
                print("Disconnected from server.")
                break
            print(data.decode().strip())
        except Exception as e:
            print(f"Receive error: {e}")
            break

# Send messages to server
async def send_messages(writer):
    while True:
        try:
            message = input()
            writer.write((message + "\n").encode())
            await writer.drain()
        except Exception as e:
            print(f"Send error: {e}")
            break

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 12345)

    # Handle username prompt
    data = await reader.readuntil(b": ")
    print(data.decode(), end="")

    username = input()
    writer.write((username + "\n").encode())
    await writer.drain()

    # Start tasks
    asyncio.create_task(receive_messages(reader))
    await send_messages(writer)

# Run client
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client closed.")