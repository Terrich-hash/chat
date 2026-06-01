import asyncio

HOST = "127.0.0.1"
PORT = 12345


async def receive_messages(reader):
    try:
        while True:
            data = await reader.readline()

            if not data:
                print("\nDisconnected from server.")
                break

            print(data.decode().strip())

    except Exception as e:
        print(f"\nReceive error: {e}")


async def send_messages(writer):
    try:
        while True:
            message = await asyncio.to_thread(input)

            writer.write((message + "\n").encode())
            await writer.drain()

    except Exception as e:
        print(f"\nSend error: {e}")


async def main():
    reader, writer = await asyncio.open_connection(
        HOST,
        PORT
    )

    prompt = await reader.readuntil(b": ")
    print(prompt.decode(), end="")

    username = await asyncio.to_thread(input)

    writer.write((username + "\n").encode())
    await writer.drain()

    receive_task = asyncio.create_task(
        receive_messages(reader)
    )

    send_task = asyncio.create_task(
        send_messages(writer)
    )

    await asyncio.gather(
        receive_task,
        send_task
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient closed.")