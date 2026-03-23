## Finding an Item in a Python Data Structure

### Using a `for` Loop with `range(len(...))`

```python
my_list = [10, 20, 30, 40, 50]
target = 30

for index in range(len(my_list)):
    if my_list[index] == target:
        print(f"Found {target} at index {index}")
        break
```

---

### Using a `for item in list` Loop (Most Pythonic)

```python
my_list = [10, 20, 30, 40, 50]
target = 30

for item in my_list:
    if item == target:
        print(f"Found {target}!")
        break
```

---

### Using the `in` Keyword (Simplest Check)

If you only need to know **whether** the item exists (not its position):

```python
my_list = [10, 20, 30, 40, 50]
target = 30

if target in my_list:
    print(f"{target} is in the list")
else:
    print(f"{target} is not in the list")
```

---

### Using the Built-in `.index()` Method

If you need the **position** of the item, Python lists have a built-in method for this:

```python
my_list = [10, 20, 30, 40, 50]
target = 30

if target in my_list:              # always check first to avoid an error
    position = my_list.index(target)
    print(f"Found {target} at index {position}")
```

---

### Summary Table

| Approach | Gives Index? | Handles Missing Item? | Best For |
|---|---|---|---|
| `range(len(...))` loop | ✅ | With `if` check | When you need the index |
| `for item in list` loop | ❌ | With `if` check | When you only need the value |
| `in` keyword | ❌ | ✅ Naturally | Simple existence check |
| `.index()` method | ✅ | Needs `in` guard | Clean, concise index lookup |

> **Tip:** For everyday searches, prefer `in` or `.index()` — they are readable, built-in, and require no external packages.