# From `print("Hello World!")` to an AutoPkg Processor

A hands-on workshop. PSU MacAdmins 2026.

We start with the most boring Python program there is:

```python
print("Hello World!")
```

…and grow it, one small change at a time, into a real AutoPkg processor — the
kind of thing you'd find in a recipe. The goal isn't to learn Python. It's to
understand **what an AutoPkg processor actually is** and **why every line of the
"boilerplate" is there**, so none of it feels like magic.

Each step is a runnable file in [`stages/`](stages). Run each one, watch what it
does, then read *why* we made the change. The finished result is
[`HelloWorld.py`](HelloWorld.py) in this folder.

---

## What is a processor, really?

AutoPkg runs **recipes**. A recipe is just an ordered list of **processors**:

```
recipe ─▶ [Processor A] ─▶ [Processor B] ─▶ [Processor C] ─▶ done
                    ╲           │            ╱
                     ╲          │           ╱
                      ▼         ▼          ▼
                  self.env  (one shared dictionary)
```

Every processor shares one dictionary, **`self.env`**. A processor reads some
values out of it, does one small job, and writes some values back in for the
next processor. That's the whole model.

And a processor is just a **Python class** that:

1. subclasses `autopkglib.Processor`, and
2. has a `main()` method.

AutoPkg finds your class, creates an instance, and calls `.main()`. Everything
below is us building exactly that, and seeing why each piece is needed.

---

## Setup

These scripts import `autopkglib`, the code that powers AutoPkg. The easiest way
to get it — plus a Python that can run it — is to install AutoPkg itself.

Download and run the installer package (this workshop targets **v2.9.0**):

- **<https://github.com/autopkg/autopkg/releases/tag/v2.9.0>** → download
  `autopkg-2.9.0.pkg` and double-click to install.

That installs, among other things:

- **`/usr/local/autopkg/python`** — the Python AutoPkg ships with. We run *every*
  script below with it, starting at Step 1, so the interpreter never changes.
- **`/Library/AutoPkg/`** — where `autopkglib` and the `autopkg` command live.

Then work from inside this workshop folder:

```bash
cd HelloWorld
```

Almost every command is just `/usr/local/autopkg/python stages/step_0X.py`:

```bash
/usr/local/autopkg/python stages/step_01_hello.py
```

The one exception is **Step 5** for reasons that will be explained then.

---

## Step 1 — a plain script

```python
print("Hello World! (step 1)")
```

```bash
/usr/local/autopkg/python stages/step_01_hello.py
#  Hello World! (step 1)
```

It runs. But it is **not** an AutoPkg processor — AutoPkg can't hand it any
values and can't get anything back out of it. AutoPkg doesn't run scripts; it
runs processors. So let's work to become one.

## Step 2 — put the work in a `main()` function

```python
def main():
    print("Hello World! (step 2)")


main()
```

```bash
/usr/local/autopkg/python stages/step_02_function.py
#  Hello World! (step 2)
```

**Why:** AutoPkg needs a named entry point it can call *when it decides to* —
not code that runs the instant the file is read. (AutoPkg **imports** your file;
anything sitting at the top level would fire during that import, before AutoPkg
is ready.) We name it `main()` because that's the exact method AutoPkg will look
for. For now we still call `main()` ourselves on the last line.

## Step 3 — make it a class

```python
class HelloWorld:
    def main(self):
        print("Hello World! (step 3)")


HelloWorld().main()
```

```bash
/usr/local/autopkg/python stages/step_03_class.py
#  Hello World! (step 3)
```

**Why:** AutoPkg processors are **classes**. AutoPkg locates your processor by
its class name and calls `.main()` on an instance of it. Wrapping `main()` in a
class named `HelloWorld` is the shape AutoPkg expects. The last line —
`HelloWorld().main()` — creates an instance and calls main() ourselves.

But watch what that last line costs us. Instead of *running* the file, *import*
it:

```bash
PYTHONPATH=stages /usr/local/autopkg/python -c "import step_03_class"
#  Hello World! (step 3)
```

We never called anything — we only imported the module — yet it still printed.
**Importing a module runs everything at its top level**, and `HelloWorld().main()`
is top-level code. That matters because AutoPkg loads a processor by *importing*
it: our greeting would fire at import time, before AutoPkg is ready to run the
recipe. Step 4 fixes exactly this.

(`PYTHONPATH=stages` tells Python where to find the module to import — running a
file by its path, as above, doesn't need it. And the stage files are named
`step_NN_…` on purpose: a module name can't start with a digit, so `import
03_class` would be a syntax error while `import step_03_class` just works. It's
the same reason a real processor's file is named after its class, like
`HelloWorld.py` — so AutoPkg can import it.)

## Step 4 — only run when the file is executed directly

```python
class HelloWorld:
    def main(self):
        print("Hello World! (step 4)")


if __name__ == "__main__":
    HelloWorld().main()
```

```bash
/usr/local/autopkg/python stages/step_04_main_guard.py
#  Hello World! (step 4)
```

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

Prove it with the same import from Step 3 — this time it stays silent:

```bash
PYTHONPATH=stages /usr/local/autopkg/python -c "import step_04_main_guard"
#  (no output — the guard skipped main() because __name__ wasn't "__main__")
```

Run it directly, though, and it still prints `Hello World! (step 4)`. That's the
goal: **importable with no side effects, runnable on demand.**

Every step from here keeps this guard.

## Step 5 — subclass `Processor`

```python
from autopkglib import Processor


class HelloWorld(Processor):
    def main(self):
        print("Hello World! (step 5)")


if __name__ == "__main__":
    HelloWorld().main()
```

```bash
PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python stages/step_05_processor_subclass.py
#  Hello World! (step 5)
```

**Why:** This is the change that turns "a class" into "an AutoPkg processor."
Subclassing `Processor` inherits the machinery AutoPkg relies on — the `self.env`
environment, `self.output()`, argument handling, and a standalone entry point.

Notice the run command grew a `PYTHONPATH`: the moment we `import autopkglib`,
Python has to be able to *find* it. The installer put it in `/Library/AutoPkg`,
which isn't on the bundled Python's default search path, so
`PYTHONPATH=/Library/AutoPkg` points Python there. (The `autopkg` command itself
doesn't need this — its own script lives inside `/Library/AutoPkg`.) A processor
is still just Python — it simply depends on `autopkglib`. Typing that prefix on
every command gets old fast, so Step 6 makes it unnecessary.

## Step 6 — stop typing `PYTHONPATH`: set the search path in code

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

```bash
/usr/local/autopkg/python stages/step_06_sys_path.py
#  Hello World! (step 6)
```

**Why:** Step 5 only ran because we prefixed the command with
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
  processor in Step 10 drops it again: when AutoPkg runs your recipe it has
  already put `autopkglib` on the path, so a shipped processor never hard-codes it.

Python internals aren't the goal here, but this one earns its keep immediately —
every remaining step is now just `/usr/local/autopkg/python stages/step_…`.

## Step 7 — log with `self.output()` instead of `print()`

```python
class HelloWorld(Processor):
    def main(self):
        self.output("Hello World! (step 7)")


if __name__ == "__main__":
    HelloWorld({"verbose": 1}).main()
```

```bash
/usr/local/autopkg/python stages/step_07_self_output.py
#  HelloWorld: Hello World! (step 7)
```

**Why:** `print()` always dumps to stdout and ignores AutoPkg. `self.output()`
is AutoPkg's logging: it tags the line with the processor name (`HelloWorld:`)
and only shows it when the run is verbose enough (the `-v` flags).

Here's the key insight: `self.output()` decides whether to print by checking the
verbosity level **stored in `self.env`**. So it needs `self.env` to exist —
which is why we now create the instance with a dictionary: `HelloWorld({"verbose":
1})`. That dictionary is the environment AutoPkg normally provides; right now
we're standing in for AutoPkg. Set `verbose` to `0` and the line disappears,
exactly like a non-verbose `autopkg run`.

## Step 8 — accept input from the recipe

```python
class HelloWorld(Processor):
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World (step 8)",
            "description": "Name to greet (default: World (step 8)).",
        },
    }
    output_variables = {}

    def main(self):
        greeting_name = self.env.get("greeting_name", "World (step 8)")
        self.output(f"Hello {greeting_name}!")


if __name__ == "__main__":
    HelloWorld({"verbose": 1, "greeting_name": "MacAdmins (step 8)"}).main()
```

```bash
/usr/local/autopkg/python stages/step_08_inputs.py
#  HelloWorld: Hello MacAdmins (step 8)!
```

**Why:** A hardcoded greeting isn't worth much. `input_variables` **declares**
what a recipe is allowed to pass in — each input's name, whether it's
`required`, a `default` for when the recipe omits it, and a `description`
(this is what `autopkg processor-info HelloWorld` prints). The actual value
arrives in `self.env`, and we read it with `self.env.get("greeting_name",
"World")`.

We pass `greeting_name` in through the env dict here, just like a recipe's
`Arguments:` will. Change the value and the output changes — without touching
`main()`. That parameterization is the entire point of a processor.

## Step 9 — produce a result for the next step

```python
class HelloWorld(Processor):
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World (step 9)",
            "description": "Name to greet (default: World (step 9)).",
        },
    }
    output_variables = {
        "greeting_result": {
            "description": "The greeting that was produced.",
        },
    }

    def main(self):
        greeting_name = self.env.get("greeting_name", "World (step 9)")
        greeting = f"Hello {greeting_name}!"
        self.output(greeting)
        self.env["greeting_result"] = greeting


if __name__ == "__main__":
    processor = HelloWorld({"verbose": 1, "greeting_name": "MacAdmins (step 9)"})
    processor.main()
    print("greeting_result is now:", processor.env["greeting_result"])
```

```bash
/usr/local/autopkg/python stages/step_09_outputs.py
#  HelloWorld: Hello MacAdmins (step 9)!
#  greeting_result is now: Hello MacAdmins (step 9)!
```

**Why:** A processor usually hands something to the next processor in the recipe.
We store our greeting back into `self.env["greeting_result"]`, and **declare**
that output in `output_variables`. Anything in `self.env` is visible to every
later step (and shown by `autopkg run -vv`). The last two lines peek into the
environment to prove the value is sitting there, ready for the next processor.

## Step 10 — the boilerplate, and running it for real

Steps 1–9 are the whole idea. A shipped processor just adds a bit of
conventional boilerplate around it — and drops the Step 6 `sys.path` line, since
when AutoPkg runs your recipe it already has `autopkglib` on the path (that's why
the `autopkg run` below needs neither `PYTHONPATH` nor a `sys.path` tweak). Here
is the finished [`HelloWorld.py`](HelloWorld.py):

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
| `if __name__ == "__main__": … execute_shell()` | The same guard from Step 4 — it keeps the run-it line from firing when AutoPkg imports the module. Here it calls `execute_shell()` (AutoPkg's standalone entry point) rather than `main()`, so you can run the file directly the way AutoPkg's own machinery does. |

**The class name matches the file name** (`HelloWorld` ↔ `HelloWorld.py`) on
purpose: that's how AutoPkg locates the processor a recipe asks for.

### Run it inside a real recipe

The whole point was to be runnable by AutoPkg. The recipe
[`HelloWorld.recipe.yaml`](HelloWorld.recipe.yaml) does exactly that:

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

`--search-dir .` tells AutoPkg to look in this folder for both the recipe and
the `HelloWorld` processor it references. The recipe's `Arguments:` become keys
in `self.env` before `main()` runs — the same hand-off we faked by hand in
Steps 8–9, now done by AutoPkg for real. 🎉

### (Optional) Run the processor standalone

`execute_shell()` reads an input plist from **stdin**, so feed it empty input
and pass arguments as `key=value`. (The shipped file dropped the Step 6 `sys.path`
line, so we prefix `PYTHONPATH` again here — or paste those two lines back in to
run it bare.)

```bash
echo -n "" | PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python HelloWorld.py greeting_name=MacAdmins verbose=1
```

It prints `HelloWorld: Hello MacAdmins!` and dumps the resulting environment
(including `greeting_result`) back out as a plist — exactly what it would hand to
the next processor.

---

## Recap

You turned `print("Hello World!")` into a processor by answering, one step at a
time, the questions AutoPkg needs answered:

1. **What do you call?** → a `main()` method (Steps 2–3)
2. **When does it run?** → only under the `if __name__ == "__main__"` guard, so
   that importing the file (as AutoPkg does) doesn't fire it (Step 4)
3. **On what?** → a class that subclasses `Processor` (Steps 3, 5)
4. **Where does Python find `autopkglib`?** → on `sys.path`; we add
   `/Library/AutoPkg` to it so the later steps run without `PYTHONPATH` (Step 6)
5. **How do you talk to the run?** → `self.output()`, reading verbosity from
   `self.env` (Step 7)
6. **What goes in?** → `input_variables`, read from `self.env` (Step 8)
7. **What comes out?** → `output_variables`, written to `self.env` (Step 9)
8. **How is it packaged and launched?** → the boilerplate + `execute_shell()`
   (Step 10)

None of it is magic — it's all in service of that one shared `self.env`
dictionary moving down the list of processors in a recipe.

## Where to go next

Every processor in the wild is just more of this. For real, working examples —
downloaders, version extractors, file hashers — see
[jgstew-recipes/SharedProcessors](https://github.com/jgstew/jgstew-recipes/tree/main/SharedProcessors).
