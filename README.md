# Interactions Take-home Assignment

A simple distributed commit log program written in Python.

## How to Run It

`python main.py`

## What Does It Do?

The driver program located in main.py starts a configurable number of writer and reader processes
which write to and read from a distributed commit log concurrently. The writer processes will write dummy data payloads with keys between 'a' and 'z'. The broker process will serialize these writes and assign increasing sequence numbers to each record, where the sequence numbers are monotonically increasing. Each sub-sequence as identified by key is tracked separately.

## Configuration

The number of reader and writer processes can be controlled by setting
the keys 'n_readers' and 'n_writers' in config.json
to the number of desired reader and writers respectively.

The size of the reader and writer queues (a lower level detail) can also be controlled in config.json by the values of the keys
'max_read_q_entries' and 'max_write_q_entries'.

