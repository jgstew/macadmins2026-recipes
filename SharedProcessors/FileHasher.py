#!/usr/local/autopkg/python
#
# Your Name Here - 2026
#
# LESSON 4 EXERCISE: file I/O, helper methods, multiple outputs, and chaining
# off %pathname% from a previous step. Reference: docs/02-input-and-output.md
# Stuck? The working answer is in solutions/FileHasher.py
#
"""See docstring for FileHasher class"""

# TODO 1: import sha1, sha256, and md5 from the standard-library hashlib module.
# from hashlib import ...

from autopkglib import (  # pylint: disable=import-error,unused-import
    Processor,
    ProcessorError,
)

__all__ = ["FileHasher"]


class FileHasher(Processor):  # pylint: disable=invalid-name
    """Computes SHA1, SHA256, and MD5 hashes and the byte size of a file in a single pass."""

    description = __doc__
    input_variables = {
        "file_path": {
            "required": False,
            "description": "Path to hash. Defaults to %pathname% (e.g. from a download step).",
        }
    }
    output_variables = {
        "filehasher_sha1": {"description": "The input file SHA1"},
        "filehasher_sha256": {"description": "The input file SHA256"},
        "filehasher_md5": {"description": "The input file MD5"},
        "filehasher_size": {"description": "The input file size in bytes"},
    }
    __doc__ = description

    def hash(self, file_path):
        """Compute SHA1, SHA256, MD5 and byte size of a file in one streaming pass."""
        # TODO 2: create the three hash objects, e.g. hashes = sha1(), sha256(), md5()
        # hashes = ...

        # TODO 3: open file_path in binary mode ("rb") and read it in chunks
        #         (a `with open(...) as f:` block plus a while loop). For each
        #         chunk: add len(chunk) to a running size, and call
        #         a_hash.update(chunk) for each hash. Stop when read() is empty.

        # TODO 4: store the four results in self.env. Hash digests come from
        #         a_hash.hexdigest(); store the size as a string.
        # self.env["filehasher_sha1"] = ...
        # self.env["filehasher_sha256"] = ...
        # self.env["filehasher_md5"] = ...
        # self.env["filehasher_size"] = ...

        # TODO 5: delete the line below once the TODOs above are complete.
        raise ProcessorError("TODO: complete Lesson 4 in SharedProcessors/FileHasher.py")

    def main(self):
        """Execution starts here."""
        # Fall back to %pathname% so this can run right after a download step
        # without the recipe author repeating the path.
        file_path = self.env.get("file_path", self.env.get("pathname"))

        if not file_path:
            raise ProcessorError("No file_path (or pathname) provided to hash!")

        self.hash(file_path)


if __name__ == "__main__":
    PROCESSOR = FileHasher()
    PROCESSOR.execute_shell()
