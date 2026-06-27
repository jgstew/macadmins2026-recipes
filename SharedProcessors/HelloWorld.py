#!/usr/local/autopkg/python
#
# Your Name Here - 2026
#
# LESSON 1 EXERCISE: the anatomy of a processor.
# Fill in the TODOs below. Reference: docs/01-anatomy.md
# Stuck? The working answer is in solutions/HelloWorld.py
#
"""See docstring for HelloWorld class"""

from autopkglib import (  # pylint: disable=import-error,unused-import
    Processor,
    ProcessorError,
)

__all__ = ["HelloWorld"]


class HelloWorld(Processor):  # pylint: disable=invalid-name
    """Greets a named recipient and returns the greeting as a string."""

    description = __doc__
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World",
            "description": "Name to include in the greeting (default: World)",
        },
    }
    output_variables = {
        "greeting_result": {
            "description": "The full greeting string that was produced",
        },
    }
    __doc__ = description

    def main(self):
        """Execution starts here."""
        # This part is done for you: read the input from the shared environment.
        greeting_name = str(self.env.get("greeting_name", "World"))

        # TODO 1: build a greeting string that includes greeting_name,
        #         e.g. "Hello, World!"  (try an f-string)
        # greeting = ...

        # TODO 2: log it so it shows up in `autopkg run` output.
        # self.output(greeting)

        # TODO 3: store the greeting in the output variable so later steps
        #         (and the test recipe) can read it.
        # self.env["greeting_result"] = greeting

        # TODO 4: delete the line below once the TODOs above are complete.
        raise ProcessorError("TODO: complete Lesson 1 in SharedProcessors/HelloWorld.py")


if __name__ == "__main__":
    PROCESSOR = HelloWorld()
    PROCESSOR.execute_shell()
