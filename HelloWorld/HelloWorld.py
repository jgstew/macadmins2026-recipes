#!/usr/local/autopkg/python
# Created 2026 by YourNameHere
#
# Step 10 — the finished processor.
#
# This is stage 09 plus the conventional boilerplate every shipped processor
# carries. Note there's no sys.path tweak (Step 6): when AutoPkg runs your recipe
# it already has autopkglib on the path, so a shipped processor never hard-codes
# it. README.md explains how we got here from a one-line script and what each
# piece below is for. The class name (HelloWorld) matches the file name
# (HelloWorld.py) on purpose: that is how AutoPkg locates the processor.
#
"""See docstring for HelloWorld class"""

# Processor is the base class. ProcessorError is what you raise to stop a recipe
# with a clear message (imported here so it is ready when you need it).
from autopkglib import Processor, ProcessorError  # noqa: F401

# __all__ lists the module's public names (what `from module import *` exports).
# AutoPkg doesn't need it (it loads the class by name); shipped processors
# include it by convention.
__all__ = ["HelloWorld"]


class HelloWorld(Processor):
    """Greets a named recipient and stores the greeting as an output variable."""

    # AutoPkg shows `description` in `autopkg processor-info`.
    # This idiom reuses the class docstring as the description.
    description = __doc__
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World",
            "description": "Name to greet (default: World).",
        },
    }
    output_variables = {
        "greeting_result": {
            "description": "The greeting that was produced.",
        },
    }

    def main(self):
        """Execution starts here. AutoPkg calls this once per recipe step."""
        greeting_name = self.env.get("greeting_name", "World")
        greeting = f"Hello {greeting_name}!"
        self.output(greeting)
        self.env["greeting_result"] = greeting


# Lets you run the file directly (AutoPkg-style) for quick testing. execute_shell
# reads an input plist from stdin, applies defaults, calls main(), and writes the
# resulting environment back out as a plist. See README.md for how to feed it.
if __name__ == "__main__":
    PROCESSOR = HelloWorld()
    PROCESSOR.execute_shell()
