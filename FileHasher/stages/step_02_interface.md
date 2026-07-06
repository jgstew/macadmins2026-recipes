# Step 2 — declare the interface

Here is Step 1's task completed: `pathname` is now a declared `input_variable` and
`filehasher_md5` a declared `output_variable`. Compare it against what you wrote.

```python
#!/usr/local/autopkg/python
"""See docstring for FileHasher class"""

import sys

sys.path.insert(0, "/Library/AutoPkg")  # look here first when importing

from autopkglib import Processor

__all__ = ["FileHasher"]


class FileHasher(Processor):
    """Computes the MD5 hash of a file."""

    description = __doc__
    input_variables = {
        "pathname": {
            "required": False,
            "description": (
                "Path to the file to hash. Normally set for you by a preceding "
                "download step (e.g. URLDownloaderPython)."
            ),
        },
    }
    output_variables = {
        "filehasher_md5": {
            "description": "The file's MD5 hex digest.",
        },
    }

    def main(self):
        """Execution starts here. AutoPkg calls this once per recipe step."""


if __name__ == "__main__":
    FileHasher().execute_shell()
```

See this code in the file here: [step_02_interface.py](step_02_interface.py)

To run it (from the `FileHasher/` folder):

```bash
/usr/local/autopkg/python stages/step_02_interface.py pathname=stages/sample.txt verbose=1
```

Or run it for you: `bash stages/step_02_interface.sh`

Declaring the variables documents the processor — it's what shows up if you run
`autopkg processor-info FileHasher` — but **declaring is not doing**. Run it and
`filehasher_md5` still isn't in the output plist, because `main()` is empty.

Why `"required": False` for `pathname`? Because in a real recipe an upstream download
step sets `pathname` for us; the recipe author doesn't pass it by hand. Marking it
required would make AutoPkg reject the recipe before the download ever runs. (We'll
see that hand-off at the very end.)

## Your turn

Make `main()` compute the hash. You already have the path — pull it out of the
environment and feed it to `md5`:

1. Add `from hashlib import md5` near the top (below the `sys.path` line is fine).
2. In `main()`, read the path: `pathname = self.env.get("pathname")`.
3. Hash it and store the result in `self.env["filehasher_md5"]`.
4. Announce it with `self.output(...)`.

The obvious move is to hand `pathname` straight to `md5()`:

```python
self.env["filehasher_md5"] = md5(pathname).hexdigest()
```

Try it, and it stops with:

```
TypeError: Strings must be encoded before hashing
```

`pathname` is a **string** (text), but hash functions work on **bytes**. A string
can be written in different encodings, so `hashlib` refuses to guess — you have to
hand it bytes. The usual way to turn a string into bytes is `.encode()`:

```python
self.env["filehasher_md5"] = md5(pathname.encode()).hexdigest()
```

That runs. Use it as your answer for this step — then open the next step, because a
version that *runs* isn't the same as a version that's *right*.

---

[← Step 1](step_01_skeleton.md) · [Workshop index](../README.md) · [Step 3 — the pathname gotcha →](step_03_hash_the_path.md)
