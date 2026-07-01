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


if __name__ == "__main__":
    FileHasher().execute_shell()
