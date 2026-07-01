# Step 4 — hash the file's bytes

Step 3's task, completed: instead of hashing the `pathname` string, we `open()` the
file in binary mode, read its bytes, and hash **those**.

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

        with open(pathname, "rb") as f:
            data = f.read()

        self.env["filehasher_md5"] = md5(data).hexdigest()
        self.output(f"MD5: {self.env['filehasher_md5']}")
```

See this code in the file here: [step_04_read_the_file.py](step_04_read_the_file.py)

To run it (from the `FileHasher/` folder):

```bash
/usr/local/autopkg/python stages/step_04_read_the_file.py pathname=stages/sample.txt verbose=1
```

Or run it for you: `bash stages/step_04_read_the_file.sh`

Now it works, and the output plist finally gains a `filehasher_md5`:

```
FileHasher: MD5: 26f2a1dca7b430081e9654a2413d6642
```

That's the MD5 of the bundled [`sample.txt`](sample.txt) — you should get exactly the
same value. Move or rename the file and this hash won't change (it's about the
contents); change a single byte inside it and the hash will. That's the whole point
of hashing the file instead of its name.

- **`with open(pathname, "rb")`** opens the file for reading in binary. The `with`
  block closes it for you when you're done.
- **`f.read()`** hands back the file's raw bytes, which is exactly what `md5()` wants.
- **`self.env["filehasher_md5"] = ...`** is the result *leaving* the processor —
  anything written to `self.env` is what the next processor in a recipe can read.

**That's the finished processor.** It's copied to
[`FileHasher.py`](../FileHasher.py) in the folder above, ready to drop into a recipe
— which is exactly what we do next.

---

[← Step 3](step_03_hash_the_path.md) · [Workshop index](../README.md) · [The finished processor & recipe →](../README.md#the-finished-processor)
