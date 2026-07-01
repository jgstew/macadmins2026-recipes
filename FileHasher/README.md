# Build a Real Processor: a File Hasher

A hands-on workshop. PSU MacAdmins 2026. *(Do the [HelloWorld workshop](../HelloWorld/README.md) first — this one assumes it.)*

In HelloWorld you built a processor that just greets you. Now we'll build one that
does **real work**: it computes the MD5 hash of a file — the kind of thing AutoPkg
does to check a download — and then chains after a downloader in a recipe.

This time we don't start from `print()`. You already know the processor skeleton, so
we start from a **bare but complete skeleton** and add one thing at a time. The twist:
**each step's file is the finished answer to the previous step's task.** Read a page,
make the change yourself, then open the next step to check your work. One of the
steps is a deliberate wrong turn — the single most common file-hashing mistake — so
you meet it on purpose instead of in production.

---

## Setup

Same as HelloWorld: install the AutoPkg pkg (so you have `/usr/local/autopkg/python`
and `/Library/AutoPkg/`; see the [HelloWorld setup](../HelloWorld/README.md#setup)),
then work from inside this folder:

```bash
cd FileHasher
```

Each stage runs standalone with the bundled Python. As in
[HelloWorld Step 6](../HelloWorld/stages/step_06_sys_path.md), the code adds
`/Library/AutoPkg` to `sys.path` itself, so there's no `PYTHONPATH` prefix to
remember. Inputs are passed as `key=value` (which `execute_shell()` reads into
`self.env`):

```bash
/usr/local/autopkg/python stages/step_01_skeleton.py pathname=stages/sample.txt verbose=1
```

There's a [`stages/sample.txt`](stages/sample.txt) to hash. Its MD5 is
`26f2a1dca7b430081e9654a2413d6642` — you'll see that value appear once the processor
is reading the file correctly, and it's the same every time.

**Troubleshooting:** `ModuleNotFoundError: No module named 'autopkglib'` means you're
not using `/usr/local/autopkg/python`, or the `sys.path.insert(...)` line is missing
or sits below the `from autopkglib import ...` line.

---

## The steps

Work through these in order, from the `FileHasher/` folder. Each page shows the code
you're starting from, the command to run it, and one task to complete. The next
page's file is the answer.

1. [The bare skeleton](stages/step_01_skeleton.md) — a complete but empty processor. *Task: declare the interface.*
2. [Declare the interface](stages/step_02_interface.md) — `pathname` in, `filehasher_md5` out. *Task: compute the hash in `main()`.*
3. [The pathname gotcha](stages/step_03_hash_the_path.md) — hashing the *path string* is the wrong turn. *Task: hash the file's bytes instead.*
4. [Hash the file's bytes](stages/step_04_read_the_file.md) — open the file, read it, hash it. The finished processor.

---

## The finished processor

Reading the file's bytes (the Step 4 task, done) gives us the finished
[`FileHasher.py`](FileHasher.py):

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

Everything here is Python's standard library (`hashlib`) plus `autopkglib` — nothing
to install.

## Chain it in a recipe

A processor on its own isn't very useful — the point is to combine it with others.
Because `FileHasher` reads `pathname` (rather than a path you pass in), it drops in
right after a download step with **no arguments**. Here is
[`FileHasher.recipe.yaml`](FileHasher.recipe.yaml):

```yaml
Description: Download a file and compute its MD5.
Identifier: com.github.jgstew.macadmins2026.FileHasher
Input:
  NAME: FileHasherDemo
  url: "https://raw.githubusercontent.com/autopkg/autopkg/v2.9.0/LICENSE.txt"
MinimumVersion: "2.3"
Process:
  - Processor: URLDownloaderPython
    Arguments:
      url: "%url%"

  - Processor: FileHasher
```

1. **`URLDownloaderPython`** downloads the URL and sets `pathname`. It's built into
   AutoPkg and pure Python, so it behaves the same on macOS, Linux, and Windows —
   nothing extra to install.
2. **`FileHasher`** takes no arguments; it just hashes the `pathname` the download
   left behind. That hand-off through `self.env` is the whole point of a recipe.

Run it from this folder:

```bash
autopkg run -v FileHasher.recipe.yaml --search-dir .
```

`--search-dir .` tells AutoPkg to look in this folder for `FileHasher.py` (AutoPkg
finds a processor by matching the recipe's `Processor:` name to a same-named `.py`
file). You should see it download the file and print:

```
FileHasher: MD5: 7e08890fe701943d5e845985957750b3
```

The URL is pinned to AutoPkg's `v2.9.0` tag, so that hash is the same every time.

**Explore:** MD5 is fine for a quick integrity check but isn't secure against
tampering. Swap `from hashlib import md5` / `md5()` for `sha256` / `sha256()` (and
rename the output variable), then re-run. The `hashlib` API is identical across
algorithms — that's the only change needed.

---

## Recap

Starting from a complete-but-empty skeleton, you built a useful processor by
answering, one step at a time:

1. **What goes in and out?** → `pathname` and `filehasher_md5`, declared
   ([Step 1–2](stages/step_02_interface.md))
2. **What do you actually hash?** → the file's **bytes**, not the pathname string —
   the gotcha that trips up nearly everyone ([Step 3](stages/step_03_hash_the_path.md))
3. **How?** → `open(pathname, "rb")`, read, `md5(...)` ([Step 4](stages/step_04_read_the_file.md))
4. **The payoff:** `URLDownloaderPython` → `FileHasher`, a two-processor recipe with
   no dependencies beyond AutoPkg

Same `self.env` hand-off as HelloWorld — now with two real processors in a row.

## A more advanced version

Ours reads the whole file at once and computes one hash. A production processor does
more: it **streams** the file in chunks (so a multi-gigabyte download doesn't load
into memory all at once), raises a **`ProcessorError`** when the file is missing, and
often returns **several** hashes plus the file size in a single pass. For a real
example, see
[`FileHasher` in jgstew-recipes](https://github.com/autopkg/jgstew-recipes/blob/main/SharedProcessors/FileHasher.py)
— the same shape you just built, with those refinements added.
