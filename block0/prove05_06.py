msg = "Name: Priya Shah | Job: Burst Pipe | Urgent: yes"
prices = {"leaky faucet": 120, "clogged drain": 85, "burst pipe": 240}

parts = msg.split(" | ")

enquiry = {}

label, value = parts[0].split(":", 1)
label = label.strip().lower()
value = value.strip()
enquiry[label] = value

label, value = parts[1].split(":", 1)
label = label.strip().lower()
value = value.strip()
enquiry[label] = value

label, value = parts[2].split(":", 1)
label = label.strip().lower()
value = value.strip()
enquiry[label] = value

print (enquiry)

job = enquiry["job"]
job = job.lower()

urgent = enquiry["urgent"]
urgent = urgent.lower()

if job not in prices:
    print(f"Sorry {enquiry['name']}, we need to look at that job first.")
elif urgent == "yes":
    total = prices[job] + 75
    print(f"Quote for {enquiry['name']}: ${total:.2f} (urgent)")
else:
    print(f"Quote for {enquiry['name']}: ${prices[job]:.2f}")