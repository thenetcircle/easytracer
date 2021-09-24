import multiprocessing
import os
import socket
import sys
import time

import redis
from gnenv import create_env

from etagent.config import ConfigKeys

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


def listener(queue):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((udp_bind_ip, udp_bin_port))

        while True:
            try:
                data = sock.recv(SIXTY_FOUR_KB)
                data = str(data, "utf-8")
                print(f"read from socket: {data}")
                queue.put(data)
            except Exception as e:
                print(f"got exception: {str(e)}")
                print(sys.exc_info())
                sys.exit(1)


def consumer(queue):
    while True:
        try:
            data = queue.get()
            print(f"send to redis: {data}")
            queue.task_done()
        except Exception as e:
            print(f"error on queue get: {str(e)}")
            print(sys.exc_info())


def main():
    pool = multiprocessing.Pool(processes=2)
    m = multiprocessing.Manager()
    q = m.Queue()

    pool.apply_async(listener, (q,))
    pool.apply_async(consumer, (q,))

    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    main()


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
