# dd_statistics.py
#
# This file provides statistical functionality
#
import pandas as pd


## Print most obvious statistics to stdout
def print_simple_statistics(transfer_results):
    df = pd.DataFrame(transfer_results)

    nr_transfer_success = (df['Xfer_success'] == True).sum().sum()
    nr_attempts = len(df)
    mean_transfer_time = df['Xfer_time'].mean()
    success_rate = (nr_transfer_success / nr_attempts) * 100

    print(f"Success rate: {success_rate:.1f}%")
    print(f"Average duration: {mean_transfer_time:.2f} seconds\n")

