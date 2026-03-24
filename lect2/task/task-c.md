# Checking if an Item Exists in a Data Structure

## The Function

```python
def item_exists(data_structure, item):
    """
    Check if an item exists in a given data structure.

    Args:
        data_structure: A list, tuple, set, dict, or string.
        item: The item to search for.

    Returns:
        True if the item exists, False otherwise.
    """
    return item in data_structure
```

---

## How It Works

The `in` operator is Python's built-in way to check membership — no external packages needed. It works across all common data structures:

| Data Structure | What `in` checks |
|---|---|
| `list` | Is the item in the list? |
| `tuple` | Is the item in the tuple? |
| `set` | Is the item in the set? |
| `dict` | Is the item a **key** in the dict? |
| `str` | Is the item a substring of the string? |

---

## Examples

```python
# --- List ---
print(item_exists([1, 2, 3, 4], 3))        # True
print(item_exists([1, 2, 3, 4], 9))        # False

# --- Tuple ---
print(item_exists(("a", "b", "c"), "b"))   # True
print(item_exists(("a", "b", "c"), "z"))   # False

# --- Set ---
print(item_exists({10, 20, 30}, 20))       # True
print(item_exists({10, 20, 30}, 99))       # False

# --- Dictionary (checks keys) ---
person = {"name": "Alice", "age": 25}
print(item_exists(person, "name"))         # True
print(item_exists(person, "Alice"))        # False  ← "Alice" is a value, not a key

# --- String ---
print(item_exists("hello world", "world")) # True
print(item_exists("hello world", "xyz"))   # False
```

---

## Important Note on Dictionaries 📌

When you use `in` on a **dictionary**, Python checks the **keys only**, not the values. If you want to search values, use `.values()`:

```python
person = {"name": "Alice", "age": 25}

# Check keys
print("name" in person)           # True

# Check values
print("Alice" in person.values()) # True
```

---

## Key Takeaway

> Python's `in` operator is the cleanest and most "Pythonic" way to check membership. It's readable, concise, and works natively across all built-in data structures — no imports required.