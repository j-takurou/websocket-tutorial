#!/usr/bin/env python

import asyncio
import itertools
import json

import websockets

from connect4 import PLAYER1, PLAYER2, Connect4

# 接続されている全てのWebSocketを管理するセット
connected_clients = set()

async def handler(websocket):
    # Initialize a Connect Four game.
    game = Connect4()

    # Players take alternate turns, using the same browser.
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)
    
    connected_clients.add(websocket)
    try:
        async for message in websocket: # 技術的ポイント①
            print("connect-four game executed")
            # Parse a "play" event from the UI.
            event = json.loads(message)
            assert event["type"] == "play"
            column = event["column"]

            try:
                # Play the move.
                row = game.play(player, column)
            except RuntimeError as exc:
                # Send an "error" event if the move was illegal.
                event = {
                    "type": "error",
                    "message": str(exc),
                }
                await websocket.send(json.dumps(event))
                continue

            # Send a "play" event to update the UI.
            event = {
                "type": "play",
                "player": player,
                "column": column,
                "row": row,
            }
            await websocket.send(json.dumps(event))

            # If move is winning, send a "win" event.
            if game.winner is not None:
                event = {
                    "type": "win",
                    "player": game.winner,
                }
                await websocket.send(json.dumps(event))

            # Alternate turns.
            player = next(turns)
    finally:
        # 接続が終了したらセットから削除
        connected_clients.remove(websocket)

async def send_time_every_second():
    while True:
        await asyncio.sleep(1)  # 1秒待機
        print("other_task")
        elapsed_time = int(asyncio.get_event_loop().time())
        data = json.dumps({"type": "time", "value": elapsed_time})
        # 全ての接続されているクライアントにメッセージを送信
        await asyncio.gather(
            *[client.send(data) for client in connected_clients]
        )

async def main():
    asyncio.create_task(send_time_every_second())
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever# 技術的ポイント②永続化をするための処理


if __name__ == "__main__":
    asyncio.run(main())