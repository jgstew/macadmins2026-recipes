# 2. Inputs, outputs, and `self.env`

Everything a processor reads and writes flows through `self.env`, a dictionary
shared by every step in the recipe. `input_variables` and `output_variables`
*document and validate* that flow — they don't store the values themselves.

## `input_variables`

A dict of the inputs your processor accepts. Each entry supports:

| key           | meaning                                                              |
|---------------|----------------------------------------------------------------------|
| `required`    | `True` → AutoPkg errors if the recipe omits it. `False` → optional.  |
| `default`     | value used when an optional input is omitted.                        |
| `description` | help text shown by `autopkg processor-info <Name>`.                  |

```python
input_variables = {
    "sleep_seconds": {
        "required": False,
        "default": 15,
        "description": "seconds to sleep",
    },
}
```

Even with a declared `default`, read inputs in `main()` from `self.env` — the
shared recipe environment is the source of truth for what the recipe passed:

```python
sleep_seconds = self.env.get("sleep_seconds", 15)
```

### How a recipe's `Arguments:` reach your processor

When a recipe step lists `Arguments:`, AutoPkg copies each one into the shared
`self.env` *before* it calls your `main()`; your processor reads them back out by
name. That hand-off is the whole point of inputs:

```yaml
# in the recipe step
- Processor: .../Sleep
  Arguments:
    sleep_seconds: "2"      # the recipe author sets a key...
```

```python
# in the processor's main()
sleep_seconds = int(self.env.get("sleep_seconds", 15))   # ...the processor reads it
```

The `Sleep` test recipe passes `sleep_seconds` exactly this way to demonstrate
the hand-off.

> Aside: an argument arrives as whatever the recipe author typed — here the
> quoted string `"2"`. (Separately, when a value contains a `%VARIABLE%` token,
> that substitution always yields a string.) Either way, wrap a value in
> `int(...)` when you need it as a number — which is why the snippet above does.

### An input can be a dict or list, not just a single value

A declared input can hold structured data, not only a scalar. `StringFormat` —
a processor that **transforms its inputs into an output** — declares a
`format_kwargs` dict input of named values to fold into the result:

```python
format_kwargs = self.env.get("format_kwargs", {})   # a dict-valued input
```

## `output_variables`

A dict documenting what you write back into `self.env`. Declaring an output
makes it show up in `autopkg run -vv` and lets later recipe steps depend on it.

```python
output_variables = {
    "greeting_result": {"description": "The full greeting string"},
}
```

You produce the value in `main()` by assigning to `self.env`:

```python
self.env["greeting_result"] = greeting
```

A processor can set **several** outputs. `FileHasher` sets four
(`filehasher_sha1`, `filehasher_sha256`, `filehasher_md5`, `filehasher_size`).

## Chaining: reading another step's output

Because `self.env` is shared, a processor can read a value an earlier step
produced. The classic example is `pathname`, set by download processors.
`FileHasher` falls back to it so it can run right after a download:

```python
file_path = self.env.get("file_path", self.env.get("pathname"))
```

In a recipe, `%pathname%` refers to that same variable. This is how processors
compose into a pipeline.

## `self.output()` and verbosity

`self.output(message, verbose_level=0)` logs a line. The level controls how many
`-v` flags are needed to see it:

| level | shown at        | use for                                  |
|-------|-----------------|------------------------------------------|
| 0     | always          | important results, warnings              |
| 1     | `-v`            | normal progress                          |
| 2–3   | `-vv` / `-vvv`  | detail useful when debugging             |
| 4     | `-vvvv`         | very noisy dumps (full env, raw headers) |

```python
self.output("Downloaded the file")          # level 0 — always
self.output(f"File SHA256 = {digest}", 1)    # level 1 — with -v
```

## Failing loudly: `ProcessorError`

When something is wrong, raise `ProcessorError` to stop the recipe with a clear
message instead of letting a raw traceback escape:

```python
if not file_path:
    raise ProcessorError("No file_path (or pathname) provided to hash!")
```

Wrap risky work and re-raise with context. `StringFormat` is a processor that
transforms an input value into an output value; when the input can't be
processed it surfaces a clear, recipe-level message instead of a raw traceback:

```python
try:
    formatted_string = format_string.format(format_value, **kwargs)
except (KeyError, IndexError, ValueError) as err:
    raise ProcessorError(f"Failed to format `{format_string}`: {err}") from err
```

The transform here happens to use Python's `str.format()`, but the AutoPkg
takeaway is the pattern: do the work, and raise `ProcessorError` with context
when it fails.

Next: [3. Testing your processor](03-testing.md).
