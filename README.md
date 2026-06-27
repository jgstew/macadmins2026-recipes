# macadmins2026-recipes

Repo for a workshop / presentation about AutoPkg at **PSU MacAdmins 2026**:
**writing AutoPkg processors from scratch.**

You'll build four working processors — `HelloWorld`, `Sleep`, `StringFormat`,
and `FileHasher` — one new concept at a time, then learn how to test and share
them. The examples are distilled from real processors in
[jgstew-recipes](https://github.com/jgstew/jgstew-recipes).

## Start here

➡️ **[WORKSHOP.md](WORKSHOP.md)** — the guided lessons.

## Quick start

```bash
# 1. get an autopkg checkout next to this repo (see docs/00-setup.md)
git clone https://github.com/autopkg/autopkg.git ../autopkg

# 2. confirm every processor imports
./test_processors_load.sh

# 3. do Lesson 1, then run its test
autopkg run -vv Test-Recipes/HelloWorld.test.recipe.yaml --search-dir SharedProcessors
```

## Layout

- `WORKSHOP.md` — the workshop guide and lesson order.
- `docs/` — setup, processor anatomy, inputs/outputs, testing, and publishing.
- `SharedProcessors/` — the exercise files you edit (plus `_template.py`, a test
  helper, and worked answers under `solutions/`).
- `Test-Recipes/` — a test recipe per lesson; "done" means its test passes.

## References

- AutoPkg: <https://github.com/autopkg/autopkg>
- Processor locations: <https://github.com/autopkg/autopkg/wiki/Processor-Locations>
- jgstew-recipes (the source of these examples): <https://github.com/jgstew/jgstew-recipes>
