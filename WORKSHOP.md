# Writing AutoPkg Processors From Scratch

A hands-on workshop. PSU MacAdmins 2026.

By the end you will have written four working AutoPkg processors and understand
every line of them — enough to read, modify, and create the kind of processors
found in [`jgstew-recipes`](https://github.com/jgstew/jgstew-recipes).

An AutoPkg **processor** is a small Python class that does one job in a recipe:
download a file, read a version, hash something, transform a string. We'll build
four, each adding exactly one new idea.

## Format

Every lesson has three files:

- **`SharedProcessors/<Name>.py`** — the exercise. A working skeleton with
  `# TODO` lines for you to fill in. It ends with a `raise ProcessorError(...)`
  guard so an unfinished lesson fails with an obvious message.
- **`Test-Recipes/<Name>.test.recipe.yaml`** — runs your processor and checks
  the result. "Done" means this passes.
- **`SharedProcessors/solutions/<Name>.py`** — the worked answer. Peek when
  stuck; copy over the exercise file to move on.

## Before you start

Work through [docs/00-setup.md](docs/00-setup.md), then confirm everything
imports:

```bash
./test_processors_load.sh
```

Read [docs/01-anatomy.md](docs/01-anatomy.md) once for the big picture, then
start Lesson 1.

## The four lessons

> Run a lesson's test (from the repo root) with:
> ```bash
> autopkg run -vv Test-Recipes/<Name>.test.recipe.yaml --search-dir SharedProcessors
> ```

### Lesson 1 — `HelloWorld`: the anatomy of a processor
**New idea:** the skeleton — `Processor` subclass, `input_variables`,
`output_variables`, `main()`, reading from and writing to `self.env`.
Build a greeting and store it in an output variable.
- Edit: [`SharedProcessors/HelloWorld.py`](SharedProcessors/HelloWorld.py)
- Test: `HelloWorld.test.recipe.yaml`
- Read: [docs/01-anatomy.md](docs/01-anatomy.md)

### Lesson 2 — `Sleep`: optional inputs, defaults, and type coercion
**New idea:** an optional input with a `default`, and why you must `int()` a
value that may arrive as the string `"2"`. Pause execution, then resume.
- Edit: [`SharedProcessors/Sleep.py`](SharedProcessors/Sleep.py)
- Test: `Sleep.test.recipe.yaml`
- Read: [docs/02-input-and-output.md](docs/02-input-and-output.md)

### Lesson 3 — `StringFormat`: required inputs and failing loudly
**New idea:** a `required` input, a dict input, and wrapping risky work in
`try/except` to raise a clear `ProcessorError`. Apply Python's `str.format()`.
- Edit: [`SharedProcessors/StringFormat.py`](SharedProcessors/StringFormat.py)
- Test: `StringFormat.test.recipe.yaml`
- Read: [docs/02-input-and-output.md](docs/02-input-and-output.md#failing-loudly-processorerror)

### Lesson 4 — `FileHasher`: file I/O, helpers, multiple outputs, chaining
**New idea:** real work — stream a file in chunks, set **four** output
variables, factor logic into a helper method, and fall back to `%pathname%` so
the processor can run right after a download step.
- Edit: [`SharedProcessors/FileHasher.py`](SharedProcessors/FileHasher.py)
- Test: `FileHasher.test.recipe.yaml` (hashes the shipped `sample.txt`)
- Read: [docs/02-input-and-output.md](docs/02-input-and-output.md#chaining-reading-another-steps-output)

## After the lessons

[docs/03-testing.md](docs/03-testing.md) covers the two test layers in depth, and
[docs/04-publishing.md](docs/04-publishing.md) explains how the
`com.github.jgstew.macadmins2026.SharedProcessors/<Name>` namespace resolves and
how to share your processors — plus where to go next in `jgstew-recipes`.

### Starting your own processor

```bash
cp SharedProcessors/_template.py SharedProcessors/MyProcessor.py
# rename the MyProcessor class to match the file, then fill in main()
```

## Directory map

```
macadmins2026-recipes/
├── WORKSHOP.md                 # you are here
├── README.md
├── requirements.txt
├── test_processors_load.sh     # Layer 1 test: does every processor import?
├── docs/
│   ├── 00-setup.md
│   ├── 01-anatomy.md
│   ├── 02-input-and-output.md
│   ├── 03-testing.md
│   └── 04-publishing.md
├── SharedProcessors/
│   ├── _template.py                          # copy-me skeleton
│   ├── macadmins2026-SharedProcessors.recipe # registers the namespace
│   ├── AssertInputContainsString.py          # test helper (provided complete)
│   ├── HelloWorld.py     Sleep.py            # <- the exercises you edit
│   ├── StringFormat.py   FileHasher.py
│   └── solutions/                            # worked answers
│       ├── HelloWorld.py     Sleep.py
│       └── StringFormat.py   FileHasher.py
└── Test-Recipes/
    ├── HelloWorld.test.recipe.yaml   Sleep.test.recipe.yaml
    ├── StringFormat.test.recipe.yaml FileHasher.test.recipe.yaml
    ├── Workshop.recipelist.txt       # all four, by identifier
    └── sample.txt                    # fixed input for the FileHasher test
```
