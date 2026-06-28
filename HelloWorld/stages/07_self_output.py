# Step 7 — log with self.output() instead of print().
#
# Run it:  /usr/local/autopkg/python stages/07_self_output.py
#   (No PYTHONPATH needed — the Step 6 sys.path line, kept below, handles it.)
#
# print() always writes to stdout and ignores AutoPkg entirely. self.output() is
# AutoPkg's logging: it tags the line with the processor name and only shows it
# when the run is verbose enough (the -v flags on `autopkg run`).
#
# self.output() reads that verbosity level from self.env — the shared bag of
# values AutoPkg gives every processor. That is why, to run this standalone, we
# now hand the instance an env dict with "verbose" turned on. Here WE are
# playing the role AutoPkg normally plays.

import sys

sys.path.insert(0, "/Library/AutoPkg")

from autopkglib import Processor  # noqa: E402


class HelloWorld(Processor):
    def main(self):
        self.output("Hello World! (step 7)")


# Stand in for AutoPkg: provide an env (with verbose on) and call main().
# Try changing 1 to 0 — the message disappears, exactly like a non-verbose run.
if __name__ == "__main__":
    HelloWorld({"verbose": 1}).main()
