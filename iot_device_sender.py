import asyncio
import websockets

# WebSocketを使ってデータを送信する非同期関数
async def send_data(queue):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await queue.get()
            if data is None:
                continue
            else:
                await websocket.send(data)
                print(f"Sent: {data}")
                response = await websocket.recv()
                print(f"Received: {response}")
                # import pdb; pdb.set_trace()

# センサのイベントをシミュレートする関数（実際のセンサイベントのハンドリングに置き換える）
async def sensor_event_simulator(queue):
    for _ in range(5):  # 5回のイベントをシミュレート
        await asyncio.sleep(1)  # イベント間の待機時間をシミュレート
        await queue.put("your_data_here_sim")

    # await queue.put(None)  # 送信終了を通知

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(sensor_event_simulator(queue), send_data(queue))

asyncio.get_event_loop().run_until_complete(main())
