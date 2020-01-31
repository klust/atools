# Resuming tasks
Resuming tasks from a job array that were not
completed, or that failed requires a level of bookkeeping you may prefer
to avoid. The same holds for listing successfully completed 
tasks for reducing the output using `areduce`.  
`aranges` is designed to help with these issues.

Note that for this to work, your job should do logging using
[`alog`](alog.md).

Tasks are classified in one of three categories based on the 
information in the logs:
* **completed** means that at least one of the logs contains a record
  of successful termination of the task.
* **failed** means that at least one of the logs contains a termination
  record of the task, and all these records have a nonzero exit code.
* **todo** means that for the task none of the logs contains a 
  termination record. The task may be running already, may have
  been interrupted before it could end or fail, or may yet have to start.

`aranges` primary purpose is in fact helping to determine which task
identifiers should be redone when an array job did not complete, or when
some of its tasks failed.  To get an identifier range of tasks that were
not completed, use
```bash
$ arange  --data data.csv  --log bootstrap.pbs.log10493`
```
or, when not using `aenv`
```bash
$ arange  -t 1-250  --log bootstrap.pbs.log10493`
```

If you want to include the tasks that failed, for instance when a bug that
caused this was fixed, simply add the `--redo` flag when invoking `aranges`.

Similarly, to get a list of tasks that have already completed, add the
`--completed` flag when invoking `aranges`. This option is very useful
in combination with the `areduce` command.

In fact, you can create any range of tasks in one or more of the categories
by specifying one or more of the flags `--completed`,  `--failed` and 
`--todo`. The flag `--redo` is equivalent to `--failed --todo` and 
specifying none of these 4 flags is equivalent to specifying `--todo`.

Another use of `aranges` is to extract the range needed for the 
job submission command (`qsub -t`, `sbatch --array`) from a CSV
data file. In this use case, the `--log` flag is not used. E.g.,
```bash
qsub -t $(aranges --data data.csv) my_job_script.pbs
```
or
```bash
sbatch --array $(aranges --data data.csv) my_job_script.slurm
```
will make sure the right number of copies of the job script is 
launched with indices suitable for `aenv`.

Help on the command is printed using the `--help` flag.
