# Step 5 — inherit from autopkglib.Processor.
#
# Run it:  PYTHONPATH=../../autopkg/Code /usr/local/autopkg/python stages/05_processor_subclass.py
#
# Subclassing Processor is what turns "a class" into "an AutoPkg processor." It
# inherits all the machinery AutoPkg relies on: the self.env environment,
# self.output() logging, argument handling, and the standalone run entry point.
#
# Notice the run command changed. The file now imports autopkglib, so Python has
# to be able to FIND AutoPkg (that is the PYTHONPATH) and we use the Python that
# ships with AutoPkg (it already has AutoPkg's dependencies, like pyyaml).

from autopkglib import Processor


class HelloWorld(Processor):
    def main(self):
        print("Hello World!")


# We keep the __main__ guard from Step 4. Standing in for AutoPkg, we make an
# instance and call main() — but only when this file is run directly.
if __name__ == "__main__":
    HelloWorld().main()
