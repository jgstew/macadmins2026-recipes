# 0. Setup

You need three things to write and run AutoPkg processors: **AutoPkg itself**, a
**Python** that can import `autopkglib`, and this **repo**.

## 1. Get this repo

```bash
git clone https://github.com/jgstew/macadmins2026-recipes.git
cd macadmins2026-recipes
```

## 2. Get AutoPkg

The processors `import` from `autopkglib`, which ships inside the AutoPkg
source tree (it is *not* a pip package). The simplest layout is to clone
AutoPkg **next to** this repo:

```bash
cd ..
git clone https://github.com/autopkg/autopkg.git
cd macadmins2026-recipes
```

You should now have:

```
parent-folder/
├── autopkg/                 # the autopkg checkout (has Code/autopkglib)
└── macadmins2026-recipes/   # this repo
```

On macOS you can instead install the AutoPkg `.pkg` from
<https://github.com/autopkg/autopkg/releases>, which puts the `autopkg`
command on your PATH and a Python at `/usr/local/autopkg/python` (the
interpreter named in every processor's shebang line).

## 3. Verify your setup

The load test imports every processor. If `autopkglib` is reachable, the
provided processors (and all the solutions) import cleanly:

```bash
./test_processors_load.sh
```

You should see `PASS` lines for `AssertInputContainsString.py`, the four
exercise files, and everything under `solutions/`. The four exercise files
import fine even though they are unfinished — importing only loads the code,
it does not *run* it.

## 4. (Optional) Run a processor directly

You don't need a full recipe to poke at a processor. With `autopkglib` on the
`PYTHONPATH` you can instantiate one and call `main()`:

```bash
PYTHONPATH="../autopkg/Code:SharedProcessors" python3 <<'EOF'
from solutions.HelloWorld import HelloWorld
p = HelloWorld({})
p.env["greeting_name"] = "MacAdmins"
p.main()
print(p.env["greeting_result"])
EOF
```

That's it — on to [the anatomy of a processor](01-anatomy.md).
