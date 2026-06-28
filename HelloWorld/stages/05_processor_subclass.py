# Step 5 — inherit from autopkglib.Processor.
#
# Run it:  PYTHONPATH=/Library/AutoPkg /usr/local/autopkg/python stages/05_processor_subclass.py
#
# Subclassing Processor is what turns "a class" into "an AutoPkg processor." It
# inherits all the machinery AutoPkg relies on: the self.env environment,
# self.output() logging, argument handling, and the standalone run entry point.
#
# Notice the run command grew a PYTHONPATH. The file now imports autopkglib,
# which the installer placed in /Library/AutoPkg -- not on the bundled Python's
# default search path -- so PYTHONPATH=/Library/AutoPkg points Python at it.

from autopkglib import Processor


class HelloWorld(Processor):
    def main(self):
        print("Hello World!")


# We keep the __main__ guard from Step 4. Standing in for AutoPkg, we make an
# instance and call main() — but only when this file is run directly.
if __name__ == "__main__":
    HelloWorld().main()
