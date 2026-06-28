# Step 3 — make it a class with a main() method.
#
# Run it:  python3 stages/03_class.py
#
# AutoPkg processors are CLASSES. AutoPkg finds your processor by its class name
# and calls .main() on an instance of it. So we wrap main() in a class named
# HelloWorld (the class name will have to match the file name later — that is
# how AutoPkg locates it).
#
# The last line creates an instance and calls main() — which is precisely what
# AutoPkg will do for us once this is a real processor.

class HelloWorld:
    def main(self):
        print("Hello World!")


HelloWorld().main()
