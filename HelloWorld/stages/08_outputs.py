# Step 8 — produce a result later steps can use.
#
# Run it:  PYTHONPATH=../../autopkg/Code /usr/local/autopkg/python stages/08_outputs.py
#
# A processor usually hands something to the next step in the recipe. We build
# the greeting, then store it back in self.env under a name we declare in
# output_variables. Anything written to self.env is visible to every later
# processor in the recipe (and is shown by `autopkg run -vv`).
#
# The last lines peek into the environment afterward to prove the value is
# really sitting there for the next step to pick up.

from autopkglib import Processor


class HelloWorld(Processor):
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
        greeting_name = self.env.get("greeting_name", "World")
        greeting = f"Hello {greeting_name}!"
        self.output(greeting)
        self.env["greeting_result"] = greeting


# Stand in for AutoPkg, then inspect what landed in the shared environment.
if __name__ == "__main__":
    processor = HelloWorld({"verbose": 1, "greeting_name": "MacAdmins"})
    processor.main()
    print("greeting_result is now:", processor.env["greeting_result"])
