# Step 3 — make it a class

We wrap `main()` in a class named `HelloWorld`, then make an instance and call it.

```python
class HelloWorld:
    def main(self):
        print("Hello World! (step 3)")


HelloWorld().main()
```

See this code in the file here: [step_03_class.py](step_03_class.py)

To run it (from the `HelloWorld/` folder):

```bash
/usr/local/autopkg/python stages/step_03_class.py
#  Hello World! (step 3)
```

Or run it for you: `bash stages/step_03_class.sh`

**Why:** AutoPkg processors are **classes**. AutoPkg locates your processor by
its class name and calls `.main()` on an instance of it, so we put `main()` in a
class named `HelloWorld`. The last line — `HelloWorld().main()` — creates an
instance and calls main() ourselves.

That last line is a problem, though. Instead of *running* the file, try
*importing* it:

```bash
PYTHONPATH=stages /usr/local/autopkg/python -c "import step_03_class"
#  Hello World! (step 3)
```

Or run it for you: `bash stages/step_03_classimport.sh`

We never called anything — we only imported the module — yet it still printed.
**Importing a module runs everything at its top level**, and `HelloWorld().main()`
is top-level code. That matters because AutoPkg loads a processor by *importing*
it: our greeting would fire at import time, before AutoPkg is ready to run the
recipe. [Step 4](step_04_main_guard.md) fixes exactly this.

(`PYTHONPATH=stages` tells Python where to find the module to import — running a
file by its path, as above, doesn't need it. And the stage files are named
`step_NN_…` on purpose: a module name can't start with a digit, so `import
03_class` would be a syntax error while `import step_03_class` just works. It's
the same reason a real processor's file is named after its class, like
`HelloWorld.py` — so AutoPkg can import it.)

---

[← Step 2 — a `main()` function](step_02_function.md) · [Workshop index](../README.md) · [Step 4 — the `__main__` guard →](step_04_main_guard.md)
