# functions for coordinating reads from a distributed log.

DEFAULT_CHUNK_SIZE = 5

def read_batch(reads_inbox, n_messages=DEFAULT_CHUNK_SIZE):
    """ gets reference to the read request inbox, and a max number of messages to read
    from the log in one read. """
    pass


def process_read(read_req):
    print(read_req)