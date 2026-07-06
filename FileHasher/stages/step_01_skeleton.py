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
