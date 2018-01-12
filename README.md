# Dead Simple Queue (dSQ)

Dead simple queue is a [slurm](https://slurm.schedmd.com/)-only successor to SimpleQueue. It wraps around slurm's [`sbatch`](https://slurm.schedmd.com/sbatch.html) to help you submit independent jobs as job arrays. In many ways, the array indeces look like normal jobs, but are far easier to manage. It's primary advantage over SimpleQueue is that your job allocation will only ever use the resources needed to complete the remaining jobs. `dSQ` is **not** recommended for situations where the initialiazation of the job takes most of its execution time and it is re-usable. These situations are much better handled by a worker-based job handler.

## Job File:

First, you'll need to generate a job file. Each line of this job file needs to specify exactly what you want run for each job, including any modules that need to be loaded or modifications to your environment variables. Empty lines or lines that begin with `#` will be ignored when submitting your job array. **Note:** slurm jobs begin in the directory from which your job was submitted, so be wary of relative paths. This also means that you don't need to `cd` to the working directory if you submit your job there.

## Usage:

`dSQ.py` takes a few arguments, then passes the rest directly to sbatch, either by writing a script to stdout or by directly submitting the job for you. Without specifying any additional sbatch arguments, some defaults will be set. run `sbatch --help` or see [schedMD's sbatch documentation](https://slurm.schedmd.com/sbatch.html) for more info on sbatch options.


```
dSQ.py --jobfile jobfile [dSQ args] [slurm args]

Required dSQ arguments:
  --jobfile JOBFILE   Job file, one job per line

Optional dSQ arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --submit              Submit the job array on the fly instead of printing to stdout.
  --max-jobs MAX_JOBS
                        Maximum number of simultaneously running jobs from the job array
```

## Output

dSQ creates a file named `job_jobid_status.tsv` which will report the success or failure of each job as it finishes. Note this file will not contain information for any jobs that were canceled (e.g. by the user with scancel) before they began. This file contains details about the completed jobs in the following tab-separated columns:

* Job_ID: the zero-based line number from your job file
* Exit_Code: exit code returned from your job
* Time_Started: time started, formatted as YYYY-MM-DD HH:MM:SS
* Time_Ended: time started, formatted as YYYY-MM-DD HH:MM:SS
* Time_Elapsed: in seconds
* Job: the line from your job file

## Autopsy Report

If you would like to generate a list of jobs that did not run, either due to failure or because they were cancelled before running, use `dSQAutopsy`. Just specify your original job file and the status file generated by `dSQ`:

```
usage: dSQAutopsy jobfile status.tsv

A helper script for analyzing the success state of your jobs after a dSQ 
run has completed. Specify the jobfile and the status.tsv file generated 
by the dSQ job and dSQAutopsy will print the jobs that didn't run or 
completed with non-zero exit codes. It will also report count of each to 
stderr.

positional arguments:
  jobfile       Job file, one job per line
  statusfile     The status.tsv file generated from your dSQ run
```

