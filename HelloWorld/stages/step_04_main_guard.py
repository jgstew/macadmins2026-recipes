# Step 4 — only run when executed directly: if __name__ == "__main__".
#
# Run it:  /usr/local/autopkg/python stages/step_04_main_guard.py
#
# Now IMPORT it the way Step 3 did — this time it stays silent (the guard works):
#   PYTHONPATH=stages /usr/local/autopkg/python -c "import step_04_main_guard"
#
# In Step 3 the last line, HelloWorld().main(), ran the moment Python read the
# file — including when the file is IMPORTED. And importing is exactly how
# AutoPkg loads your processor: it imports the module to grab the class, it does
# NOT run the file as a script. If our "run it now" line fired on import, it
# would go off at the wrong time every time AutoPkg loaded the processor.
#
# The fix is the __main__ guard. Python sets the built-in variable __name__ to
# the string "__main__" ONLY when a file is run directly
# (/usr/local/autopkg/python thisfile.py).
# When the file is imported instead, __name__ is the module's name, so the
# guarded code is skipped. Result: run directly -> main() runs; imported by
# AutoPkg -> it does not. AutoPkg will call main() itself when it's ready.


class HelloWorld:
    def main(self):
        print("Hello World! (step 4)")


if __name__ == "__main__":
    HelloWorld().main()
