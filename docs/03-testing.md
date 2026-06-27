# 3. Testing your processor

There are two layers of testing in this repo, cheapest first.

## Layer 1: does it import? (`test_processors_load.sh`)

A processor that can't be imported can never run. The load test imports every
`.py` under `SharedProcessors/` (and `solutions/`) and reports `PASS`/`FAIL`:

```bash
./test_processors_load.sh        # quiet
./test_processors_load.sh -v     # also show captured output
```

This catches syntax errors, bad imports, and typos in seconds — without needing
a recipe. The unfinished exercise files **pass** this layer: importing loads the
code but does not run `main()`, so the `raise ProcessorError("TODO: ...")` guard
inside them never fires here.

## Layer 2: does it behave? (test recipes)

Each lesson ships a `*.test.recipe.yaml` that runs the processor and then checks
the result with the `AssertInputContainsString` processor (provided complete).
Run one by file path, pointing AutoPkg at `SharedProcessors/` so it can find the
processors:

```bash
autopkg run -vv Test-Recipes/HelloWorld.test.recipe.yaml --search-dir SharedProcessors
```

A test recipe is an ordinary recipe: a `Process:` list of steps. The pattern is
**run your processor, then assert on what it put in `self.env`**:

```yaml
Process:
  - Processor: com.github.jgstew.macadmins2026.SharedProcessors/HelloWorld
    Arguments:
      greeting_name: "MacAdmins"

  - Processor: com.github.jgstew.macadmins2026.SharedProcessors/AssertInputContainsString
    Arguments:
      input_string: "%greeting_result%"   # <- the output your processor set
      assert_string: "Hello, MacAdmins!"  # <- must appear inside it
```

`%greeting_result%` is variable substitution: AutoPkg replaces it with the value
in `self.env`. If the substring is missing, `AssertInputContainsString` raises
and the recipe fails — that's your test failing.

### Expected first run

Before you finish a lesson, its processor ends with
`raise ProcessorError("TODO: ...")`, so the recipe fails immediately with a
message naming the file to edit. Implement the TODOs, delete that line, and run
again until it passes.

### The whole suite

`Test-Recipes/Workshop.recipelist.txt` lists all four recipes by identifier so
you can run them together once the repo is registered with AutoPkg:

```bash
autopkg run --recipe-list Test-Recipes/Workshop.recipelist.txt
```

## Layer 3 (bonus): poke it directly in Python

For tight feedback while writing logic, skip recipes entirely:

```bash
PYTHONPATH="../autopkg/Code:SharedProcessors" python3 <<'EOF'
from FileHasher import FileHasher
p = FileHasher({})
p.env["file_path"] = "Test-Recipes/sample.txt"
p.main()
print(p.env["filehasher_sha256"], p.env["filehasher_size"])
EOF
```

Next: [4. Sharing your processor](04-publishing.md).
