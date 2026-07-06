# Step 4 — only run when the file is executed directly

We stop calling `HelloWorld().main()` directly and put it behind an `if __name__ == "__main__":` guard.

```python
class HelloWorld:
    def main(self):
        print("Hello World! (step 4)")


if __name__ == "__main__":
    HelloWorld().main()
```

See this code in the file here: [step_04_main_guard.py](step_04_main_guard.py)

To run it (from the `HelloWorld/` folder):

```bash
/usr/local/autopkg/python stages/step_04_main_guard.py
#  Hello World! (step 4)
```

Or run it for you: `bash stages/step_04_main_guard.sh`

**Why:** Until now, `HelloWorld().main()` sat at the top level, so it ran the
instant Python read the file — *including when the file is imported*. And
importing is exactly how AutoPkg loads your processor: it imports the module to
get the class, it does **not** run the file as a script. An unguarded `main()`
call would therefore fire at the wrong moment, every time AutoPkg loaded the
processor.

`if __name__ == "__main__":` is the guard. Python sets the built-in variable
`__name__` to the string `"__main__"` **only** when the file is run directly
(`/usr/local/autopkg/python stages/step_04_main_guard.py`). When the file is *imported*, `__name__` is
the module's name instead, so the guarded line is skipped:

- **run it directly** → `__name__ == "__main__"` → `main()` runs (handy for testing)
- **imported by AutoPkg** → the guard is false → nothing runs on its own; AutoPkg
  calls `main()` itself when it's ready

Prove it with the same import from [Step 3](step_03_class.md) — this time it stays silent:

```bash
PYTHONPATH=stages /usr/local/autopkg/python -c "import step_04_main_guard"
#  (no output — the guard skipped main() because __name__ wasn't "__main__")
```

Or run it for you: `bash stages/step_04_main_guardimport.sh`

Run it directly, though, and it still prints `Hello World! (step 4)`. That is
what we want: the file can be imported without doing anything, and still runs
when you call it directly.

Every step from here keeps this guard.

---

[← Step 3 — make it a class](step_03_class.md) · [Workshop index](../README.md) · [Step 5 — subclass `Processor` →](step_05_processor_subclass.md)
