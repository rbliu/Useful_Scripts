
import subprocess
import multiprocessing
import sys

def run_process(arg):
    p = subprocess.Popen(arg.split(' '))
    p.communicate()

total = 3000
cmdlist = ["python test.py "+str(x) for x in range(total)]
p = multiprocessing.Pool(4)
p.map(run_process, cmdlist)
p.close()
#p.join()
