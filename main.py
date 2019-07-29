# interactions programming assignment
# distributed commit log with n readers and n writers

import collections
import multiprocessing
import functools
import random
import string

import reader
import writer
import message


COMMIT_LOG_FILENAME = 'commits.log'
MAX_WRITE_Q_ENTRIES = 16
MAX_READ_Q_ENTRIES = 16
N_WRITE_PROCESSES = 4
N_READ_PROCESSES = 4


def process_reqs(read_q, write_q):
    logfile = open(COMMIT_LOG_FILENAME, 'w')
    while True:
        while not write_q.empty():
            try:
                req = write_q.get()
                print(f'got write req: {req}')
                writer.process_write(req, logfile)
            except:
                break

        while not read_q.empty():
            try:
                req = read_q.get()
                reader.process_read(req)
            except:
                break


def start_writers(write_q, n_writers=N_WRITE_PROCESSES):
    writer_procs = []
    for i in range(n_writers):
        p = multiprocessing.Process(target=writer.submit_write, args=(write_q,))
        writer_procs.append(p)
        p.start()
    return writer_procs


def start_readers(read_q, n_readers=N_READ_PROCESSES):
    reader_procs = []
    # for i in range(n_readers):
        # p = multiprocessing.Process(target=reader.read_batch)
        # reader_procs.append(p)
        # p.start()
    return reader_procs


def start_broker(read_q, write_q):
    p = multiprocessing.Process(target=process_reqs, args=(read_q, write_q))
    p.start()
    return p


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    writes_inbox = manager.Queue(MAX_WRITE_Q_ENTRIES)
    reads_inbox = manager.Queue(MAX_READ_Q_ENTRIES)
    
    # start writer processes which will submit items to the writes inbox,
    # which will be processed by a broker process that understands how to write
    # to the commit log, which is represented on disk as a file.
    broker_proc = start_broker(reads_inbox, writes_inbox)
    writer_procs = start_writers(writes_inbox)
    reader_procs = []  # eventually this will actually be a function returning reader handles

    # start reader processes which will block until messages are available, or start non-destructively
    # reading from the commit log by submitting requests to the broker and waiting for results.
    # as readers come online, they will checkpoint to an in-memory database which maintains
    # which producer the reader is associated with, and the last sequence number it successfully
    # processed.

    for p in writer_procs:
        p.join()
    for p in reader_procs:
        p.join()
    broker_proc.join()
 