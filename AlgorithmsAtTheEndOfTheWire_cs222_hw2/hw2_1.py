#!/usr/bin/python
#Shawn Pan
#CS222 HW2

import subprocess
import resource
import os

#files to test
path = "./testfiles"
files = os.listdir(path)

#commands
commands = ["gzip {}", "ls -l *.gz", "gunzip *.gz",
            "bzip2 {}", "ls -l *.bz2", "bunzip2 *.bz2",
            "xz {}", "ls -l *.xz", "xz -d *.xz",
            "7z a temp.7z {} -m0=ppmd", "ls -l temp.7z", "7z e temp.7z -y; rm temp.7z"]

for testfile in files:
  results = [testfile]
  for command in commands:
    info = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = info.ru_utime + info.ru_stime #add user and system time
    output = subprocess.check_output(command.format(testfile), cwd=path, shell=True).split()
    info = resource.getrusage(resource.RUSAGE_CHILDREN)
    end = info.ru_utime + info.ru_stime
    elapsed = end - start

    if command[:2] == "ls": #ls command, get size
      results.append(output[4])
    else: #time command
      results.append(str(elapsed))

  print ", ".join(results)