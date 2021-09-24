import socket
import redis
import os
import time
from etagent.config import ConfigKeys
import signal
import sys
from gnenv import create_env
import asyncio

ENVIRONMENT = os.environ.get("ET_ENVIRONMENT", "local")
SIXTY_FOUR_KB = 2 ** 16

env = create_env(ENVIRONMENT)
udp_bind_ip = env.config.get(ConfigKeys.BIND_IP, "127.0.0.1")
udp_bin_port = env.config.get(ConfigKeys.BIND_PORT, 6789)

r_server = redis.Redis(
    host=env.config.get(ConfigKeys.REDIS_HOST, "127.0.0.1"),
    port=env.config.get(ConfigKeys.REDIS_PORT, 6379),
    db=env.config.get(ConfigKeys.REDIS_DB, 0)
)


async def server(queue):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((udp_bind_ip, udp_bin_port))

        while True:
            try:
                data = await loop.sock_recv(sock, SIXTY_FOUR_KB)
                data = str(data, "utf-8")
                print(f"ready from socket: {data}")
                await queue.put(data)
            except Exception as e:
                print(f"got exception: {str(e)}")
                print(sys.exc_info())
                sock.close()
                sys.exit(1)


async def consumer(queue):
    while True:
        data = await queue.get()
        print(f"send to redis: {data}")
        queue.task_done()


async def main():
    queue = asyncio.Queue()

    # fire up the both producers and consumers
    producers = [asyncio.create_task(server(queue))]
    consumers = [asyncio.create_task(consumer(queue))]

    await asyncio.gather(*producers)
    await queue.join()

    for c in consumers:
        c.cancel()


loop = asyncio.get_event_loop()
asyncio.run(main())

"""
async def main():
    asyncio.ensure_future(server())
    await asyncio.sleep(0)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setblocking(False)
        sock.connect((local_ip, 4567))
        await loop.sock_sendall(sock, b'somedata')
        await asyncio.sleep(1)
"""

#
#loop.run_until_complete(server())
#loop.close()
