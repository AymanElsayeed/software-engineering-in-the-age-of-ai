🔍 Finding an Item in a Python Data Structure

You already know how to loop over a list — great! Now let’s build on that to search for an item.

⸻

✅ 1. Simple Membership Check (Best & Most Pythonic)

If you only need to check whether an item exists, use in:

my_list = [1, 2, 3, 4]

if 3 in my_list:
    print("Found!")
else:
    print("Not found")

✔️ Clean
✔️ Fast
✔️ Recommended for most cases

⸻

✅ 2. Find Item Using a Loop

If you want more control (e.g., custom logic):

my_list = [1, 2, 3, 4]
target = 3

found = False

for item in my_list:
    if item == target:
        found = True
        break

if found:
    print("Found!")
else:
    print("Not found")

✔️ Useful when conditions are more complex
✔️ You can stop early with break

⸻

✅ 3. Find Index of an Item

If you need the position (index) of the item:

Option A — Using .index()

my_list = [1, 2, 3, 4]

index = my_list.index(3)
print(index)  # Output: 2

⚠️ Warning: Raises an error if item is not found

Safer version:

if 3 in my_list:
    print(my_list.index(3))
else:
    print("Not found")


⸻

Option B — Using enumerate() (Very Recommended)

my_list = [1, 2, 3, 4]
target = 3

for index, item in enumerate(my_list):
    if item == target:
        print(f"Found at index {index}")
        break

✔️ Clean
✔️ Pythonic
✔️ No risk of error

⸻

✅ 4. Find All Occurrences

If the item appears multiple times:

my_list = [1, 2, 3, 2, 4]
target = 2

indices = []

for index, item in enumerate(my_list):
    if item == target:
        indices.append(index)

print(indices)  # Output: [1, 3]


⸻

🧠 Summary

Goal	Best Method
Check if item exists	if item in list
Find index (single)	.index()
Safe index search	enumerate()
Find all matches	loop + enumerate()


⸻

💡 Mentor Tip
	•	Use in when you just need yes/no
	•	Use enumerate() when you need index + value
	•	Avoid manual indexing (range(len(...))) unless necessary

⸻

If you want, I can also show you how to search in dictionaries, sets, or nested structures 👍