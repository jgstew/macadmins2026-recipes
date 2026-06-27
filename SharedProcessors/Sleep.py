#!/usr/local/autopkg/python
#
# Your Name Here - 2026
#
# LESSON 2 EXERCISE: optional inputs, defaults, and reading a recipe's
# Arguments from self.env.
# Fill in the TODOs below. Reference: docs/02-input-and-output.md
# Stuck? The working answer is in solutions/Sleep.py
#
"""See docstring for Sleep class"""

# TODO 1: import the standard-library module that lets you pause execution.
# import ...

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
        # TODO 2: read "sleep_seconds" from self.env with a default of 15.
        #         self.env is how a recipe's Arguments reach your processor.
        #         (Aside: env values may arrive as text, so int(...) it.)
        # sleep_seconds = int(self.env.get(..., ...))

        # TODO 3: log that you are pausing, then actually pause, then log resume.
        # self.output(f"Pausing execution for {sleep_seconds} seconds")
        # <pause here using the module you imported in TODO 1>
        # self.output(f"Resuming execution after {sleep_seconds} seconds")

        # TODO 4: delete the line below once the TODOs above are complete.
        raise ProcessorError("TODO: complete Lesson 2 in SharedProcessors/Sleep.py")


if __name__ == "__main__":
    PROCESSOR = Sleep()
    PROCESSOR.execute_shell()
