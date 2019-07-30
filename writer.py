# functions for coordinating writes to distributed log.

import random
import string
import logging

logging.basicConfig()
logger = logging.getLogger('writer-module')


def submit_write(write_q):
    letter_range = list(string.ascii_uppercase)
    chosen_key = random.choice(letter_range)
    dummy_data = b'somestuff'
    # sequence number is assigned by the broker when it processes a write request.
    print(f'submitted write: {(chosen_key, dummy_data)}')
    return write_q.put((chosen_key, dummy_data))


def submit_many_writes(write_q):
    for i in range(1000):
        submit_write(write_q)


def process_write(write_req, log_array, seq_number_table):
    if write_req:
        key, data = write_req
        try:
            seq_number_table[key] += 1
        except (KeyError, IndexError):
            seq_number_table[key] = 1
        log_array.append((key, data, seq_number_table[key]))
        print(f'wrote: {(key, data, seq_number_table[key])} to log')
