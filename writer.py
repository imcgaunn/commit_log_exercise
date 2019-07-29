# functions for coordinating writes to distributed log.

import random
import string


def submit_write(write_q):
    # randomly pick a letter between A and A + N_WRITE_PROCESSES
    letter_range = list(string.ascii_uppercase)
    chosen_key = random.choice(letter_range)
    dummy_data = b'somestuff'
    # sequence number is assigned by the broker when it processes a write request.
    print(f'submitted write: {(chosen_key, dummy_data)}')
    return write_q.put((chosen_key, dummy_data))


def process_write(write_req, logfile):
    print('got write req:')
    if write_req:
        # handle any write request here in broker process, which has access to the log file
        return logfile.write(f'{write_req.key}||{write_req.data}||{write_req.seq}')