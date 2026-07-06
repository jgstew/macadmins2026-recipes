# Step 3 — the pathname gotcha

Here is the version you landed on at the end of Step 2 — `md5(pathname.encode())`.
It runs, it prints a perfectly real-looking hash — and it's wrong. This is the
mistake almost everyone makes once.

```python
#!/usr/local/autopkg/python
"""See docstring for FileHasher class"""

from hashlib import md5
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
        pathname = self.env.get("pathname")

        self.env["filehasher_md5"] = md5(pathname.encode()).hexdigest()
        self.output(f"MD5: {self.env['filehasher_md5']}")
```

See this code in the file here: [step_03_hash_the_path.py](step_03_hash_the_path.py)

To run it (from the `FileHasher/` folder):

```bash
/usr/local/autopkg/python stages/step_03_hash_the_path.py pathname=stages/sample.txt verbose=1
#  FileHasher: MD5: aad6cd2e48ed2abc2a89a682c31dccd9
```

Or run it for you: `bash stages/step_03_hash_the_path.sh`

In Step 2, `.encode()` got us past the `TypeError` — but making the error go away is
exactly the trap, because it lets a wrong program *look* like it works.

It runs and prints `aad6cd2e48ed2abc2a89a682c31dccd9`. That's a genuine MD5 — of the
**characters of the path**, `s`, `t`, `a`, `g`, `e`, `s`, `/`, … — not of the file
those characters point to. Two ways to see that it's wrong:

- **Run it for you** with `bash stages/step_03_hash_the_path.sh` and you get a
  *different* hash for the *same file*, because the runner passes the file's absolute
  path — different path text, different result.
- The real hash of the file's contents (coming in Step 4) is
  `26f2a1dca7b430081e9654a2413d6642`, and this value never matches it. Edit the bytes
  inside `sample.txt` and this hash won't budge; rename the file and it changes.

The `pathname` is a signpost, not the thing it points to. To hash the file, we have
to **open it and read its bytes**.

## Your turn

Hash the file's contents instead of its name:

1. `open()` the file at `pathname` in **binary** mode (`"rb"`) — binary because we
   want the raw bytes, and because a download isn't necessarily text.
2. Read the bytes out of it.
3. Pass *those bytes* to `md5(...)` (no `.encode()` needed — they're already bytes).

Done? Check the next step.

---

[← Step 2](step_02_interface.md) · [Workshop index](../README.md) · [Step 4 — hash the file's bytes →](step_04_read_the_file.md)
