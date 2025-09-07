#!/usr/bin/python3
import argparse
import sys
import time


## chunk_size: Size of each chunk in bytes; max_bitrate: Desired bitrate (bits/s).
def throttle_input(chunk_size, max_bitrate):
    expected_transfer_time = (chunk_size * 8) / max_bitrate  # Time to transfer a chunk
    
    while True:
        start_time = time.time()
        chunk = sys.stdin.buffer.read(chunk_size)  # Read a chunk from standard input

        if not chunk: break  # End of file

        sys.stdout.buffer.write(chunk)  # Write the chunk to standard output
        sys.stdout.buffer.flush()

        elapsed = time.time() - start_time
        sleep_time = expected_transfer_time - elapsed

        # Wait until the expected transfer time has passed
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Throttles the rate at which data is transferred from standard input to standard output.")
    parser.add_argument("-c", "--chunk-size", type=int, help="Chunk size in bytes.")
    parser.add_argument("-b", "--max-bitrate", type=int, help="Maximum bitrate bits/s).")
    args = parser.parse_args()
    throttle_input(args.chunk_size, args.max_bitrate)
