#!/usr/local/autopkg/python
#
# James Stewart @JGStew - 2026
#
# SOLUTION for Lesson 4. Compare against your SharedProcessors/FileHasher.py.
#
"""See docstring for FileHasher class"""

from hashlib import md5, sha1, sha256

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
        """Compute SHA1, SHA256, MD5 and byte size of a file in one streaming pass.

        Streaming in chunks means even a multi-GB file never has to be loaded
        fully into memory, and it is read from disk only once for all 3 hashes.
        """
        hashes = sha1(), sha256(), md5()

        # Read in chunks at least as large as the biggest hash block size.
        chunksize = max(409600, max(a_hash.block_size for a_hash in hashes))
        size = 0

        with open(file_path, "rb") as file_stream:
            while True:
                chunk = file_stream.read(chunksize)
                if not chunk:
                    break
                size += len(chunk)
                for a_hash in hashes:
                    a_hash.update(chunk)

        self.output(f"File MD5    = {hashes[2].hexdigest()}", 1)
        self.output(f"File SHA1   = {hashes[0].hexdigest()}", 1)
        self.output(f"File SHA256 = {hashes[1].hexdigest()}", 1)
        self.output(f"File Size   = {size}", 1)

        self.env["filehasher_sha1"] = hashes[0].hexdigest()
        self.env["filehasher_sha256"] = hashes[1].hexdigest()
        self.env["filehasher_md5"] = hashes[2].hexdigest()
        self.env["filehasher_size"] = str(size)

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
