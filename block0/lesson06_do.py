prices = {"leaky faucet": 120, "clogged drain": 85, "burst pipe": 240}
enquiry = {"name": "Priya Shah", "job": "Burst Pipe", "urgent": "yes"}

job = enquiry.get("job")
job = job.strip().lower()

if job not in prices:
    print(f"Sorry {enquiry['name']}, we need to look at that job first.")
elif enquiry["urgent"] == "yes":
    total = prices[job]+75
    print(f"Quote for {enquiry['name']}: ${total:.2f} (urgent)")
else:
    print(f"Quote for {enquiry['name']}: ${prices[job]:.2f}")
