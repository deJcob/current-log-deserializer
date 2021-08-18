# How to use 

The read_log method opens file and returns array of timestamps, current for channel A and channel B. 

In ``main.py`` there is demo based on ``matplolib``.

# Required packages

- Numpy
- Matplolib (only for demo puropses)

# Current data log file

File is builded with multiple of dataset:

- Timestamp from ros.time.Now().ToNsecs() (uint64_t)
- Size of vector (size_t, 4 bytes)
- Empty 4 bytes
- Vector of pairs of doubles (two channels)

To check the structure of file you may use:
```
hexdump -C test_file -n 5000
```