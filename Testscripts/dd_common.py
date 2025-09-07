# dd_common.py
#
# This file provides common functions
#
import csv
import glob
import hashlib
import os
import subprocess


## Calculate hash for given file
def hash_file(filepath, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

## Generate random datafile
def create_random_datafile(data_file, size):
    with open(data_file, "wb") as outfile:
        subprocess.run(["head", "-c", size, "/dev/urandom"], stdout=outfile, check=True)
    return hash_file(data_file)

## Generate datafile consisting of 'a's
def create_testfile(data_file, size):
    with open(data_file, 'wb') as f: 
        f.write(b'a' * int(size))
    return hash_file(data_file)

## Check for the presence of outputfiles
def output_files_exist(out_file):
    return glob.glob(out_file + "_*") != []

## Remove previous testfiles
def delete_output_files(out_file):
    for file in glob.glob(out_file + "_*"):
        os.remove(file)

## Persist output data to CSV file
def output_2_csv(results, outfile, results_dir):
    with open(outfile, "w") as csv_file:
        writer = csv.DictWriter(csv_file, results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    # Organize testresults in a directory
    os.makedirs(results_dir, exist_ok=True)
    subprocess.run(f"mv {outfile} {results_dir}/{outfile}", shell=True, check=True)

## Build part of output filenames
def get_tool_str(tool, redundancy):
    if tool == 'pydiode':
        tool_str = f"{tool}_{str(redundancy)}"
    elif tool == 'nc':
        tool_str = f"{tool}"
    return tool_str

