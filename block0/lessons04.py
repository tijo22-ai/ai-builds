jobs = ["leaky faucet", "clogged drain"]
prices = [120, 85]
pair = "Phone: 780-555-0142".split(":", 1)

jobs.append("burst pipe")
prices.append(240)

print (f"{len(jobs)} jobs | cheapest ${min(prices)} | total ${sum(prices)}")

label, value = pair
print (label.strip().lower(), value.strip())