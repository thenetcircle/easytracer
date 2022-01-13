import argparse
import json
import logging
import multiprocessing
import os
import socket
import sys
import time
from contextlib import contextmanager

import requests


def parse_args():
    parser = argparse.ArgumentParser(description="easytracer agent")
    parser.add_argument(
        '-b', '--bind',
        help='Either ip:port or /path/to/easytracer.sock. Example: :9999 or localhost:1234',
        required=True
    )
    parser.add_argument(
        '-e', '--endpoint',
        help='Collector endpoint URL. Example: http://127.0.0.1:6790/v1/collect',
        required=True
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Enable debug logging',
        dest='verbose',
        action='store_true',
        required=False
    )
    parser.set_defaults(verbose=False)
    return parser.parse_args()


def init_logging(_args):
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=log_level
    )
    return logging.getLogger(__name__)


SIXTY_FOUR_KB = 2 ** 16
args = parse_args()
logger = init_logging(args)

udp_bind_socket = args.bind
collector_endpoint = args.endpoint


@contextmanager
def socket_file_listener():
    sock = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(udp_bind_socket)

    try:
        yield sock
    finally:
        sock.close()


@contextmanager
def socket_port_listener():
    sock = None

    try:
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        local_ip, local_port = udp_bind_socket.split(":")
        sock.bind((local_ip, int(float(local_port))))
    except Exception as e:
        logger.error(f"could not bind to socket: {str(e)}")
        logger.exception(e)

        if sock is not None:
            sock.close()

        sys.exit(1)

    try:
        yield sock
    finally:
        sock.close()


# listen on UDP packets from loopback interface, then send them directly to the shared Queue
# to be able to accept new packets as soon as possible
def listener(queue):
    if ":" in udp_bind_socket:
        logger.info(f"listening on {udp_bind_socket}")
        socket_listener = socket_port_listener
    else:
        logger.info(f"listening to file socket {udp_bind_socket}")
        socket_listener = socket_file_listener

    with socket_listener() as sock:
        while True:
            try:
                data = sock.recv(SIXTY_FOUR_KB)
                data = str(data, "utf-8")
                logger.debug(f"got data: {data}")
                queue.put(data)
            except (KeyboardInterrupt, InterruptedError):
                logger.info('received interrupt, exiting')
                return
            except Exception as e:
                logger.error(f"got exception when reading from socket: {str(e)}")
                logger.error(sys.exc_info())
                time.sleep(0.01)
                sys.exit(1)


# consume the events posted on the shared Queue and post then to the collector using TCP
def consumer(queue):
    while True:
        try:
            data = json.loads(queue.get())
            response = requests.post(
                collector_endpoint,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code != 200:
                logger.error(f"non-ok response code {response.status_code} for {collector_endpoint}: {response.json()}")
                logger.error("data was:")
                logger.error(data)

            # TODO: do we need to put task_done() in "finally:"? or will this event get re-processed forever if failing?
            queue.task_done()
        except (KeyboardInterrupt, InterruptedError):
            logger.info('received interrupt, exiting')
            return
        except requests.exceptions.ConnectionError as e:
            logger.error(f"could not send to collector: {str(e)}")
        except Exception as e:
            logger.error(f"error on queue get: {str(e)}")
            logger.exception(sys.exc_info())


def main():
    try:
        os.remove(udp_bind_socket)
    except OSError:
        pass

    pool = multiprocessing.Pool(processes=2)
    m = multiprocessing.Manager()
    q = m.Queue()

    pool.apply_async(listener, (q,))
    pool.apply_async(consumer, (q,))

    while True:
        try:
            time.sleep(0.5)
        except (KeyboardInterrupt, InterruptedError):
            logger.info('received interrupt, exiting')
            return


if __name__ == "__main__":
    main()
