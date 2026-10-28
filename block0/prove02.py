job = "leaky faucet"
rate = 92.5
hours = input("How many hours worked?")
total = rate * float(hours) * 1.05
total = round(total,2)
print (job, hours, total, sep = " | ")