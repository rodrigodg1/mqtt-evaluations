
from datetime import datetime
import time

now = time.time()

#label  = f"Start Time Evaluation: {now}"

f = open("evaluation/start_time_evaluation.txt", "a")
f.write(str(now))
f.write("\n")
f.close()

