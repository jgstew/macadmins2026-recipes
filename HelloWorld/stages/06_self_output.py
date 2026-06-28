# Step 6 — log with self.output() instead of print().
#
# Run it:  PYTHONPATH=../../autopkg/Code /usr/local/autopkg/python stages/06_self_output.py
#
# print() always writes to stdout and ignores AutoPkg entirely. self.output() is
# AutoPkg's logging: it tags the line with the processor name and only shows it
# when the run is verbose enough (the -v flags on `autopkg run`).
#
# self.output() reads that verbosity level from self.env — the shared bag of
# values AutoPkg gives every processor. That is why, to run this standalone, we
# now hand the instance an env dict with "verbose" turned on. Here WE are
# playing the role AutoPkg normally plays.

from autopkglib import Processor


class HelloWorld(Processor):
    def main(self):
        self.output("Hello World!")


# Stand in for AutoPkg: provide an env (with verbose on) and call main().
# Try changing 1 to 0 — the message disappears, exactly like a non-verbose run.
if __name__ == "__main__":
    HelloWorld({"verbose": 1}).main()
