# Step 2 — put the work in a `main()` function

We move the work into a function named `main()`, and call it ourselves at the bottom.

```python
def main():
    print("Hello World! (step 2)")


main()
```

See this code in the file here: [step_02_function.py](step_02_function.py)

To run it:

```bash
/usr/local/autopkg/python stages/step_02_function.py
#  Hello World! (step 2)
```

Or run it for you: `bash stages/step_02_function.sh`

**Why:** AutoPkg needs a named entry point it can call when it's ready — not code
that runs the moment the file is read. (AutoPkg **imports** your file, and
anything at the top level runs during that import, before AutoPkg is ready.) We
name it `main()` because that is the exact method AutoPkg will call. For now we
still call `main()` ourselves on the last line.

---

[← Step 1 — a plain script](step_01_hello.md) · [Workshop index](../README.md) · [Step 3 — make it a class →](step_03_class.md)
