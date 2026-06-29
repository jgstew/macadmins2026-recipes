# Step 8 — accept input from the recipe

```python
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


if __name__ == "__main__":
    HelloWorld({"verbose": 1, "greeting_name": "MacAdmins (step 8)"}).main()
```

```bash
/usr/local/autopkg/python stages/step_08_inputs.py
#  HelloWorld: Hello MacAdmins (step 8)!
```

Or run it for you: `bash stages/step_08_inputs.sh`

**Why:** A hardcoded greeting isn't worth much. `input_variables` **declares**
what a recipe is allowed to pass in — each input's name, whether it's
`required`, a `default` for when the recipe omits it, and a `description`
(this is what `autopkg processor-info HelloWorld` prints). The actual value
arrives in `self.env`, and we read it with `self.env.get("greeting_name",
"World")`.

We pass `greeting_name` in through the env dict here, just like a recipe's
`Arguments:` will. Change the value and the output changes — without touching
`main()`. That parameterization is the entire point of a processor.

---

[← Step 7 — `self.output()`](step_07_self_output.md) · [Workshop index](../README.md) · [Step 9 — produce a result →](step_09_outputs.md)
