#!/usr/bin/env python
from __future__ import print_function #to make printing stderr work cleanly
import sys
import argparse

__version__ = 0.9

desc = """Dead Simple Queue Autopsy v{}
https://github.com/ycrc/dSQ
A helper script for analyzing the success state of your jobs after a dSQ 
run has completed. Specify the jobfile and the status.tsv file generated 
by the dSQ job and dSQAutopsy will print the jobs that didn't run or 
completed with non-zero exit codes. It will also report count of each to 
stderr.

""".format(__version__)

# argument parsing
parser = argparse.ArgumentParser(description=desc,
                                 usage='%(prog)s jobfile status.tsv', 
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 prog='dSQAutopsy')
parser.add_argument('-v','--version',
                    action='version',
                    version='%(prog)s {}'.format(__version__))
parser.add_argument('jobfile',
                    nargs=1,
                    type=argparse.FileType('r'),
                    help='Job file, one job per line')
parser.add_argument('statusfile',
                    nargs=1,
                    type=argparse.FileType('r'),
                    help='The status.tsv file generated from your dSQ run')

args = parser.parse_args()

try:
    succeeded = set()
    failed = set()
    norun = set()
    for l in args.statusfile[0]:
        tid, exit_code, rest = l.split('\t',2)
        if exit_code == "0":
            succeeded.add(int(tid))
        else:
            failed.add(int(tid))

    for i,l in enumerate(args.jobfile[0]):
        if i not in succeeded:
            if i not in failed:
                norun.add(i)
            print(l, end='')
    print("Autopsy Job Report:\n{} succeeded\n{} failed\n{} didn't run.".format(len(succeeded), len(failed), len(norun)), file=sys.stderr)
except Exception as e:
    print ("Something went wrong. Did you specify the right files?")
    sys.exit(1)
