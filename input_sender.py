import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

async def send_data():
    uri = "ws://localhost:8765"
    reconnect_delay = 0  # 再接続のための待機時間（秒）

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    # ここでデータを取得します。例として、キーボード入力を取得します。
                    data = input("Enter data (type 'exit' to quit): ")
                    if data == "exit":
                        return
                    await websocket.send(data)
                    print(f"Sent data: {data}")
                    response = await websocket.recv()
                    print(f"Received: {response}")
        except ConnectionClosedOK as e:
            print(e)
        except ConnectionClosedError as e:
            print(e)
            print("Connection was closed. Retrying in a few seconds...")
        except OSError:
            print("Could not connect to server. Retrying in a few seconds...")
        await asyncio.sleep(reconnect_delay)

asyncio.get_event_loop().run_until_complete(send_data())
