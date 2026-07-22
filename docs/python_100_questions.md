# 100 Real-World Python Questions — Easy → Hard

**Rules:** Type every answer yourself. No AI, no Google on the first attempt.
For "predict the output" questions — write your prediction FIRST, then run the code and compare.
Mark each question: ✅ got it | ❌ wrong | 🤷 didn't know. Re-do all ❌ and 🤷 after 7 days.

---

## PART 1 — EASY (Q1–35): Core mechanics that cause real bugs

### References, copies, mutability

**Q1.** Predict the output:
```python
a = [1, 2, 3]
b = a
a.append(4)
print(b)
```

**Q2.** Predict the output:
```python
a = [1, 2, 3]
b = a.copy()
a.append(4)
print(b)
```

**Q3.** Predict the output:
```python
x = 5
y = x
x = x + 1
print(y)
```
Why does this behave differently from Q1?

**Q4.** Predict the output:
```python
config = {"debug": True}
backup = config
config["debug"] = False
print(backup["debug"])
```
How do you fix `backup` so it keeps the original value?

**Q5.** Predict the output:
```python
matrix = [[0] * 3] * 3
matrix[0][0] = 9
print(matrix)
```
(This one surprises almost everyone.)

**Q6.** Which of these can be modified after creation: `list`, `tuple`, `str`, `dict`, `set`? What error do you get if you try `"hello"[0] = "H"`?

**Q7.** Predict the output:
```python
def update(data):
    data["count"] = data["count"] + 1

d = {"count": 0}
update(d)
update(d)
print(d)
```
Why does the function change `d` without returning anything?

### Strings

**Q8.** Write one line that turns `"  Hello World  "` into `"hello world"` (strip spaces, lowercase).

**Q9.** Predict the output:
```python
s = "python"
print(s[-1], s[::-1], s[1:4])
```

**Q10.** Write code that takes `"user@gmail.com"` and extracts just `"gmail.com"` — two different ways (split, and slicing with find).

**Q11.** What is the output and why?
```python
name = "Deepak"
age = 25
print(f"{name} is {age + 5} years old")
```

**Q12.** Fix this bug:
```python
path = "C:\new_folder\test.txt"
print(path)
```
Why does it print something strange?

**Q13.** Write code that counts how many times each character appears in `"engineering"` — result should be a dict.

### Dicts, sets, lists

**Q14.** Predict the output:
```python
d = {"a": 1, "b": 2}
print(d.get("c"))
print(d.get("c", 0))
print(d["c"])
```

**Q15.** You have `users = ["ram", "sam", "ram", "tom", "sam", "ram"]`. Write code to get:
- unique names
- count of each name
- the most common name

**Q16.** What's the difference between `d.get("key")` and `d["key"]`? When would `d["key"]` crash your production script at 2am?

**Q17.** Predict the output:
```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)
print(a is b)
```
Explain the difference between `==` and `is`.

**Q18.** Write one line using a list comprehension: from `nums = [1, 2, 3, 4, 5, 6]`, get squares of only the even numbers.

**Q19.** Convert this loop into a dict comprehension:
```python
result = {}
for word in ["apple", "banana", "kiwi"]:
    result[word] = len(word)
```

**Q20.** Predict the output:
```python
items = [1, 2, 3, 4, 5]
for item in items:
    if item == 3:
        items.remove(item)
print(items)
```
Why is modifying a list while looping over it dangerous?

### Functions

**Q21.** Predict the output:
```python
def greet(name="World", punctuation="!"):
    return f"Hello {name}{punctuation}"

print(greet())
print(greet("Deepak"))
print(greet(punctuation="?"))
```

**Q22.** Predict the output (the classic):
```python
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add("a"))
print(add("b"))
```
Then write the FIXED version using `None` as the default.

**Q23.** What does this function return?
```python
def process(x):
    if x > 0:
        return "positive"
print(process(-5))
```
Why is a function that "sometimes returns" dangerous?

**Q24.** Explain what `*args` and `**kwargs` do. Write a function `def log_call(*args, **kwargs)` that prints them both.

**Q25.** Predict the output:
```python
def outer():
    x = 10
    def inner():
        print(x)
    inner()
outer()
```

### Errors and exceptions

**Q26.** Write code that asks for a number with `input()` and keeps asking until the user enters a valid integer. (while loop + try/except)

**Q27.** What exception does each line raise?
```python
int("abc")
[1, 2, 3][10]
{"a": 1}["b"]
1 / 0
None.upper()
open("no_such_file.txt")
```

**Q28.** What's wrong with this, and why is it a bad habit even though it "works"?
```python
try:
    result = risky_operation()
except:
    pass
```

**Q29.** Predict the output:
```python
try:
    print("A")
    x = 1 / 0
    print("B")
except ZeroDivisionError:
    print("C")
finally:
    print("D")
```

**Q30.** Rewrite this so it doesn't crash when the key is missing OR when the value is None:
```python
price = data["product"]["price"] * 1.18
```

### Files and basics of I/O

**Q31.** Write code that reads a file `notes.txt` and prints only lines containing the word "error" (case-insensitive). Use `with open(...)`.

**Q32.** Why is `with open(...)` better than `f = open(...)` then `f.close()`? What happens to the file if an exception occurs in the middle?

**Q33.** Write code that appends the current timestamp to a file `runs.log` every time the script runs. (Hint: `datetime.now()`, mode `"a"`.)

**Q34.** Write code that reads a CSV file `sales.csv` with columns `name,amount` and prints the total amount — using only the `csv` module, no pandas.

**Q35.** What is the difference between `"r"`, `"w"`, `"a"`, and `"x"` file modes? Which one silently DESTROYS your existing data?

---

## PART 2 — MEDIUM (Q36–75): Real project code

### Logging (you asked for this — Q36–44)

**Q36.** Replace these prints with proper logging. Write the full setup:
```python
print("Starting job")
print("WARNING: config missing, using defaults")
print("ERROR: could not connect to DB")
```
Use `logging.basicConfig` with level, and the format: `2026-07-06 10:30:00 - INFO - Starting job`.

**Q37.** What are the 5 standard logging levels, in order? If you set `level=logging.WARNING`, which messages are shown and which are hidden?

**Q38.** Write a complete `logger_setup.py` module that:
- creates a logger named `"app"`
- logs to BOTH the console and a file `app.log`
- console shows INFO and above, file records DEBUG and above
- format includes timestamp, level, filename, line number, message

**Q39.** Write the setup for a **rotating log file**: max size 5 MB, keep the last 3 backup files. (Hint: `logging.handlers.RotatingFileHandler`.) Explain what happens to `app.log` when it reaches 5 MB — what files exist afterwards?

**Q40.** Write the setup for a **time-based rotating log**: create a new log file every midnight, keep 7 days of logs. (Hint: `TimedRotatingFileHandler`.)

**Q41.** What's the difference between:
```python
logging.error("DB connection failed")
logging.exception("DB connection failed")
```
Inside which block does `logging.exception` make sense, and what extra info does it record?

**Q42.** You have `main.py` importing `db.py` and `api.py`. Show how each module should get its own logger using `logging.getLogger(__name__)` — and explain why `__name__` and not a hardcoded string.

**Q43.** This code logs everything twice. Find the bug:
```python
def get_logger():
    logger = logging.getLogger("app")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    return logger

log = get_logger()
log2 = get_logger()
log.info("hello")
```

**Q44.** Why is this bad in production, and how should it be written instead?
```python
logging.info("Processing user " + str(user_id) + " with data " + str(big_dict))
```
(Hint: lazy formatting — `logging.info("Processing user %s", user_id)`.)

### OOP for real code

**Q45.** Write a class `BankAccount` with: balance starting at 0, `deposit(amount)`, `withdraw(amount)` that raises `ValueError` if insufficient funds, and a `__str__` that prints `"Balance: ₹500"`.

**Q46.** Predict the output:
```python
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1

a = Counter()
b = Counter()
print(Counter.count, a.count)
```
What's the difference between a class attribute and an instance attribute?

**Q47.** Predict the output:
```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof"

animals = [Animal(), Dog()]
for a in animals:
    print(a.speak())
```
What is this concept called?

**Q48.** What does `super().__init__()` do? Write a `Vehicle` class with `brand`, and a `Car(Vehicle)` subclass that adds `model`, calling super correctly.

**Q49.** Write a `@dataclass` for a `Product` with `name: str`, `price: float`, `in_stock: bool = True`. Then explain: what does dataclass generate for you that you'd otherwise write by hand? (You said dataclasses were useless — prove yourself wrong here.)

**Q50.** Predict the output:
```python
class Config:
    def __init__(self):
        self.settings = {}

c1 = Config()
c2 = Config()
c1.settings["debug"] = True
print(c2.settings)
```
Now change `settings = {}` to a CLASS attribute and predict again. Which version is the bug?

### Working with JSON and APIs (daily AI-engineer work)

**Q51.** Write code that reads `config.json` from disk into a dict, changes `"model"` to `"claude-sonnet"`, and writes it back — pretty-printed with indent 2.

**Q52.** This API response is a nested dict. Write code that safely extracts the city, returning `"unknown"` if ANY level is missing:
```python
response = {"user": {"profile": {"address": {"city": "Chennai"}}}}
```

**Q53.** Write a function `call_api(url)` using `requests` that:
- has a 10-second timeout
- retries up to 3 times on failure with 2-second sleep between tries
- raises an exception after 3 failures
- logs each retry attempt

**Q54.** What's the difference between `response.text` and `response.json()`? What exception can `.json()` raise and when?

**Q55.** Write code that loops over a list of 100 user IDs, calls an API for each, and collects results — but if one call fails, logs the error and CONTINUES instead of crashing the whole batch. Store failed IDs in a separate list.

**Q56.** What is wrong with hardcoding `api_key = "sk-abc123"` in your script? Write the correct version using `os.environ` / `os.getenv`, with a clear error message if the variable is missing.

### Pathlib, argparse, scripts

**Q57.** Using `pathlib`, write code that finds all `.csv` files in a folder (including subfolders) and prints each filename with its size in KB.

**Q58.** Write a script with `argparse` that accepts: `--input` (required file path), `--output` (optional, default `"result.txt"`), and `--verbose` (a flag). Print the parsed values.

**Q59.** What does `if __name__ == "__main__":` do? What goes wrong if you import a script that doesn't have it?

**Q60.** Write code that creates a folder `outputs/2026-07-06/` (today's date, dynamically) if it doesn't exist, without crashing if it already exists.

### Comprehensions, generators, iteration patterns

**Q61.** Convert to a single comprehension:
```python
result = []
for row in data:
    if row["status"] == "active":
        result.append(row["email"].lower())
```

**Q62.** What's the difference between these two? Which one can process a 50 GB file without running out of memory, and why?
```python
lines = [line for line in open("huge.txt")]
lines = (line for line in open("huge.txt"))
```

**Q63.** Write a generator function `read_in_batches(items, batch_size)` that yields lists of `batch_size` items at a time. (This is exactly how you batch API calls to LLMs.)

**Q64.** Predict the output:
```python
gen = (x * 2 for x in [1, 2, 3])
print(list(gen))
print(list(gen))
```
Why is the second print different?

**Q65.** Use `enumerate` to print line numbers starting from 1 while reading a file. Then use `zip` to combine `names = ["a","b"]` and `scores = [90, 85]` into a dict.

### Sorting, lambdas, real data wrangling

**Q66.** Sort this list of dicts by price, highest first:
```python
products = [{"name": "A", "price": 300}, {"name": "B", "price": 100}, {"name": "C", "price": 200}]
```

**Q67.** What's the difference between `sorted(lst)` and `lst.sort()`? Which returns None? (Connects to Q23.)

**Q68.** You have log lines like `"2026-07-06 ERROR timeout in module db"`. Write code that takes a list of 1000 such lines and counts how many of each level (INFO/WARNING/ERROR) appear.

**Q69.** Write a function that takes a list of email addresses and returns a dict grouping them by domain: `{"gmail.com": [...], "yahoo.com": [...]}`. (Hint: `dict.setdefault` or `defaultdict`.)

**Q70.** Predict the output:
```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])
```
(The classic closure trap. If you get this right cold, you're ahead of many mid-level devs.)

### Debugging and tracebacks

**Q71.** Read this traceback bottom-up and state: which file, which line, what's the actual problem, and what's your first debugging step?
```
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    result = process_order(order)
  File "orders.py", line 45, in process_order
    total = item["price"] * item["qty"]
KeyError: 'qty'
```

**Q72.** Your function returns the wrong total but doesn't crash. List 3 concrete techniques to find the bug WITHOUT asking AI.

**Q73.** What does this print, and what subtle bug does it demonstrate?
```python
def apply_discount(prices, discount=0.1):
    for i in range(len(prices)):
        prices[i] = prices[i] * (1 - discount)
    return prices

original = [100, 200]
discounted = apply_discount(original)
print(original)
```

**Q74.** Insert `print()` statements into this broken code at the RIGHT places to find why it returns 0 — where would you print and what would you print?
```python
def average_positive(nums):
    total = 0
    count = 0
    for n in nums:
        if n > 0:
            total += n
            count = + 1
    return total / count if count else 0
```
(There IS a bug in this code. Find it.)

**Q75.** What's the difference between a syntax error, a runtime error (exception), and a logic error? Give one example of each from your own experience.

---

## PART 3 — HARD (Q76–100): Production-grade patterns

### Decorators and context managers

**Q76.** Write a decorator `@timer` that prints how long any function takes to run. Test it on a function with `time.sleep(1)`.

**Q77.** Write a decorator `@retry(times=3)` that re-runs a function if it raises an exception, up to `times` attempts. (Decorator with arguments — genuinely hard. Struggle before looking anything up.)

**Q78.** What do `@staticmethod` and `@classmethod` do? Write one realistic example of each in a `User` class (hint: classmethod as an alternative constructor `User.from_json(...)`).

**Q79.** Write your own context manager class `Timer` so this works:
```python
with Timer() as t:
    do_slow_thing()
# prints: "Took 2.31 seconds"
```
Implement `__enter__` and `__exit__`. Then rewrite it using `@contextlib.contextmanager`.

**Q80.** What happens to `__exit__` if an exception occurs inside the `with` block? How would you make your Timer log the exception but let it propagate?

### Typing and pydantic (yes — proving type hints matter)

**Q81.** Add complete type hints:
```python
def process_users(users, min_age, active_only=True):
    return [u["name"] for u in users if u["age"] >= min_age]
```
Including the nested structure of `users`.

**Q82.** What's the difference between `Optional[str]`, `str | None`, and just `str`? What bug category do these annotations prevent when combined with a checker like mypy?

**Q83.** Write a pydantic model `LLMRequest` with: `prompt: str` (min length 1), `temperature: float` (between 0 and 2, default 0.7), `max_tokens: int` (positive). Show what happens when you pass `temperature=5`.

**Q84.** You receive untrusted JSON from an API. Show how pydantic's `model_validate_json` (or `parse_raw`) turns "crash somewhere deep in my code later" into "clear error at the boundary immediately." Why is failing EARLY better?

### Concurrency (batch LLM calls — your actual job)

**Q85.** You need to call an LLM API for 50 prompts. Sequentially it takes 100 seconds. Write a version using `concurrent.futures.ThreadPoolExecutor` with `max_workers=10`. Why do threads help here even though Python has the GIL?

**Q86.** What's the difference between CPU-bound and I/O-bound work? For each, which is the right tool: threads, processes, or asyncio?

**Q87.** Rewrite this as async:
```python
def fetch(url):
    return requests.get(url).text

results = [fetch(u) for u in urls]
```
Using `asyncio` + `aiohttp` (or httpx), fetch all URLs concurrently. What do `async def`, `await`, and `asyncio.gather` each do?

**Q88.** In your ThreadPool version from Q85, one API call raises an exception. What happens to the other 49? Write the version where failures are collected but don't stop the batch.

### Real-world mini-systems (write from scratch, no AI)

**Q89.** Write a complete script `watchdog.py`:
- checks if a URL is reachable every 60 seconds
- logs UP/DOWN status with timestamps to a rotating log file (5 MB, 2 backups)
- if the site goes DOWN, writes an alert line to a separate `alerts.log`
- runs forever until Ctrl+C, which it handles gracefully with a "shutting down" log
This combines Q39, Q53, and exception handling. It's a real tool you can actually use.

**Q90.** Write a `RateLimiter` class: `limiter = RateLimiter(max_calls=5, period=60)` — calling `limiter.allow()` returns True if fewer than 5 calls happened in the last 60 seconds, else False. (This is how you protect yourself from LLM API rate limits.)

**Q91.** Write a simple file-based cache decorator `@cache_to_disk` — before running an expensive function, check if the result for those arguments exists in a JSON file; if yes return it, if no compute, save, and return. (This is how you avoid paying for the same LLM call twice.)

**Q92.** Write a `Config` class that loads settings in priority order: environment variables override `config.json` values, which override built-in defaults. `Config().get("model")` returns the winner. Explain your design.

**Q93.** Write a CLI tool that reads a huge log file (may be GBs) and outputs the top 10 most frequent ERROR messages — WITHOUT loading the whole file into memory. (Generators, Counter, and Q62 knowledge combined.)

### Tricky interview-grade snippets

**Q94.** Predict the output, then explain:
```python
a = [1, 2, 3]
b = a
a = a + [4]
print(b)

x = [1, 2, 3]
y = x
x += [4]
print(y)
```
Why do `a = a + [4]` and `x += [4]` behave DIFFERENTLY?

**Q95.** Predict the output:
```python
print(0.1 + 0.2 == 0.3)
```
Why? What's the correct way to compare floats, and why does this matter when comparing model loss values?

**Q96.** Predict the output:
```python
def f(x, lst=None):
    lst = lst or []
    lst.append(x)
    return lst

print(f(1))
print(f(2))
print(f(3, [0]))
print(f(0, [])) 
```
The last line has a subtle trap. What's the difference between `lst = lst or []` and `lst = [] if lst is None else lst`? When does `or` betray you?

**Q97.** Predict the output:
```python
data = {"a": [1, 2], "b": [3, 4]}
copy1 = data.copy()
copy1["a"].append(99)
print(data["a"])
```
What's the difference between shallow copy and deep copy? When did this exact bug bite people in ML pipelines (hint: copying config dicts with nested lists)?

**Q98.** What does this print, and in what order?
```python
def gen():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = gen()
print("created")
print(next(g))
print(next(g))
```
What does this teach you about WHEN generator code actually runs?

**Q99.** Explain what happens here and why it's a memory/correctness trap:
```python
results = {}
for user in users:
    results[user.id] = process(user)
    if len(results) > 10000:
        results = {}
```
The dict is reassigned — but what if another variable elsewhere holds a reference to the old `results`? Connect this to Q1.

**Q100.** Design question (write actual code): You're building a script that processes 10,000 documents through an LLM API. Requirements: batch of 20 at a time (Q63), retry failures 3 times (Q77), rate-limited to 50 calls/minute (Q90), progress logged to rotating file (Q39), results cached to disk so a crash can resume where it left off (Q91), config from env vars (Q92). Sketch the full structure — classes, functions, main loop. This is a REAL production task, and every piece is a question you already solved.

---

## How to use this

1. **Do 5 questions per day**, in order. Don't binge 30 in one day — retention needs sleep between sessions.
2. **Type everything** in a real editor and RUN it. Predictions written down BEFORE running.
3. Keep an **error journal**: every ❌, write one line about what you misunderstood.
4. After 7 days, **redo all your ❌ questions cold.**
5. Q89 and Q100 are your graduation projects. When you can write those without help, you are no longer "knows concepts, can't code."

Estimated timeline at 3–4 hrs/day: Part 1 in ~1 week, Part 2 in ~3 weeks, Part 3 in ~3 weeks. About 7 weeks to transform.
