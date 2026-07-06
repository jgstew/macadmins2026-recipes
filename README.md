# macadmins2026-recipes

Workshops / presentation about AutoPkg for **PSU MacAdmins 2026**.

Each workshop is a self-contained folder you can work through on its own.

## Workshops

- **[HelloWorld/](HelloWorld/README.md)** — _From `print("Hello World!")` to an
  AutoPkg processor._ Build a processor from scratch, one small step at a time,
  understanding **why** each piece of the boilerplate exists. The goal is to
  understand what a processor actually is, not to learn Python.

- **[FileHasher/](FileHasher/README.md)** — _Build a real processor: a file hasher._
  The follow-up to HelloWorld — start from a complete-but-empty skeleton and add one
  thing at a time (each step's file is the answer to the previous step's task), then
  chain after AutoPkg's built-in `URLDownloaderPython` to hash a download. No
  dependencies beyond AutoPkg itself.

## Quick start

1. Install AutoPkg (it brings its own Python plus `autopkglib`): download
   `autopkg-2.9.0.pkg` from
   <https://github.com/autopkg/autopkg/releases/tag/v2.9.0> and run it.
2. Then:

```bash
cd HelloWorld

# Step 1 — a plain script (AutoPkg's bundled Python runs everything)
/usr/local/autopkg/python stages/step_01_hello.py

# Step 10 — the finished processor, run inside a recipe
autopkg run -v HelloWorld.recipe.yaml --search-dir .
```

## Layout

```
macadmins2026-recipes/
├── HelloWorld/                    # workshop 1: anatomy of a processor (start here)
│   ├── README.md                  # index: overview, setup, links to each step
│   ├── stages/                    # one step_NN_*.py + step_NN_*.md (+ .sh) per step
│   ├── HelloWorld.py              # the finished processor
│   └── HelloWorld.recipe.yaml     # a recipe that runs it
└── FileHasher/                    # workshop 2: a real, useful processor
    ├── README.md                  # index: setup, the steps, the finished processor
    ├── stages/                    # step_01..step_04 (.md + .py + .sh) + sample.txt
    ├── FileHasher.py              # the finished processor (MD5, reads %pathname%)
    └── FileHasher.recipe.yaml     # URLDownloaderPython → FileHasher
```
