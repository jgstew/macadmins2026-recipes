# Step 10 — the boilerplate, and running it for real

Steps 1–9 are the whole idea. A shipped processor just adds a bit of
conventional boilerplate around it — and drops the [Step 6](step_06_sys_path.md) `sys.path` line, since
when AutoPkg runs your recipe it already has `autopkglib` on the path (that's why
the `autopkg run` below needs neither `PYTHONPATH` nor a `sys.path` tweak). Here
is the finished [`HelloWorld.py`](../HelloWorld.py) (one level up, in the workshop folder):

```python
#!/usr/local/autopkg/python
#
# Your Name Here - 2026
#
"""See docstring for HelloWorld class"""

from autopkglib import Processor, ProcessorError  # noqa: F401

__all__ = ["HelloWorld"]


class HelloWorld(Processor):
    """Greets a named recipient and stores the greeting as an output variable."""

    description = __doc__
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World",
            "description": "Name to greet (default: World).",
        },
    }
    output_variables = {
        "greeting_result": {
            "description": "The greeting that was produced.",
        },
    }
    __doc__ = description

    def main(self):
        """Execution starts here. AutoPkg calls this once per recipe step."""
        greeting_name = self.env.get("greeting_name", "World")
        greeting = f"Hello {greeting_name}!"
        self.output(greeting)
        self.env["greeting_result"] = greeting


if __name__ == "__main__":
    PROCESSOR = HelloWorld()
    PROCESSOR.execute_shell()
```

Every new piece, and why it's there:

| Piece | Why it exists |
|-------|---------------|
| `#!/usr/local/autopkg/python` | The interpreter AutoPkg uses on macOS. Documents the intended Python. |
| `"""module docstring"""` | Convention; a short pointer to the class. |
| `from autopkglib import Processor, ProcessorError` | `Processor` is the base class; `ProcessorError` is what you `raise` to stop a recipe with a clear message (imported so it's ready to use). |
| `__all__ = ["HelloWorld"]` | Declares the module's public name — the processor class. |
| class docstring + `description = __doc__` … `__doc__ = description` | AutoPkg reads a class attribute called `description` (shown by `autopkg processor-info`). This idiom reuses the docstring as the description, then restores `__doc__`. |
| `if __name__ == "__main__": … execute_shell()` | The same guard from [Step 4](step_04_main_guard.md) — it keeps the run-it line from firing when AutoPkg imports the module. Here it calls `execute_shell()` (AutoPkg's standalone entry point) rather than `main()`, so you can run the file directly the way AutoPkg's own machinery does. |

**The class name matches the file name** (`HelloWorld` ↔ `HelloWorld.py`) on
purpose: that's how AutoPkg locates the processor a recipe asks for.

### Run it inside a real recipe

The whole point was to be runnable by AutoPkg. The recipe
[`HelloWorld.recipe.yaml`](../HelloWorld.recipe.yaml) does exactly that:

```yaml
Process:
  - Processor: HelloWorld
    Arguments:
      greeting_name: "MacAdmins"
```

```bash
autopkg run -v HelloWorld.recipe.yaml --search-dir .
#  Processing HelloWorld.recipe.yaml...
#  HelloWorld
#  HelloWorld: Hello MacAdmins!
```

Or run it for you: `bash stages/step_10_finished_processor.sh`

`--search-dir .` tells AutoPkg to look in this folder for both the recipe and
the `HelloWorld` processor it references. The recipe's `Arguments:` become keys
in `self.env` before `main()` runs — the same hand-off we did by hand in
Steps 8–9, now done by AutoPkg for real.

### (Optional) Run the processor standalone

`execute_shell()` reads an input plist from **stdin**, so feed it empty input
and pass arguments as `key=value`. (The shipped file dropped the Step 6 `sys.path`
line, so we prefix `PYTHONPATH` again here — or paste those two lines back in to
run it bare.)

```bash
echo -n "" | PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python HelloWorld.py greeting_name=MacAdmins verbose=1
```

Or run it for you: `bash stages/step_10_finished_processor_standalone.sh`

It prints `HelloWorld: Hello MacAdmins!` and dumps the resulting environment
(including `greeting_result`) back out as a plist — exactly what it would hand to
the next processor.

That's the whole workshop. Head back to the [recap](../README.md#recap) on the index.

---

[← Step 9 — produce a result](step_09_outputs.md) · [Workshop index](../README.md)
