name = "  priya SHAH "
phone = "780-555-0142"
rate = 92.5
hours = "1.5"

clean = name.strip().title()
digits = phone.replace("-", "")
area = phone[0:3]

total = rate * float(hours) * 1.05

print (digits.isdigit())
print(f"{clean} ({area}) | {hours} h | ${total:.2f}")