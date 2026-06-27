#!/usr/local/autopkg/python
#
# Your Name Here - 2026
#
# Copy this file to start a brand-new processor:
#   cp _template.py MyProcessor.py
#
# Then rename the class (and the references to it) from `MyProcessor` to
# whatever you are building. The FILE NAME and the CLASS NAME must match,
# because AutoPkg imports the processor by name (see docs/04-publishing.md).
#
"""See docstring for MyProcessor class"""

# Every processor imports at least these two names from autopkglib.
# `Processor`      - the base class every processor inherits from.
# `ProcessorError` - raise this to stop the recipe with a clear message.
from autopkglib import (  # pylint: disable=import-error,unused-import
    Processor,
    ProcessorError,
)

# __all__ controls what `from MyProcessor import *` exports. AutoPkg looks
# for a class whose name matches the processor name; listing it here is the
# convention used throughout this repo.
__all__ = ["MyProcessor"]


class MyProcessor(Processor):  # pylint: disable=invalid-name
    """One-sentence summary of what this processor does (shown by `autopkg info`)."""

    # AutoPkg shows `description` in `autopkg processor-info`. The idiom below
    # reuses the class docstring as the description, then restores __doc__.
    description = __doc__

    # Inputs the recipe author may pass via the `Arguments:` block.
    #   required:    True  -> AutoPkg errors if the recipe omits it
    #   default:     value used when the recipe omits an optional input
    #   description: human-readable help text (shown by `autopkg info`)
    input_variables = {
        "example_input": {
            "required": False,
            "default": "",
            "description": "Describe what this input is for.",
        },
    }

    # Variables this processor writes back into the shared recipe environment
    # so that later steps (or `autopkg run -vv`) can use them.
    output_variables = {
        "example_output": {
            "description": "Describe what this output contains.",
        },
    }

    __doc__ = description

    def main(self):
        """Execution starts here. This runs once per recipe step."""
        # 1. READ inputs from the shared environment (self.env), where a
        #    recipe's Arguments arrive. Coerce types when needed (env values
        #    can be text, e.g. int() a number).
        example_input = self.env.get("example_input", "")

        # 2. DO the work. Keep it small and testable.
        #    Use self.output(message, verbose_level) to log; higher level =
        #    only shown with more -v flags (0 always shows, 4 is very verbose).
        self.output(f"example_input was: {example_input}", 1)
        result = example_input

        # 3. WRITE outputs back to the environment for later steps to read.
        self.env["example_output"] = result


# This block lets you run the processor directly from the command line for
# quick testing, e.g. `python MyProcessor.py`. AutoPkg uses execute_shell().
if __name__ == "__main__":
    PROCESSOR = MyProcessor()
    PROCESSOR.execute_shell()
