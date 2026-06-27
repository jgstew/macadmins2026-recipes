#!/usr/local/autopkg/python
#
# Your Name Here - 2026
#
# LESSON 3 EXERCISE: required inputs, dict inputs, and failing loudly.
# Fill in the TODOs below. Reference: docs/02-input-and-output.md
# Stuck? The working answer is in solutions/StringFormat.py
#
"""See docstring for StringFormat class"""

from autopkglib import (  # pylint: disable=import-error,unused-import
    Processor,
    ProcessorError,
)

__all__ = ["StringFormat"]


class StringFormat(Processor):  # pylint: disable=invalid-name
    """Formats a string using Python str.format(), supporting zero-padding, alignment, and named substitutions."""

    description = __doc__
    input_variables = {
        "format_string": {
            "required": True,
            "description": (
                "A Python format string. The single value is available as `{}`, "
                "`{0}`, or `{value}`; named values from format_kwargs are available "
                "by their key, e.g. '{name}-v{version}' or '{value:0>5}'."
            ),
        },
        "format_value": {
            "required": False,
            "default": "",
            "description": "A single value referenced as `{}`, `{0}`, or `{value}`.",
        },
        "format_kwargs": {
            "required": False,
            "default": {},
            "description": "A dict of named values referenced by key in the format string.",
        },
    }
    output_variables = {
        "formatted_string": {
            "description": "The result of applying the format string",
        },
    }
    __doc__ = description

    def main(self):
        """Execution starts here."""
        # TODO 1: read the three inputs from self.env.
        #         format_string is required; the others have defaults ("" and {}).
        # format_string = self.env.get(...)
        # format_value = self.env.get(..., "")
        # format_kwargs = self.env.get(..., {})

        # TODO 2: build the kwargs dict. Start with {"value": format_value}
        #         then merge in format_kwargs so recipe-supplied keys win.
        # kwargs = {"value": format_value}
        # kwargs.update(...)

        # TODO 3: apply the format. A bad format string is an authoring error,
        #         so wrap it in try/except and raise a ProcessorError with a
        #         helpful message instead of letting a raw traceback escape.
        # try:
        #     formatted_string = format_string.format(format_value, **kwargs)
        # except (KeyError, IndexError, ValueError) as err:
        #     raise ProcessorError(f"Failed to format `{format_string}`: {err}") from err

        # TODO 4: log it and store it in the output variable.
        # self.output(f"Formatted string: {formatted_string}")
        # self.env["formatted_string"] = formatted_string

        # TODO 5: delete the line below once the TODOs above are complete.
        raise ProcessorError("TODO: complete Lesson 3 in SharedProcessors/StringFormat.py")


if __name__ == "__main__":
    PROCESSOR = StringFormat()
    PROCESSOR.execute_shell()
