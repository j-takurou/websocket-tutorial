#!/usr/bin/env python
import json
import asyncio
import websockets
from connect4 import PLAYER1, PLAYER2, Connect4

async def handler(websocket):
    # 
    game = Connect4()
    while True:
        message = await websocket.recv()
    # for player, column, row in [
    #     (PLAYER1, 3, 0),
    #     (PLAYER2, 3, 1),
    #     (PLAYER1, 4, 0),
    #     (PLAYER2, 4, 1),
    #     (PLAYER1, 2, 0),
    #     (PLAYER2, 1, 0),
    #     (PLAYER1, 5, 0),
    # ]:
    #     event = {
    #         "type": "play",
    #         "player": player,
    #         "column": column,
    #         "row": row,
    #     }
    #     await websocket.send(json.dumps(event))
    #     await asyncio.sleep(0.5)
    # event = {
    #     "type": "win",
    #     "player": PLAYER1,
    # }
    # await websocket.send(json.dumps(event))

async def main():
    async with websockets.serve(handler, "", 8001):# serveしたら、handlerを一度だけ実行する。その関数内に" async for message in websocket:"を実装して無限ループを起こしている

        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())