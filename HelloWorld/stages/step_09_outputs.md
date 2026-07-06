# Step 9 — produce a result for the next step

We declare an `output_variables` entry and write the greeting back into `self.env` so a later step can use it.

```python
class HelloWorld(Processor):
    input_variables = {
        "greeting_name": {
            "required": False,
            "default": "World (step 9)",
            "description": "Name to greet (default: World (step 9)).",
        },
    }
    output_variables = {
        "greeting_result": {
            "description": "The greeting that was produced.",
        },
    }

    def main(self):
        greeting_name = self.env.get("greeting_name", "World (step 9)")
        greeting = f"Hello {greeting_name}!"
        self.output(greeting)
        self.env["greeting_result"] = greeting


if __name__ == "__main__":
    processor = HelloWorld({"verbose": 1, "greeting_name": "MacAdmins (step 9)"})
    processor.main()
    print("greeting_result is now:", processor.env["greeting_result"])
```

See this code in the file here: [step_09_outputs.py](step_09_outputs.py)

To run it (from the `HelloWorld/` folder):

```bash
/usr/local/autopkg/python stages/step_09_outputs.py
#  HelloWorld: Hello MacAdmins (step 9)!
#  greeting_result is now: Hello MacAdmins (step 9)!
```

Or run it for you: `bash stages/step_09_outputs.sh`

**Why:** A processor usually hands something to the next processor in the recipe.
We store our greeting back into `self.env["greeting_result"]`, and **declare**
that output in `output_variables`. Anything in `self.env` is visible to every
later step (and shown by `autopkg run -vv`). The last two lines peek into the
environment to prove the value is sitting there, ready for the next processor.

---

[← Step 8 — accept input](step_08_inputs.md) · [Workshop index](../README.md) · [Step 10 — the finished processor →](step_10_finished_processor.md)
