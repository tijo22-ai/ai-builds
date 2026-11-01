# A
price = 85
if price > 100:
    print("medium")
else:
    print("small")

# B
price = 240
if price > 100:
    print("over 100")
elif price > 200:
    print("over 200")

# C
hours = 3
urgent = True
if hours > 2 and urgent:
    print("call now")
else:
    print("book later")

# D
job = "Burst Pipe"
if job == "burst pipe":
    print("found")
else:
    print("not found")

# E
prices = {"leaky faucet": 120}
price = prices.get("roof leak")
if price is None:
    print("not on list")
else:
    print(price)

# F
msg = ""
if msg:
    print("got a message")
else:
    print("empty")