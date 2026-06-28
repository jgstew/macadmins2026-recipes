# From `print("Hello World!")` to an AutoPkg Processor

A hands-on workshop. PSU MacAdmins 2026.

We are going to start with the simplest Python program there is:

```python
print("Hello World!")
```

Then we are going to change it, one step at a time, into a real AutoPkg processor
— the kind of thing you'd find in a recipe. The goal isn't to learn Python. It's
to understand **what an AutoPkg processor actually is** and **why each line of the
"boilerplate" is there**.

Each step has its own short page — work through them in order from the list
below. Each page has the code, the command to run, and why we made that change.
The finished result is [`HelloWorld.py`](HelloWorld.py) in this folder.

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

AutoPkg finds your class, creates an instance, and calls `.main()`. The rest of
this workshop builds exactly that, one piece at a time, and explains why each
piece is needed.

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

The one exception is [**Step 5**](stages/step_05_processor_subclass.md) for reasons that will be explained then.

---

## The steps

Work through these in order. Each page has the code, the command to run, and the
reasoning. Run all commands from the `HelloWorld/` folder.

1. [A plain script](stages/step_01_hello.md) — where we start: `print("Hello World!")`.
2. [Put the work in a `main()` function](stages/step_02_function.md) — a named entry point AutoPkg can call.
3. [Make it a class](stages/step_03_class.md) — and see why *importing* it is a problem.
4. [Only run when executed directly](stages/step_04_main_guard.md) — the `if __name__ == "__main__"` guard.
5. [Subclass `Processor`](stages/step_05_processor_subclass.md) — inherit AutoPkg's machinery.
6. [Set the search path in code](stages/step_06_sys_path.md) — drop the `PYTHONPATH` prefix using `sys.path`.
7. [Log with `self.output()`](stages/step_07_self_output.md) — instead of `print()`.
8. [Accept input from the recipe](stages/step_08_inputs.md) — `input_variables`, read from `self.env`.
9. [Produce a result](stages/step_09_outputs.md) — `output_variables`, written back to `self.env`.
10. [The boilerplate, and running it for real](stages/step_10_finished_processor.md) — the finished processor in a recipe.

---

## Recap

You turned `print("Hello World!")` into a processor by answering, one step at a
time, the questions AutoPkg needs answered:

1. **What do you call?** → a `main()` method ([Steps 2–3](stages/step_02_function.md))
2. **When does it run?** → only under the `if __name__ == "__main__"` guard, so
   that importing the file (as AutoPkg does) doesn't fire it ([Step 4](stages/step_04_main_guard.md))
3. **On what?** → a class that subclasses `Processor` ([Step 5](stages/step_05_processor_subclass.md))
4. **Where does Python find `autopkglib`?** → on `sys.path`; we add
   `/Library/AutoPkg` to it so the later steps run without `PYTHONPATH` ([Step 6](stages/step_06_sys_path.md))
5. **How do you talk to the run?** → `self.output()`, reading verbosity from
   `self.env` ([Step 7](stages/step_07_self_output.md))
6. **What goes in?** → `input_variables`, read from `self.env` ([Step 8](stages/step_08_inputs.md))
7. **What comes out?** → `output_variables`, written to `self.env` ([Step 9](stages/step_09_outputs.md))
8. **How is it packaged and launched?** → the boilerplate + `execute_shell()`
   ([Step 10](stages/step_10_finished_processor.md))

It all comes down to that one shared `self.env` dictionary moving down the list
of processors in a recipe.

## Where to go next

Every processor in the wild is just more of this. For real, working examples —
downloaders, version extractors, file hashers — see
[jgstew-recipes/SharedProcessors](https://github.com/jgstew/jgstew-recipes/tree/main/SharedProcessors).
