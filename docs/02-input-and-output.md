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

Even with a declared `default`, read inputs defensively in `main()`:

```python
sleep_seconds = int(self.env.get("sleep_seconds", 15))
```

### Everything can arrive as a string

Recipe `Arguments:` values — especially from YAML and from `%VARIABLE%`
substitution — often reach you as **strings**. If you need a number, coerce it:

```python
sleep_seconds = int(self.env.get("sleep_seconds", 15))   # "5"  -> 5
```

The `Sleep` test recipe deliberately passes `"2"` (a string) to prove your
`int()` call works. This is the single most common bug in a new processor.

### Inputs can be richer than strings

Inputs can be lists or dicts too. `StringFormat` takes a `format_kwargs` dict:

```python
format_kwargs = self.env.get("format_kwargs", {})   # default to empty dict
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

Wrap risky operations and re-raise with context — `StringFormat` turns a bad
format string into a helpful error:

```python
try:
    formatted_string = format_string.format(format_value, **kwargs)
except (KeyError, IndexError, ValueError) as err:
    raise ProcessorError(f"Failed to format `{format_string}`: {err}") from err
```

Next: [3. Testing your processor](03-testing.md).
