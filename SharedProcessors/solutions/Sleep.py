#!/usr/local/autopkg/python
#
# James Stewart @JGStew - 2026
#
# SOLUTION for Lesson 2. Compare against your SharedProcessors/Sleep.py.
#
"""See docstring for Sleep class"""

import time

from autopkglib import (  # pylint: disable=import-error,unused-import
    Processor,
    ProcessorError,
)

__all__ = ["Sleep"]


class Sleep(Processor):  # pylint: disable=invalid-name
    """Pauses AutoPkg recipe execution for a specified number of seconds."""

    description = __doc__
    input_variables = {
        "sleep_seconds": {
            "required": False,
            "default": 15,
            "description": "seconds to sleep",
        },
    }
    output_variables = {}
    __doc__ = description

    def main(self):
        """Execution starts here."""
        # Recipe arguments often arrive as strings ("5"), so coerce to int.
        sleep_seconds = int(self.env.get("sleep_seconds", 15))

        self.output(f"Pausing execution for {sleep_seconds} seconds")

        time.sleep(sleep_seconds)

        self.output(f"Resuming execution after {sleep_seconds} seconds")


if __name__ == "__main__":
    PROCESSOR = Sleep()
    PROCESSOR.execute_shell()
