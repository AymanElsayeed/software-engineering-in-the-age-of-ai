# Check if an Item Exists in a Data Structure (Python)

## Goal
Write a Python function that checks whether a given item exists inside a data structure.

---

## Key Idea

Different data structures in Python behave differently:

- **List / Tuple** → ordered, allow duplicates
- **Set** → unordered, no duplicates, fast lookup
- **Dictionary** → key-value pairs (by default, lookup checks keys)

Python provides a simple and readable way to check existence using the `in` operator.

---

## Function Implementation

```python
def item_exists(data_structure, item):
    return item in data_structure


⸻

How It Works
	•	The in keyword checks if item exists in data_structure
	•	It automatically adapts to the type:
	•	List / Tuple → checks values
	•	Set → checks values (very fast)
	•	Dictionary → checks keys only

⸻

Examples

# List
print(item_exists([1, 2, 3], 2))   # True

# Tuple
print(item_exists((1, 2, 3), 5))   # False

# Set
print(item_exists({1, 2, 3}, 3))   # True

# Dictionary (checks keys)
print(item_exists({"a": 1, "b": 2}, "a"))  # True
print(item_exists({"a": 1, "b": 2}, 1))    # False


⸻

Edge Cases
	•	Empty data structure

print(item_exists([], 1))  # False

	•	Different types

print(item_exists([1, 2, 3], "1"))  # False (string ≠ integer)


⸻

Notes
	•	This solution is simple and Pythonic
	•	No external libraries are needed
	•	Performance:
	•	List / Tuple → O(n)
	•	Set / Dictionary → O(1) average

⸻

Optional Extension (Dictionary Values)

If you want to check values inside a dictionary instead of keys:

def item_exists_in_dict_values(d, item):
    return item in d.values()


⸻

Summary
	•	Use in for clean and readable existence checks
	•	Works for all basic Python data structures
	•	Be aware of dictionary behavior (keys vs values)

