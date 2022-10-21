from tracemalloc import start


file = open("evaluation/delay.csv", "r")
line_count = 0
for line in file:
    if line != "\n":
        line_count += 1
file.close()


#without header
total_transactions = line_count - 1
#print(line_count-1)


f = open("evaluation/start_time_evaluation.txt", "r")
start_time = f.read()


f = open("evaluation/end_evaluation_time.txt", "r")
end_time = f.readlines()[-1]


start_time = float(start_time)
end_time = float(end_time)


delay = end_time - start_time


print("Total Transactions: ",total_transactions)
print("Total Time (s): ",delay)
print("TPS:", (total_transactions/delay))
