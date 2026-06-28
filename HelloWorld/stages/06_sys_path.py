# Step 6 — stop typing PYTHONPATH: add /Library/AutoPkg to the path in code.
#
# Run it:  /usr/local/autopkg/python stages/06_sys_path.py
#
# Step 5 only ran if you prefixed the command with PYTHONPATH=/Library/AutoPkg.
# PYTHONPATH is just one way to fill sys.path — the list of folders Python
# searches, in order, whenever you import something. We can add that folder from
# inside the script instead, so the import works on its own and the command goes
# back to a plain /usr/local/autopkg/python with no prefix.
#
# Order matters: sys.path.insert() must run BEFORE `from autopkglib import ...`,
# because Python searches sys.path at the moment of the import. Putting an import
# below other code is what trips the linter rule E402 ("module level import not
# at top of file"), so we silence it with `# noqa: E402` — the same exception
# real AutoPkg processors carry when they do this.

import sys

sys.path.insert(0, "/Library/AutoPkg")  # look here first when importing

from autopkglib import Processor  # noqa: E402


class HelloWorld(Processor):
    def main(self):
        print("Hello World! (step 6)")


if __name__ == "__main__":
    HelloWorld().main()
