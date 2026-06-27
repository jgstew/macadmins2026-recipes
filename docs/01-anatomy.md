# 1. The anatomy of a processor

An AutoPkg processor is just a Python class that subclasses `Processor` and
implements a `main()` method. Everything else is convention. Here is the whole
of `solutions/HelloWorld.py` with every part labelled.

```python
#!/usr/local/autopkg/python          # (1) shebang
#
# Your Name Here - 2026              # (2) header / attribution
#
"""See docstring for HelloWorld class"""   # (3) module docstring

from autopkglib import (             # (4) imports from autopkglib
    Processor,
    ProcessorError,
)

__all__ = ["HelloWorld"]             # (5) public API

class HelloWorld(Processor):         # (6) subclass Processor
    """Greets a named recipient and returns the greeting as a string."""  # (7)

    description = __doc__            # (8) description idiom
    input_variables = {             # (9) declared inputs
        "greeting_name": {
            "required": False,
            "default": "World",
            "description": "Name to include in the greeting (default: World)",
        },
    }
    output_variables = {            # (10) declared outputs
        "greeting_result": {
            "description": "The full greeting string that was produced",
        },
    }
    __doc__ = description            # (8, cont.)

    def main(self):                  # (11) the entry point
        """Execution starts here."""
        greeting_name = str(self.env.get("greeting_name", "World"))  # (12) read
        greeting = f"Hello, {greeting_name}!"                        #      work
        self.output(greeting)                                        # (13) log
        self.env["greeting_result"] = greeting                       # (14) write

if __name__ == "__main__":           # (15) run-from-CLI hook
    PROCESSOR = HelloWorld()
    PROCESSOR.execute_shell()
```

### The parts

1. **Shebang** `#!/usr/local/autopkg/python` — the Python that ships with
   AutoPkg on macOS. It documents the intended interpreter; AutoPkg imports the
   module rather than executing the file, so the line is mostly informative.
2. **Header** — your name/year. Many processors also link to related code.
3. **Module docstring** — a short pointer. The class docstring is the one that
   matters.
4. **Imports** — at minimum `Processor` (the base class) and `ProcessorError`
   (raise it to stop a recipe cleanly). Import standard-library modules you need
   here too.
5. **`__all__`** — names exported by `from module import *`. By convention it
   lists the processor class.
6. **`class HelloWorld(Processor)`** — subclassing `Processor` gives you
   `self.env`, `self.output()`, `execute_shell()`, and the input/output plumbing.
7. **Class docstring** — one sentence describing what the processor does. This
   is what `autopkg processor-info HelloWorld` prints.
8. **The `description = __doc__` ... `__doc__ = description` idiom** — AutoPkg
   reads a class attribute called `description`. This pair sets it from the
   docstring and then puts the docstring back. Copy it verbatim; it keeps the
   description and the docstring in sync.
9. **`input_variables`** — declares what the recipe may pass in. Covered in
   [2. Inputs & outputs](02-input-and-output.md).
10. **`output_variables`** — declares what the processor writes back out.
11. **`main(self)`** — the method AutoPkg calls. Everything happens here (or in
    helpers it calls). Think of it in three beats: **read → work → write**.
12. **Read** inputs from `self.env` (the shared dictionary of recipe variables).
13. **Log** with `self.output()` so progress shows up under `autopkg run -v`.
14. **Write** results back into `self.env` so later steps can use them.
15. **`if __name__ == "__main__":`** — lets you run the file directly for quick
    experiments. `execute_shell()` is AutoPkg's CLI entry point.

### The mental model

A recipe is a list of processors run in order. They all share one dictionary,
`self.env`. Each processor reads some keys, does a small job, and writes some
keys. That's the whole game.

```
recipe Input ─▶ [Processor A] ─▶ env ─▶ [Processor B] ─▶ env ─▶ [Processor C] ─▶ result
```

Next: [2. Inputs & outputs](02-input-and-output.md).
