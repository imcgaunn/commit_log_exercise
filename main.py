# interactions programming assignment
# distributed commit log with n readers and n writers

from collections import namedtuple
from multiprocessing import Manager, Queue
import random
import string

COMMIT_LOG_FILENAME = 'commits.log'
MAX_WRITE_Q_ENTRIES = 16
MAX_READ_Q_ENTRIES = 16
N_WRITE_PROCESSES = 4
N_READ_PROCESSES = 4

# data is a sequence of bytes. key should be a function of which writer
# wrote the data. sequence is a monotonically increasing sequence number
# that is tracked separately for each key. e.g. subsequence for A writers
# can have independently increasing sequence numbers from the 'B' writers sequence.
LogMessage = namedtuple('LogMessage', ['key', 'data', 'seq'])

def write_message():
    # randomly pick a letter between A and A + N_WRITE_PROCESSES
    letter_range = list(string.ascii_uppercase)
    chosen_key = random.choice(letter_range)
    dummy_data = b'somestuff'
    # sequence number is assigned by the broker when it processes a write request.
    pass


def start_writers(n_writers=N_WRITE_PROCESSES, write_q):
    with multiprocessing.Pool(processes=n_writers) as pool:
        pool.map()


def start_readers(n_readers=N_READ_PROCESSES, read_q):
    with multiprocessing.Pool(n_readers):
        read_req = read_q.get()
        if read_req:
            print(f'{read_req}')


if __name__ == '__main__':
    manager = Manager()
    writes_inbox = manager.Queue(MAX_WRITE_Q_ENTRIES)
    reads_inbox = manager.Queue(MAX_READ_Q_ENTRIES)
    log = open(COMMIT_LOG_FILENAME, 'w')

    while True:
        write_req = writes_inbox.get()
        if write_req:
            # handle any write request in broker process which has access to the log file
            log.write(f'{write_req.key}||{write_req.data}||{write_req.seq}')

    # start writer processes which will submit items to the writes inbox,
    # which will be processed by a broker process that understands how to write
    # to the commit log, which is represented on disk as a file.

    # start reader processes which will block until messages are available, or start non-destructively
    # reading from the commit log by submitting requests to the broker and waiting for results.
    # as readers come online, they will checkpoint to an in-memory database which maintains
    # which producer the reader is associated with, and the last sequence number it successfully
    # processed.
