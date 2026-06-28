# Step 2 — move the work into a function.
#
# Run it:  /usr/local/autopkg/python stages/step_02_function.py
#
# AutoPkg needs a named entry point it can call WHEN IT CHOOSES, not code that
# runs the instant the file is read. (AutoPkg imports your file; any work left
# at the top level would fire during that import.) So we put the work inside a
# function called main() — that is the exact name AutoPkg will look for later.
#
# For now we still call main() ourselves on the last line.

def main():
    print("Hello World! (step 2)")


main()
