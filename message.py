# data is a sequence of bytes. key should be a function of which writer
# wrote the data. sequence is a monotonically increasing sequence number
# that is tracked separately for each key. e.g. subsequence for A writers
# can have independently increasing sequence numbers from the 'B' writers sequence.
LogMessage = namedtuple('LogMessage', ['key', 'data', 'seq'])
