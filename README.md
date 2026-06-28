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

```bash
# AutoPkg's code, cloned next to this repo (so Python can import autopkglib)
git clone https://github.com/autopkg/autopkg.git ../autopkg

# pick a workshop folder and follow its WORKSHOP.md
cd HelloWorld

# Step 1 — a plain script
python3 stages/01_hello.py

# Step 8 — the finished processor, run inside a recipe
autopkg run -v HelloWorld.recipe.yaml --search-dir .
```

## Layout

```
macadmins2026-recipes/
└── HelloWorld/                    # one workshop, self-contained
    ├── WORKSHOP.md                # the guided, step-by-step build (start here)
    ├── stages/01_*.py … 08_*.py   # runnable snapshot at each step
    ├── HelloWorld.py              # the finished processor (Step 8)
    └── HelloWorld.recipe.yaml     # a recipe that runs it
```
