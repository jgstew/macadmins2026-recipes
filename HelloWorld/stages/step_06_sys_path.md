# Step 6 — stop typing `PYTHONPATH`: set the search path in code

We add `/Library/AutoPkg` to `sys.path` at the top of the script, so the import works without the `PYTHONPATH` prefix Step 5 needed.

```python
import sys

sys.path.insert(0, "/Library/AutoPkg")

from autopkglib import Processor  # noqa: E402


class HelloWorld(Processor):
    def main(self):
        print("Hello World! (step 6)")


if __name__ == "__main__":
    HelloWorld().main()
```

See this code in the file here: [step_06_sys_path.py](step_06_sys_path.py)

To run it:

```bash
/usr/local/autopkg/python stages/step_06_sys_path.py
#  Hello World! (step 6)
```

Or run it for you: `bash stages/step_06_sys_path.sh`

**Why:** [Step 5](step_05_processor_subclass.md) only ran because we prefixed the command with
`PYTHONPATH=/Library/AutoPkg`. `PYTHONPATH` is just one way to fill **`sys.path`**
— the list of folders Python searches, in order, whenever you `import` something.
We can add that folder from inside the script instead:

```python
import sys
sys.path.insert(0, "/Library/AutoPkg")   # look here first when importing
```

With `/Library/AutoPkg` on `sys.path`, `import autopkglib` now succeeds on its
own, so the command drops back to a plain
`/usr/local/autopkg/python stages/step_06_sys_path.py` — and every step after this one
stays that simple.

Two things worth noticing:

- **Order matters.** The `sys.path` line must run *before* `from autopkglib
  import …`, because Python searches `sys.path` at the instant of the import.
  Putting an import below other code is what trips the linter rule `E402`, so it
  carries a `# noqa: E402` — the same exception real AutoPkg processors use when
  they do this.
- This is a convenience for running our **stage files** by hand. The finished
  processor in [Step 10](step_10_finished_processor.md) drops it again: when AutoPkg runs your recipe it has
  already put `autopkglib` on the path, so a shipped processor never hard-codes it.

Python internals aren't the goal here, but this change is worth it: every
remaining step is now just `/usr/local/autopkg/python stages/step_…`.

---

[← Step 5 — subclass `Processor`](step_05_processor_subclass.md) · [Workshop index](../README.md) · [Step 7 — `self.output()` →](step_07_self_output.md)
