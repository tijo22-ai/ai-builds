jobs = ["leaky faucet", "clogged drain", "burst pipe"]
prices = [120, 85, 240]
msg = "  Name: Priya Shah | Job: Burst Pipe  "

print(max(prices))

print(sorted(prices))

last = jobs.pop()
print(last)

avg=sum(prices)/len(prices)
avg=round(avg,2)
print(avg)

jobs.append("running toilet")
print(jobs)

msg=msg.strip()
print(msg)

parts = msg.split(" | ", 1)
print (parts)

print(", ".join(jobs))