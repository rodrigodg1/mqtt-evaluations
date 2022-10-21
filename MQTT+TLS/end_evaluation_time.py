
from datetime import datetime
import time


now = time.time()

f = open("evaluation/total_time_evaluation.txt", "a")
f.write(str(now))
f.write("\n")
f.close()

