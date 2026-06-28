# Step 8 — accept input from the recipe.
#
# Run it:  /usr/local/autopkg/python stages/step_08_inputs.py
#
# A hardcoded "World" isn't useful. input_variables DECLARES what a recipe is
# allowed to pass in: each input's name, whether it is required, a default when
# the recipe omits it, and a human-readable description (shown by
# `autopkg processor-info`). The actual value arrives in self.env, which we read
# with self.env.get().
#
# Change "MacAdmins" below (or, later, the recipe) and the greeting changes —
# without touching main(). That is the whole point of an input.

import sys

sys.path.insert(0, "/Library/AutoPkg")

from autopkglib import Processor  # noqa: E402


class HelloWorld(Processor):
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World (step 8)",
            "description": "Name to greet (default: World (step 8)).",
        },
    }
    output_variables = {}

    def main(self):
        greeting_name = self.env.get("greeting_name", "World (step 8)")
        self.output(f"Hello {greeting_name}!")


# Stand in for AutoPkg: pass greeting_name in through the env, like a recipe would.
if __name__ == "__main__":
    HelloWorld({"verbose": 1, "greeting_name": "MacAdmins (step 8)"}).main()
