import pickle
import logging

logging.basicConfig(level=logging.INFO, datefmt="%h %m %s")

class RPC:
    def __init__(self, sock):
        self._sock = sock


class RCPHandler:
    def __init__(self, sock):
        self._sock = sock
        self._registered_func = {}

    def register_func(self, func):
        self._registered_func[func.__name__] = func

    def handle_connection(self, conn):
        try:
            while True:
                msg = conn.recv()
                if msg:
                    func_name, args, kwargs = pickle.loads(msg)
                    # Call the function and send response
                    try:
                        result = self._registered_func[func_name](*args, **kwargs)
                        bytes_sent = conn.send(pickle.dumps(result))
                        logging.info(f"Delivered {bytes_sent} bytes to client")
                    except Exception e:
                        conn.send(pickle.dumps(result))

                else:
                    logging.info("Connection lost")
        except EOFError as e:
            logging.error(f"Houston, we got a problem: {e}")

