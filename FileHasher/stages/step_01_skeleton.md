# Step 1 — the bare skeleton

This is the least code AutoPkg will still recognize as a processor. It's the same
shape you finished HelloWorld with — a class that subclasses `Processor`, a
`main()` method, an `input_variables` dict, and an `output_variables` dict — but
everything is empty, so it does nothing yet. We'll fill it in one step at a time,
and **each step's file is the completed answer to the previous step's task**, so
you can always check your work.

```python
#!/usr/local/autopkg/python
"""See docstring for FileHasher class"""

import sys

sys.path.insert(0, "/Library/AutoPkg")  # look here first when importing

from autopkglib import Processor

__all__ = ["FileHasher"]


class FileHasher(Processor):
    """FileHasher processor."""

    description = __doc__

    # input_variables: every value this processor reads from the
    # environment. Document each one. Example entry:
    #     "example_input": {
    #         "required": False,
    #         "default": "",
    #         "description": "What this input controls.",
    #     },
    input_variables = {}

    # output_variables: every value this processor writes back to
    # the environment. Document each one. Example entry:
    #     "example_output": {
    #         "description": "What this output contains.",
    #     },
    output_variables = {}

    def main(self):
        """Execution starts here."""


if __name__ == "__main__":
    FileHasher().execute_shell()
```

See this code in the file here: [step_01_skeleton.py](step_01_skeleton.py)

To run it (from the `FileHasher/` folder):

```bash
/usr/local/autopkg/python stages/step_01_skeleton.py pathname=stages/sample.txt verbose=1
```

Or run it for you: `bash stages/step_01_skeleton.sh`

Two things carried over from HelloWorld:

- **`sys.path.insert(0, "/Library/AutoPkg")`** is how we point Python at `autopkglib`
  from inside the code — the same trick as
  [HelloWorld Step 6](../../HelloWorld/stages/step_06_sys_path.md), so there's no
  `PYTHONPATH` prefix to remember. The `from autopkglib import Processor` has to come
  *after* it, once the path is set.
- **`execute_shell()`** in the `if __name__ == "__main__"` block lets you run the
  processor from the command line. It reads `key=value` arguments (`pathname=...`,
  `verbose=1`) into `self.env` for you.

It runs, and prints an output plist showing what ended up in `self.env`:

```xml
<dict>
	<key>pathname</key>
	<string>.../sample.txt</string>
	<key>verbose</key>
	<string>1</string>
</dict>
```

Notice what's **not** there: no `filehasher_md5`. We were handed a `pathname` but
produced nothing, because `main()` is empty. That plist is our progress bar for the
next few steps — watch for `filehasher_md5` to appear.

## Your turn

A processor should declare what it reads and what it writes. Replace the two empty
dicts (the comments show the shape):

- add a **`pathname`** entry to `input_variables` — the file to hash.
- add a **`filehasher_md5`** entry to `output_variables` — the digest we'll return.

Give each one a `description`. Leave `main()` empty for now — just the declarations.

Done? The next step is that same file with the interface filled in — check your
work against it.

---

[Workshop index](../README.md) · [Step 2 — declare the interface →](step_02_interface.md)
