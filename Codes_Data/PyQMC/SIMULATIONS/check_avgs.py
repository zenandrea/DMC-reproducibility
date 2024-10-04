import pyqmc.api as pyq
import sys
from rich import print

print(pyq.read_mc_output(sys.argv[1],warmup=100, reblock=20))