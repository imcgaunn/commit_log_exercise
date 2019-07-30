# interactions programming assignment
# distributed commit log with n readers and n writers

import collections
import multiprocessing
import functools
import logging
import random
import string

import config
import reader
import writer
import message


SEQ_NUMBER_TABLE = {} # stores associations of keys to last seq number written
READER_CHECKPOINT_TABLE = {} # stores associations of reader to key and last seq processed
LOG_ARRAY = []

def process_write_reqs(write_q):
    global LOG_ARRAY
    global SEQ_NUMBER_TABLE
    while True:
        while not write_q.empty():
            try:
                req = write_q.get()
                writer.process_write(req, LOG_ARRAY, SEQ_NUMBER_TABLE)
            except Exception:
                print(f'exception while processing write')


def start_writers(write_q, n_writers=N_WRITE_PROCESSES):
    writer_procs = []
    for i in range(n_writers):
        p = multiprocessing.Process(target=writer.submit_many_writes, args=(write_q,))
        writer_procs.append(p)
        p.start()
    return writer_procs


def start_reader(read_q):
    # when a reader starts up, it should determine which key
    # it is processing (choose a key k randomly from the set of keys in SEQ_NUMBER_TABLE)
    # and then start reading from the log, ignoring records that don't have
    # its key (k), starting at index i, where i is the value of READER_CHECKPOINT_TABLE[k].
    avail_keys = list(SEQ_NUMBER_TABLE.keys())
    k = random.choice(avail_keys)
    last_processed_i = READER_CHECKPOINT_TABLE[k]


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
    config_opts = config.read_config()
    manager = multiprocessing.Manager()
    writes_inbox = manager.Queue(config_opts['max_read_q_entries'])
    reads_inbox = manager.Queue(config_opts['max_write_q_entries'])

    # start writer processes which will submit requests to the writes 'inbox'.
    # these will be processed by a broker process that understands how to write
    # to the commit log, which is represented as an array of tuples [(key, val, seq)].
    broker_proc = start_broker(reads_inbox, writes_inbox)
    writer_procs = start_writers(writes_inbox)

    # start reader processes which will non-destructively read from the commit log by submitting
    # requests to the broker and waiting for results.
    # as readers come online, they will checkpoint to an in-memory database which maintains
    # which producer the reader is associated with, and the last sequence number it successfully
    # processed.
    reader_procs = start_readers(reads_inbox)

    for p in writer_procs:
        p.join()
    for p in reader_procs:
        p.join()
    broker_proc.join()
 
