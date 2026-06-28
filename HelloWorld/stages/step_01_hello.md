# Step 1 — a plain script

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

---

[Workshop index](../WORKSHOP.md) · [Step 2 — a `main()` function →](step_02_function.md)
