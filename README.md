# macadmins2026-recipes

Workshops / presentation about AutoPkg for **PSU MacAdmins 2026**.

Each workshop is a self-contained folder you can work through on its own.

## Workshops

- **[HelloWorld/](HelloWorld/WORKSHOP.md)** — *From `print("Hello World!")` to an
  AutoPkg processor.* Build a processor from scratch, one small step at a time,
  understanding **why** each piece of the boilerplate exists. The goal is to
  understand what a processor actually is, not to learn Python.

_(More workshops can be added as sibling folders alongside `HelloWorld/`.)_

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
└── HelloWorld/                    # one workshop, self-contained
    ├── WORKSHOP.md                # index: overview, setup, links to each step (start here)
    ├── stages/                    # one step_NN_*.py + step_NN_*.md per step
    ├── HelloWorld.py              # the finished processor (Step 10)
    └── HelloWorld.recipe.yaml     # a recipe that runs it
```
