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


async def server():
    print("creating socket")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while True:
            print("binding socket")
            try:
                sock.bind((udp_bind_ip, udp_bin_port))
                data = await loop.sock_recv(sock, SIXTY_FOUR_KB)
                # data, _ = sock.recvfrom(SIXTY_FOUR_KB)
                print(data)
            except Exception as e:
                print(f"got exception: {str(e)}")
                sock.close()
                sys.exit(1)


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

loop = asyncio.get_event_loop()
loop.run_until_complete(server())
loop.close()
