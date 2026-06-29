# Step 5 — subclass `Processor`

We make `HelloWorld` subclass `Processor` from `autopkglib`.

```python
from autopkglib import Processor


class HelloWorld(Processor):
    def main(self):
        print("Hello World! (step 5)")


if __name__ == "__main__":
    HelloWorld().main()
```

See this code in the file here: [step_05_processor_subclass.py](step_05_processor_subclass.py)

To run it:

```bash
PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python stages/step_05_processor_subclass.py
#  Hello World! (step 5)
```

Or run it for you: `bash stages/step_05_processor_subclass.sh`

**Why:** This is the change that turns "a class" into "an AutoPkg processor."
Subclassing `Processor` inherits the machinery AutoPkg relies on — the `self.env`
environment, `self.output()`, argument handling, and a standalone entry point.

Notice the run command grew a `PYTHONPATH`: the moment we `import autopkglib`,
Python has to be able to *find* it. The installer put it in `/Library/AutoPkg`,
which isn't on the bundled Python's default search path, so
`PYTHONPATH=/Library/AutoPkg` points Python there. (The `autopkg` command itself
doesn't need this — its own script lives inside `/Library/AutoPkg`.) A processor
is still just Python — it simply depends on `autopkglib`. Typing that prefix on
every command gets old fast, so [Step 6](step_06_sys_path.md) makes it unnecessary.

---

[← Step 4 — the `__main__` guard](step_04_main_guard.md) · [Workshop index](../README.md) · [Step 6 — set the search path →](step_06_sys_path.md)
