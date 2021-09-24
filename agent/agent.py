import multiprocessing
import os
import socket
import sys
import time
import requests
from loguru import logger

from gnenv import create_env

from etagent.config import ConfigKeys

ENVIRONMENT = os.environ.get("ET_ENVIRONMENT", "local")
SIXTY_FOUR_KB = 2 ** 16

env = create_env(ENVIRONMENT)
udp_bind_ip = env.config.get(ConfigKeys.BIND_IP, "127.0.0.1")
udp_bin_port = env.config.get(ConfigKeys.BIND_PORT, 6789)
collector_endpoint = env.config.get(ConfigKeys.BIND_IP, "http://127.0.0.1:6790/v1/collect")


# listen on UDP packets from loopback interface, then send them directly to the shared Queue
# to be able to accept new packets as soon as possible
def listener(queue):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((udp_bind_ip, udp_bin_port))

        while True:
            try:
                data = sock.recv(SIXTY_FOUR_KB)
                data = str(data, "utf-8")
                queue.put(data)
            except Exception as e:
                logger.error(f"got exception when reading from socket: {str(e)}")
                logger.error(sys.exc_info())
                sys.exit(1)


# consume the events posted on the shared Queue and post then to the collector using TCP
def consumer(queue):
    while True:
        try:
            data = queue.get()
            response = requests.post(
                collector_endpoint,
                json=data
            )
            if response.status_code != 200:
                logger.error(f"non-ok response code {response.status_code} for {collector_endpoint}, data was:")
                logger.error(data)

            # TODO: do we need to put task_done() in "finally:"? or will this event get re-processed forever if failing?
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
