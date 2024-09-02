""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved
"""

import asyncio
import pickle
import socket  # hostname 확인용

IP_ADDR = socket.gethostbyname(socket.gethostname())
PORT = 7470

writer_list = []


async def forward(data):
    for w in writer_list.copy():
        try:
            w.write(data)
            await w.drain()
        except:
            writer_list.remove(w)
            # w.close()


async def handle(reader, writer):
    global writer_list
    writer_list.append(writer)
    addr = writer.get_extra_info("peername")
    print(f"클라이언트 연결: {addr}")

    while writer in writer_list:
        try:
            data = await reader.read(1024)
            print("받은 데이터: ", pickle.loads(data))
        except:
            break  # 클라이언트 연결 오류

        await forward(data)


async def main():
    server = await asyncio.start_server(handle, IP_ADDR, PORT)
    print(f"Started server at {server.sockets[0].getsockname()}")

    async with server:
        await server.serve_forever()


asyncio.run(main())

"""
그렇다면 클라이언트는?
- GUI도 별도의 event loop를 갖고 있어서 asyncio와 함께 쓰기 어려움
- GUI는 사람의 입력을 가정하기 때문에 동시성으로 최적화할 필요성이 적다.
"""
