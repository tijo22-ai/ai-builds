msg = "Name: Priya Shah | Job: leaky faucet | Phone: 780-555-0142"
prices = {"leaky faucet": 120, "clogged drain": 85, "burst pipe": 240}

parts = msg.split(" | ")
print (parts)

enquiry={}

label, value =parts[0].split(":",1)
label = label.strip().lower()
value=value.strip()
enquiry[label]=value

label, value =parts[1].split(":",1)
label = label.strip().lower()
value=value.strip()
enquiry[label]=value

label, value =parts[2].split(":",1)
label = label.strip().lower()
value=value.strip()
enquiry[label]=value

print (enquiry)

job = enquiry["job"]
job = job.lower()
price = prices.get(job)

print(f"Quote for {enquiry['name']}: ${price:.2f}")

print("email" in enquiry)
