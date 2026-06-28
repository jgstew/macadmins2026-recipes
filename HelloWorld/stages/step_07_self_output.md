# Step 7 — log with `self.output()` instead of `print()`

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

The important detail: `self.output()` decides whether to print by checking the
verbosity level **stored in `self.env`**. So it needs `self.env` to exist —
which is why we now create the instance with a dictionary: `HelloWorld({"verbose":
1})`. That dictionary is the environment AutoPkg normally provides; right now
we're standing in for AutoPkg. Set `verbose` to `0` and the line disappears,
exactly like a non-verbose `autopkg run`.

---

[← Step 6 — set the search path](step_06_sys_path.md) · [Workshop index](../WORKSHOP.md) · [Step 8 — accept input →](step_08_inputs.md)
