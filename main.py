# interactions programming assignment
# distributed commit log with n readers and n writers

from collections import namedtuple
from multiprocessing import Manager, Queue

COMMIT_LOG_FILENAME = 'commits.log'
MAX_WRITE_Q_ENTRIES = 16
MAX_READ_Q_ENTRIES = 16

# data is a sequence of bytes. key should be a function of which writer
# wrote the data. sequence is a monotonically increasing sequence number
# that is tracked separately for each key. e.g. subsequence for A writers
# can have independently increasing sequence numbers from the 'B' writers sequence.
LogMessage = namedtuple('LogMessage', ['key', 'data', 'seq'])

if __name__ == '__main__':
    manager = Manager()
    writes_inbox = manager.Queue(MAX_WRITE_Q_ENTRIES)
    reads_inbox = manager.Queue(MAX_READ_Q_ENTRIES)
    
    # start writer processes which will submit items to the writes inbox,
    # which will be processed by a broker process that understands how to write
    # to the commit log, which is represented on disk as a file.
    
    # start reader processes which will block until messages are available, or start non-destructively
    # reading from the commit log by submitting requests to the broker and waiting for results.
    # as readers come online, they will checkpoint to an in-memory database which maintains
    # which producer the reader is associated with, and the last sequence number it successfully
    # processed.
